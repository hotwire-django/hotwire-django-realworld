from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from .models import Article
from .forms import ArticleForm


def view(req, slug):
    return render(req, "articles/detail.html")


class EditArticle(LoginRequiredMixin, UpdateView):
    template_name = "articles/edit.html"
    model = Article
    form_class = ArticleForm
    extra_context = {"nav_link": "new_post"}

    def get_success_url(self):
        return reverse_lazy("article_view", kwargs={"slug": self.object.slug})

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form.
        Turbo wants a 422 on errors.
        """
        return self.render_to_response(self.get_context_data(form=form), status=422)

    def form_valid(self, form):
        """Security check complete. Log the user in.
        Turbo wants a 303 on success.
        """
        self.object = form.save(self.request.user)
        return HttpResponseRedirect(self.get_success_url(), status=303)


class CreateArticle(LoginRequiredMixin, CreateView):
    template_name = "articles/edit.html"
    model = Article
    form_class = ArticleForm
    extra_context = {"nav_link": "new_post"}

    def get_success_url(self):
        return reverse_lazy("article_view", kwargs={"slug": self.object.slug})

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form.
        Turbo wants a 422 on errors.
        """
        return self.render_to_response(self.get_context_data(form=form), status=422)

    def form_valid(self, form):
        """Security check complete. Log the user in.
        Turbo wants a 303 on success.
        """
        self.object = form.save(self.request.user)
        return HttpResponseRedirect(self.get_success_url(), status=303)
