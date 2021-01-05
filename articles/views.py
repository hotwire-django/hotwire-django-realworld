from django.shortcuts import render


def article(req, title):
    print(title)
    return render(req, "articles/article.html")
