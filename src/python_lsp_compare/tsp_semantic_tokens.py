from __future__ import annotations

import ast
import io
import keyword
import tokenize
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .lsp_client import LspClient


TOKEN_TYPES = [
    "comment",
    "keyword",
    "operator",
    "string",
    "number",
    "type",
    "class",
    "function",
    "method",
    "property",
    "variable",
    "parameter",
    "module",
    "selfParameter",
    "clsParameter",
    "builtinConstant",
]
TOKEN_TYPE_INDEX = {name: index for index, name in enumerate(TOKEN_TYPES)}

DECLARATION_MODIFIER = 1 << 0
ASYNC_MODIFIER = 1 << 3
BUILTIN_MODIFIER = 1 << 9
CALLABLE_MODIFIER = 1 << 11
CLASS_MEMBER_MODIFIER = 1 << 12


@dataclass(slots=True)
class SemanticTokenEntry:
    line: int
    character: int
    length: int
    token_type: str
    modifiers: int = 0


class _SemanticTokenBuilder:
    def __init__(self) -> None:
        self._entries: dict[tuple[int, int, int], tuple[SemanticTokenEntry, int]] = {}

    def add(
        self,
        line: int,
        character: int,
        length: int,
        token_type: str,
        modifiers: int = 0,
        *,
        priority: int = 1,
    ) -> None:
        if length <= 0 or line < 0 or character < 0:
            return
        key = (line, character, length)
        current = self._entries.get(key)
        entry = SemanticTokenEntry(line, character, length, token_type, modifiers)
        if current is None or priority >= current[1]:
            self._entries[key] = (entry, priority)

    def entries(self) -> list[SemanticTokenEntry]:
        return sorted(
            (entry for entry, _priority in self._entries.values()),
            key=lambda item: (item.line, item.character, item.length, item.token_type),
        )

    def encode(self) -> list[int]:
        data: list[int] = []
        previous_line = 0
        previous_character = 0
        for entry in self.entries():
            delta_line = entry.line - previous_line
            delta_character = entry.character if delta_line else entry.character - previous_character
            data.extend(
                [
                    delta_line,
                    delta_character,
                    entry.length,
                    TOKEN_TYPE_INDEX.get(entry.token_type, TOKEN_TYPE_INDEX["variable"]),
                    entry.modifiers,
                ]
            )
            previous_line = entry.line
            previous_character = entry.character
        return data


