from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Article(models.Model):
    title = models.CharField(max_length=200)
    published = models.BooleanField(default=False)


def build_article_metadata(article: Article) -> tuple[str, str]:
    slug = slugify(article.title)
    detail_url = reverse("article-detail", kwargs={"slug": slug})
    return slug, detail_url


article = Article(title="Copilot Benchmarks", published=True)
article_slug, article_url = build_article_metadata(article)
queryset = Article.objects.filter(published=True).values_list("title", flat=True)
first_title = queryset.first()
