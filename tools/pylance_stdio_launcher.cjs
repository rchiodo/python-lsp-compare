const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

function parseArgs(argv) {
    const options = {
        serverPath: '',
        workspaceRoot: process.cwd(),
        productName: 'Pylance',
        version: 'benchmark-launcher',
        logLevel: 'Info',
    };

    for (let index = 2; index < argv.length; index += 1) {
        const key = argv[index];
        const value = argv[index + 1];
        if (!value) {
            throw new Error(`Missing value for ${key}`);
        }
        if (key === '--server-path') {
            options.serverPath = value;
        } else if (key === '--workspace-root') {
            options.workspaceRoot = value;
        } else if (key === '--product-name') {
            options.productName = value;
        } else if (key === '--version') {
            options.version = value;
        } else if (key === '--log-level') {
            options.logLevel = value;
        } else {
            throw new Error(`Unknown argument: ${key}`);
        }
        index += 1;
    }

    if (!options.serverPath) {
        throw new Error('Expected --server-path <path-to-dist/server.js>');
    }

    return options;
}

class NodeReadOnlyFileSystem {
    constructor(workspaceRoot, modulePath) {
        this.workspaceRoot = path.resolve(workspaceRoot);
        this.modulePath = path.resolve(modulePath);
    }

    existsSync(targetPath) {
        return fs.existsSync(targetPath);
    }

    chdir(targetPath) {
        process.chdir(targetPath);
    }

    readdirEntriesSync(targetPath) {
        return fs.readdirSync(targetPath, { withFileTypes: true }).map((entry) => ({
            name: entry.name,
            isFile: () => entry.isFile(),
            isDirectory: () => entry.isDirectory(),
            isSymbolicLink: () => entry.isSymbolicLink(),
        }));
    }

    readdirSync(targetPath) {
        return fs.readdirSync(targetPath);
    }

    readFileSync(targetPath, encoding = null) {
        return fs.readFileSync(targetPath, encoding === null ? undefined : encoding);
    }

    statSync(targetPath) {
        const stats = fs.statSync(targetPath);
        return {
            size: stats.size,
            isFile: () => stats.isFile(),
            isDirectory: () => stats.isDirectory(),
            isSymbolicLink: () => stats.isSymbolicLink(),
        };
    }

    realpathSync(targetPath) {
        return fs.realpathSync.native ? fs.realpathSync.native(targetPath) : fs.realpathSync(targetPath);
    }

    getModulePath() {
        return this.modulePath;
    }

    readFile(targetPath) {
        return fs.promises.readFile(targetPath);
    }

    readFileText(targetPath, encoding = 'utf-8') {
        return fs.promises.readFile(targetPath, encoding);
    }

    realCasePath(targetPath) {
        return this.realpathSync(targetPath);
    }

    isMappedFilePath() {
        return false;
    }

    getOriginalFilePath(mappedFilePath) {
        return mappedFilePath;
    }

    getMappedFilePath(originalFilePath) {
        return originalFilePath;
    }

    getUri(targetPath) {
        return pathToFileURL(targetPath).toString();
    }

    dispose() {
    }
}

function main() {
    const options = parseArgs(process.argv);
    const serverPath = path.resolve(options.serverPath);
    const packageRoot = path.dirname(path.dirname(serverPath));
    const resolveFromPackage = (request) => require.resolve(request, { paths: [packageRoot] });
    const lspNode = require(resolveFromPackage('vscode-languageserver/node'));
    const serverModule = require(serverPath);

    const { createConnection, ProposedFeatures } = lspNode;
    const { LimitedPylanceServer, LogLevel } = serverModule;

    const connection = createConnection(process.stdin, process.stdout, undefined, ProposedFeatures.all);
    const fileSystem = new NodeReadOnlyFileSystem(options.workspaceRoot, path.dirname(serverPath));
    const logLevel = LogLevel[options.logLevel] || LogLevel.Info;

    const server = new LimitedPylanceServer(
        connection,
        {
            productName: options.productName,
            version: options.version,
            fileSystem,
        },
        logLevel
    );

    process.on('exit', () => {
        server.end();
        fileSystem.dispose();
    });
    process.on('SIGINT', () => process.exit(0));
    process.on('SIGTERM', () => process.exit(0));

    server.start();
}

main();