class _SemanticTokenCollector(ast.NodeVisitor):
    def __init__(
        self,
        client: LspClient,
        file_path: Path,
        source: str,
        snapshot: int,
        start_line: int,
        start_character: int,
        end_line: int,
        end_character: int,
        context: dict[str, Any] | None,
    ) -> None:
        self._client = client
        self._file_path = file_path
        self._uri = file_path.as_uri()
        self._source = source
        self._snapshot = snapshot
        self._builder = _SemanticTokenBuilder()
        self._parents: dict[ast.AST, ast.AST | None] = {}
        self._class_stack: list[str] = []
        self._start = (start_line, start_character)
        self._end = (end_line, end_character)
        self._context = dict(context or {})
        self.type_query_count = 0
        self.type_query_failure_count = 0

    def collect(self) -> dict[str, Any]:
        self._add_syntax_tokens()
        try:
            tree = ast.parse(self._source, filename=str(self._file_path))
        except SyntaxError:
            tree = None
        if tree is not None:
            self._parents[tree] = None
            self.visit(tree)
        entries = self._builder.entries()
        counts = Counter(entry.token_type for entry in entries)
        return {
            "data": self._builder.encode(),
            "semantic_token_count": len(entries),
            "type_query_count": self.type_query_count,
            "type_query_failure_count": self.type_query_failure_count,
            "token_type_counts": dict(sorted(counts.items())),
            "legend": {"tokenTypes": TOKEN_TYPES},
        }

    def generic_visit(self, node: ast.AST) -> None:
        for child in ast.iter_child_nodes(node):
            self._parents[child] = node
        super().generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._add_identifier(node.lineno - 1, node.col_offset + 6, len(node.name), "class", DECLARATION_MODIFIER, priority=3)
        self._class_stack.append(node.name)
        self.generic_visit(node)
        self._class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._add_function_definition(node, is_async=False)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._add_function_definition(node, is_async=True)
        self.generic_visit(node)

    def visit_arg(self, node: ast.arg) -> None:
        token_type = "parameter"
        if node.arg == "self":
            token_type = "selfParameter"
        elif node.arg == "cls":
            token_type = "clsParameter"
        self._add_identifier(node.lineno - 1, node.col_offset, len(node.arg), token_type, DECLARATION_MODIFIER, priority=3)
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            alias_name = alias.asname or alias.name.split(".")[0]
            location = self._find_name_position(node.lineno - 1, alias_name)
            if location is not None:
                self._add_identifier(location[0], location[1], len(alias_name), "module", 0, priority=2)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module_name = node.module or ""
        if module_name:
            location = self._find_name_position(node.lineno - 1, module_name.split(".")[0])
            if location is not None:
                self._add_identifier(location[0], location[1], len(module_name.split(".")[0]), "module", 0, priority=2)
        for alias in node.names:
            alias_name = alias.asname or alias.name
            location = self._find_name_position(node.lineno - 1, alias_name)
            if location is not None:
                self._add_identifier(location[0], location[1], len(alias_name), "module", 0, priority=2)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        parent = self._parents.get(node)
        if self._is_annotation_name(node):
            token_type = "type"
            modifiers = 0
            priority = 3
        elif isinstance(node.ctx, ast.Store):
            token_type = "variable"
            modifiers = DECLARATION_MODIFIER
            priority = 3
        else:
            is_call_target = isinstance(parent, ast.Call) and parent.func is node
            token_type = self._resolve_token_type_for_span(
                line=node.lineno - 1,
                character=node.col_offset,
                length=len(node.id),
                fallback="function" if is_call_target else "variable",
                is_attribute=False,
                is_call_target=is_call_target,
            )
            modifiers = CALLABLE_MODIFIER if is_call_target else 0
            priority = 4
        self._add_identifier(node.lineno - 1, node.col_offset, len(node.id), token_type, modifiers, priority=priority)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        line = (node.end_lineno or node.lineno) - 1
        character = (node.end_col_offset or node.col_offset) - len(node.attr)
        parent = self._parents.get(node)
        is_call_target = isinstance(parent, ast.Call) and parent.func is node
        token_type = self._resolve_token_type_for_span(
            line=line,
            character=character,
            length=len(node.attr),
            fallback="method" if is_call_target else "property",
            is_attribute=True,
            is_call_target=is_call_target,
        )
        modifiers = CLASS_MEMBER_MODIFIER | (CALLABLE_MODIFIER if is_call_target else 0)
        self._add_identifier(line, character, len(node.attr), token_type, modifiers, priority=4)
        self.generic_visit(node)

    def _add_function_definition(self, node: ast.FunctionDef | ast.AsyncFunctionDef, *, is_async: bool) -> None:
        token_type = "method" if self._class_stack else "function"
        modifier = DECLARATION_MODIFIER | (ASYNC_MODIFIER if is_async else 0)
        keyword_length = 9 if is_async else 4
        self._add_identifier(node.lineno - 1, node.col_offset + keyword_length, len(node.name), token_type, modifier, priority=3)

    def _resolve_token_type_for_span(
        self,
        *,
        line: int,
        character: int,
        length: int,
        fallback: str,
        is_attribute: bool,
        is_call_target: bool,
    ) -> str:
        if length <= 0:
            return fallback
        query_context = dict(self._context)
        query_context["phase"] = f"{self._context.get('phase', 'measured')}:type-query"
        query_context["parent_method"] = "typeServer/semanticTokens"
        node = {
            "uri": self._uri,
            "range": {
                "start": {"line": line, "character": character},
                "end": {"line": line, "character": character + length},
            },
        }
        try:
            self.type_query_count += 1
            result = self._client.tsp_get_computed_type(node, self._snapshot, context=query_context)
        except Exception:
            self.type_query_failure_count += 1
            return fallback
        return _classify_type_result(result, fallback=fallback, is_attribute=is_attribute, is_call_target=is_call_target)

    def _is_annotation_name(self, node: ast.AST) -> bool:
        current: ast.AST | None = node
        while current is not None:
            parent = self._parents.get(current)
            if parent is None:
                return False
            if isinstance(parent, ast.arg) and parent.annotation is current:
                return True
            if isinstance(parent, ast.AnnAssign) and parent.annotation is current:
                return True
            if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef)) and parent.returns is current:
                return True
            if isinstance(parent, ast.Subscript):
                current = parent
                continue
            return False
        return False

    def _find_name_position(self, line_index: int, name: str) -> tuple[int, int] | None:
        lines = self._source.splitlines()
        if line_index < 0 or line_index >= len(lines):
            return None
        character = lines[line_index].find(name)
        if character < 0:
            return None
        return (line_index, character)

    def _add_identifier(
        self,
        line: int,
        character: int,
        length: int,
        token_type: str,
        modifiers: int,
        *,
        priority: int,
    ) -> None:
        if not self._is_within_requested_range(line, character, length):
            return
        self._builder.add(line, character, length, token_type, modifiers, priority=priority)

    def _add_syntax_tokens(self) -> None:
        readline = io.StringIO(self._source).readline
        for token in tokenize.generate_tokens(readline):
            line = token.start[0] - 1
            character = token.start[1]
            length = token.end[1] - token.start[1]
            if not self._is_within_requested_range(line, character, length):
                continue
            if token.type == tokenize.COMMENT:
                self._builder.add(line, character, length, "comment", priority=1)
            elif token.type == tokenize.STRING:
                self._builder.add(line, character, length, "string", priority=1)
            elif token.type == tokenize.NUMBER:
                self._builder.add(line, character, length, "number", priority=1)
            elif token.type == tokenize.OP:
                self._builder.add(line, character, length, "operator", priority=1)
            elif token.type == tokenize.NAME:
                if token.string in {"True", "False", "None"}:
                    self._builder.add(line, character, length, "builtinConstant", BUILTIN_MODIFIER, priority=2)
                elif keyword.iskeyword(token.string):
                    self._builder.add(line, character, length, "keyword", priority=1)

    def _is_within_requested_range(self, line: int, character: int, length: int) -> bool:
        start = (line, character)
        end = (line, character + length)
        if start < self._start:
            return False
        if end > self._end:
            return False
        return True


