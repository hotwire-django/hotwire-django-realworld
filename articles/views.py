from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.db.models import Count
from .models import Article, Tag
from .forms import ArticleForm


def view(req, slug):
    return render(req, "articles/detail.html")


class ListArticle(ListView):
    template_name = "articles/list.html"
    paginate_by = 10
    model = Article

    def _get_query_context(self):
        ctx = {
            "tag": None,
            "query_string": [],
            "author": None,
            "favorited": None,
            "followed_by": None,
        }

        tag_slug = self.request.GET.get("tag")
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            ctx["tag"] = tag
            ctx["query_string"].append(f"tag={tag_slug}")

        author = self.request.GET.get("author")
        if author:
            ctx["author"] = author
            ctx["query_string"].append(f"author={author}")

        favorited = self.request.GET.get("favorited")
        if favorited:
            ctx["favorited"] = favorited
            ctx["query_string"].append(f"favorited={favorited}")

        followed_by = self.request.GET.get("followed_by")
        if followed_by:
            ctx["followed_by"] = followed_by
            ctx["query_string"].append(f"followed_by={followed_by}")

        ctx["query_string"] = "&".join(ctx["query_string"])
        return ctx

    def get_queryset(self):
        qs = (
            Article.objects.all()
            .select_related("author__user")
            .annotate(favorited_by__count=Count("favorited_by"))
        )

        if tag := self._get_query_context()["tag"]:
            qs = qs.filter(tags__slug=tag.slug)

        if author := self._get_query_context()["author"]:
            qs = qs.filter(author__user__username=author)

        if favorited := self._get_query_context()["favorited"]:
            qs = qs.filter(favorited_by__user__username=favorited)

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
