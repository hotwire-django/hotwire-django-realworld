from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from random_username.generate import generate_username
from essential_generators import DocumentGenerator
from articles.models import Article, Comment, Tag
import string
import random
from articles.forms import make_slug


tags = [
    ("Radical Red", "radicalred"),
    ("Wild Watermelon", "wildwatermelon"),
    ("Outrageous Orange", "outrageousorange"),
    ("Atomic Tangerine", "atomictangerine"),
    ("Neon Carrot", "neoncarrot"),
    ("Sunglow", "sunglow"),
    ("Laser Lemon", "laserlemon"),
    ("Unmellow Yellow", "unmellowyellow"),
    ("Electric Lime", "electriclime"),
    ("Screamin' Green", "screamingreen"),
    ("Magic Mint", "magicmint"),
    ("Blizzard Blue", "blizzardblue"),
    ("Shocking Pink", "shockingpink"),
    ("Razzle Dazzle Rose", "razzledazzlerose"),
    ("Hot Magenta", "hotmagenta"),
    ("Purple Pizzazz", "purplepizzazz"),
]


class Command(BaseCommand):
    help = "Generates users, articles, tag, follows and comments."
    article_upper_bound = 5
    follows_upper_bounds = 10
    favorties_upper_bounds = 10
    password = "turbodjango"

    def add_arguments(self, parser):
        parser.add_argument("num_users", type=int)

    def handle(self, *args, **options):
        Tag.objects.bulk_create(
            [Tag(tag=t[0], slug=t[1]) for t in tags], ignore_conflicts=True
        )
        names = generate_username(int(options["num_users"]))
        User = get_user_model()
        users = [
            User.objects.create_user(username=n, password=self.password) for n in names
        ]
        print(users)
        gen = DocumentGenerator()
        gen.init_word_cache(5000)
        gen.init_sentence_cache(5000)
        for user in users:
            user = User.objects.get(username=user.username)
            user.profile.bio = gen.sentence()
            user.profile.save()
            articles = Article.objects.bulk_create(
                [
                    Article(
                        slug=make_slug(gen.sentence()),
                        title=gen.sentence(),
                        description=gen.sentence(),
                        body=gen.paragraph(),
                        author=user.profile,
                    )
                    # Make sure every user has at least 1 article
                    for _ in range(random.randrange(1, self.article_upper_bound))
                ]
            )
            print(articles)
            # Make sure every article has 1 tag, could add more later
            for article in articles:
                article.tags.add(Tag.objects.get(slug=random.choice(tags)[1]))
        self.stdout.write(self.style.SUCCESS(f"Created {len(users)} users"))
