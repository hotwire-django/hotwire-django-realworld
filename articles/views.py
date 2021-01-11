from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from .models import Article, Tag
from .forms import ArticleForm


def view(req, slug):
    return render(req, "articles/detail.html")


class ListArticle(ListView):
    template_name = "articles/list.html"
    paginate_by = 10
    model = Article

    def _get_query_context(self):
        qs = {"active_tab": "global", "tag": None}
        tag_slug = self.request.GET.get("tag")
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            qs["tag"] = tag
            qs["active_tab"] = "tag"
        return qs

    def get_queryset(self):
        qs = super().get_queryset()
        if tag := self._get_query_context()["tag"]:
            qs = qs.filter(tags__slug=tag.slug)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self._get_query_context())
        return ctx


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
