from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, ListView
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Count

from .models import Article, Comment, Tag
from .forms import ArticleForm, CommentForm
from .mixins import UserIsAuthorMixin


class ViewArticle(DetailView):
    model = Article
    template_name = "articles/detail.html"
    context_object_name = "article"


class AddComment(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "articles/_add_comment.html"
    form_class = CommentForm

    def get_login_url(self):
        return reverse_lazy("login_to_add_comment", kwargs={"slug": self.kwargs["slug"]})

    def form_valid(self, form):
        form.instance.article = Article.objects.get(slug=self.kwargs["slug"])
        form.instance.author = self.request.user.profile
        new_comment = form.save()
        comment_author = self.request.user

        def render_comment_turbo_stream():
            new_comment_partial = render_to_string("articles/_comment.html",
                                                   {"comment": new_comment, "user": comment_author})
            return f'<turbo-stream target="comments" action="prepend">' \
                   f'<template>{new_comment_partial}<template>' \
                   f'</turbo-stream>'

        return StreamingHttpResponse(render_comment_turbo_stream(), content_type="text/html; turbo-stream;")


class LoginToAddComment(TemplateView):
    template_name = "articles/_login_to_add_comment.html"


class ViewComment(DetailView):
    model = Comment
    template_name = "articles/_comment.html"
    context_object_name = "comment"


class EditComment(UserIsAuthorMixin, LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'articles/_edit_comment.html'
    form_class = CommentForm
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy("view_comment", kwargs={"pk": self.object.pk})


class DeletedComment(TemplateView):
    comment_deleted = True
    template_name = "articles/_comment.html"

    def __init__(self, *args, **kwargs):
        super().__init__(
            content_type="text/html; turbo-stream; charset=utf-8", *args, **kwargs
        )


class DeleteComment(UserIsAuthorMixin, LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "articles/_comment_confirm_delete.html"
    context_object_name = "comment"

    def get_success_url(self):
        return reverse_lazy("deleted_comment", kwargs={"pk": self.object.pk})


class ListArticle(ListView):
    template_name = "articles/list.html"
    paginate_by = 10
    model = Article

    def _make_tabs(self, ctx):
        tabs = []
        url = reverse_lazy("article_list")
        default_active = not any(
            [ctx.get(a) for a in ["followed_by", "favorited", "tag"]]
        )
        if ctx["profile"]:
            profile = ctx["profile"]
            tabs.append(
                {
                    "url": url + f"?profile={profile}",
                    "text": "My Articles",
                    "active": default_active,
                }
            )
            tabs.append(
                {
                    "url": url + f"?favorited={profile}&profile={profile}",
                    "text": "Favorited Articles",
                    "active": ctx.get("favorited") is not None,
                }
            )
        else:
            if self.request.user.is_authenticated:
                tabs.append(
                    {
                        "url": url + f"?followed_by={self.request.user}",
                        "text": "Your Feed",
                        "active": ctx.get("followed_by") is not None,
                    }
                )
            tabs.append(
                {
                    "url": url,
                    "text": "Global",
                    "active": default_active,
                }
            )
            if ctx.get("tag"):
                tabs.append(
                    {
                        "url": url + f'?tag={ctx.get("tag").slug}',
                        "text": ctx.get("tag"),
                        "active": ctx.get("tag") is not None,
                    }
                )
        return tabs

    def _get_query_context(self):
        ctx = {
            "tag": None,
            "query_string": [],
            "profile": None,
            "author": None,
            "favorited": None,
            "followed_by": None,
            "type": None,
            "tabs": [],
        }

        tag_slug = self.request.GET.get("tag")
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            ctx["tag"] = tag
            ctx["query_string"].append(f"tag={tag_slug}")

        profile = self.request.GET.get("profile")
        if profile:
            ctx["profile"] = profile
            ctx["query_string"].append(f"profile={profile}")

        favorited = self.request.GET.get("favorited")
        if favorited:
            ctx["favorited"] = favorited
            ctx["query_string"].append(f"favorited={favorited}")

        followed_by = self.request.GET.get("followed_by")
        if followed_by:
            ctx["followed_by"] = followed_by
            ctx["query_string"].append(f"followed_by={followed_by}")

        ctx["query_string"] = "&".join(ctx["query_string"])
        ctx["tabs"] = self._make_tabs(ctx)
        return ctx

    def get_queryset(self):
        qs = (
            Article.objects.all()
            .select_related("author__user")
            .annotate(favorited_by__count=Count("favorited_by"))
            .order_by("-created_at")
        )
        ctx = self._get_query_context()
        if tag := ctx["tag"]:
            qs = qs.filter(tags__slug=tag.slug)

        if profile := ctx["profile"]:
            qs = qs.filter(author__user__username=profile)

        if favorited := ctx["favorited"]:
            qs = qs.filter(favorited_by__user__username=favorited)

        if favorited := ctx["followed_by"]:
            # FIXFIX get articles by author the user follows
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
