from django.shortcuts import render
from articles.models import Article, Tag
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect
from .forms import UserCreationForm


def index(req):
    articles = Article.objects.all()
    tags = Tag.objects.all()
    return render(req, "index.html", context={"articles": articles, "tags": tags})


def login(req):
    return render(req, "login.html")


def signup(request):
    status = 200
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            a = redirect("index")
            # Turbo expects a 303 response on form success
            a.status_code = 303
            return a
        # Turbo expects a 422 response on form errors
        status = 422
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form}, status=status)
