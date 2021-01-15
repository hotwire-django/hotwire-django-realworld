
import random
import string

from django.forms import ModelForm, Textarea, CharField, TextInput

from .models import Article, Comment, Tag


def make_slug(title):
    rnd = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    slug = title.lower().replace(" ", "-")
    allowed = string.ascii_lowercase + "-"
    return "".join([a for a in slug if a in allowed])[:20].strip(" -") + f"-{rnd}"


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            "body": Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write a comment...",
                    "rows": 3,
                }
            )
        }


class ArticleForm(ModelForm):
    tags = CharField(
        widget=TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Enter tags"
            }
        )
    )

    class Meta:
        model = Article
        fields = ("title", "description", "body", "tags")
        widgets = {
            "title": TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Article Title",
                }
            ),
            "description": TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "What's this article about?",
                }
            ),
            "body": Textarea(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Write your article (in markdown)",
                    "rows": 8,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tags'].widget.format_value = self._format_tags_value

    def _format_tags_value(self, queryset):
        return ', '.join(
            self.instance.tags.values_list('tag', flat=True)
        )

    def clean_tags(self, *args, **kwargs):
        return [
            Tag.objects.get_or_create(
                tag=tag.strip(),
                defaults={'slug': make_slug(tag.strip())}
            )[0]
            for tag in self.cleaned_data['tags'].split(',')
        ]

    def save(self, user):
        if not self.instance.pk:
            self.instance.author = user.profile
            self.instance.slug = make_slug(self.instance.title)

        return super().save()
