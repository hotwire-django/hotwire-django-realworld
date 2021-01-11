from django.shortcuts import get_object_or_404, render
from articles.models import Tag
from django.contrib.auth import login as auth_login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView as AuthLoginView
from django.shortcuts import redirect
from .forms import UserCreationForm, UserLoginForm


def index(request):
    tags = Tag.objects.all()
    tag_slug = request.GET.get("tag")
    tag = None
    active_tab = request.GET.get("active_tab", "global")
    article_params = ""
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        active_tab = "tag"
        article_params = f"tag={tag_slug}"
    if active_tab == "feed":
        article_params = f"followed_by={request.user.username}"

    return render(
        request,
        "index.html",
        context={
            "tags": tags,
            "nav_link": "home",
            "tag": tag,
            "active_tab": active_tab,
            "article_params": article_params,
        },
    )


class LoginView(AuthLoginView):
    template_name = "login.html"
    form_class = UserLoginForm
    extra_context = {"nav_link": "sign_in"}

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form.
        Turbo wants a 422 on errors.
        """
        return self.render_to_response(self.get_context_data(form=form), status=422)

    def form_valid(self, form):
        """Security check complete. Log the user in.
        Turbo wants a 303 on success.
        """
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url(), status=303)


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
    return render(
        request, "signup.html", {"form": form, "nav_link": "sign_up"}, status=status
    )
