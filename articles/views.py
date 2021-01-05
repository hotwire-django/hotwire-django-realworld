from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def view(req, slug):
    return render(req, "articles/detail.html")


@login_required
def edit(req, slug):
    return render(req, "articles/edit.html")


@login_required
def create(req):
    return render(req, "articles/edit.html")