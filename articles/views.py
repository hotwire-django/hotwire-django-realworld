
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Count

from .models import Article
from .forms import ArticleForm


class IsAuthenticatedOrReadOnly(UserPassesTestMixin):
    def test_func(self):
        return self.request.method == 'GET' or self.request.user.is_authenticated


def view(req, slug):
    return render(req, "articles/detail.html", {
        "article": Article.objects.get(slug=slug)
    })


class EditArticle(LoginRequiredMixin, UpdateView):
    template_name = "articles/edit.html"
    model = Article
    form_class = ArticleForm

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


class FavoriteArticle(IsAuthenticatedOrReadOnly, UpdateView):
    fields = []
    template_name = 'articles/_favorite.html'
    queryset = Article.objects.select_related('author__user').annotate(
        favorited_by__count=Count('favorited_by')
    )

    def get_success_url(self):
        return reverse_lazy('article_favorite', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['has_favorited'] = self.request.user.profile.has_favorited(self.object)

        return context

    def form_valid(self, form):
        profile = self.request.user.profile

        if profile.has_favorited(self.object):
            profile.unfavorite(self.object)
        else:
            profile.favorite(self.object)

        return HttpResponseRedirect(self.get_success_url(), status=303)
