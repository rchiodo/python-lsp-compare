from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)


class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)


def load_published_articles() -> list[Article]:
    queryset = Article.objects.filter(published=True).select_related("author")
    return list(queryset)


articles = load_published_articles()
filtered = Article.objects.filter(author__name__icontains="copilot")
title_sample = filtered.first()