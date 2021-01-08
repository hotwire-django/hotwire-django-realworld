from django.shortcuts import render
from articles.models import Article, Tag
from django.contrib.auth import login as auth_login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView as AuthLoginView
from django.shortcuts import redirect
from django.db.models import Count
from .forms import UserCreationForm, UserLoginForm


def index(request):
    articles = Article.objects.all().select_related("author__user").annotate(favorited_by__count=Count("favorited_by"))
    tags = Tag.objects.all()
    return render(request, "index.html", context={"articles": articles, "tags": tags})


class LoginView(AuthLoginView):
    template_name = "login.html"
    form_class = UserLoginForm

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
    return render(request, "signup.html", {"form": form}, status=status)
