from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def view(req, profile):
    return render(req, "profile/detail.html")


@login_required
def edit(req):
    return render(req, "profile/edit.html")