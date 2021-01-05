from django.shortcuts import render
from articles.models import Article, Tag

# Create your views here.
def index(req):
    articles = Article.objects.all()
    tags = Tag.objects.all()
    return render(req, "index.html", context={"articles": articles, "tags": tags})
