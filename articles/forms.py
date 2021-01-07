from django.forms import ModelForm, Textarea, CharField, TextInput
from .models import Article


class ArticleForm(ModelForm):
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
            # "tags": TextInput(
            #     attrs={
            #         "class": "form-control form-control-lg",
            #         "placeholder": "Enter tags",
            #     }
            # ),
        }
