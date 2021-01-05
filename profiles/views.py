from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm


def view(req, profile):
    return render(req, "profile/detail.html")


@login_required
def edit(request):
    status = 200
    initial = {
        "image": request.user.profile.image,
        "bio": request.user.profile.bio,
    }

    if request.method == "POST":
        form = EditProfileForm(request.POST, initial=initial)
        if form.is_valid():
            form.save(request.user)
            a = redirect("profile_view", profile=request.user.username)
            # Turbo expects a 303 response on form success
            a.status_code = 303
            return a
        else:
            # Turbo expects a 422 response on form errors
            status = 422
    else:
        form = EditProfileForm(initial=initial)

    return render(request, "profile/edit.html", {"form": form}, status=status)