def _classify_type_result(result: Any, *, fallback: str, is_attribute: bool, is_call_target: bool) -> str:
    if not isinstance(result, dict):
        return fallback
    kind = str(result.get("kind", "")).lower()
    type_name = ""
    for key in ("name", "className", "moduleName"):
        value = result.get(key)
        if isinstance(value, str):
            type_name = value
            break

    if "module" in kind:
        return "module"
    if is_call_target and ("class" in kind or _looks_like_type_name(type_name)):
        return "class"
    if is_call_target:
        return "method" if is_attribute else "function"
    if "function" in kind or "overloaded" in kind:
        return "method" if is_attribute else "function"
    if "class" in kind or _looks_like_type_name(type_name):
        return "class" if not is_attribute else "property"
    if is_attribute:
        return "property"
    return fallback


def _looks_like_type_name(value: str) -> bool:
    return bool(value) and value[:1].isupper()


def compute_semantic_tokens(
    client: LspClient,
    file_path: Path,
    *,
    snapshot: int,
    start_line: int,
    start_character: int,
    end_line: int,
    end_character: int,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source = file_path.read_text(encoding="utf-8")
    collector = _SemanticTokenCollector(
        client=client,
        file_path=file_path,
        source=source,
        snapshot=snapshot,
        start_line=start_line,
        start_character=start_character,
        end_line=end_line,
        end_character=end_character,
        context=context,
    )
    return collector.collect()
