from django.shortcuts import render
from articles.models import Article

# Create your views here.
def index(req):
    articles = Article.objects.all()
    return render(req, "index.html", context={"articles": articles})
