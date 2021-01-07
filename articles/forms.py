from django.forms import ModelForm, Textarea, CharField, TextInput
from .models import Article
import random
import string


def make_slug(title):
    rnd = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    slug = title.lower().replace(" ", "-")
    allowed = string.ascii_lowercase + "-"
    return "".join([a for a in slug if a in allowed])[:20].strip(" -") + f"-{rnd}"


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ("title", "description", "body")
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
            # "tags": TextInput(
            #     attrs={
            #         "class": "form-control form-control-lg",
            #         "placeholder": "Enter tags",
            #     }
            # ),
        }

    def save(self, user):
        if not self.instance.pk:
            self.instance.author = user.profile
            self.instance.slug = make_slug(self.instance.title)

        return super().save()
