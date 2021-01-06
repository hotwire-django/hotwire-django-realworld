from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from random_username.generate import generate_username
from essential_generators import DocumentGenerator
from articles.models import Article, Comment, Tag
from profiles.models import Profile
import random


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
    help = "Generates users, posts and comments."
    article_upper_bound = 2
    follows_upper_bounds = 2
    favorties_upper_bounds = 2

    def add_arguments(self, parser):
        parser.add_argument("num_users", type=int)

    def handle(self, *args, **options):
        tag_objects = Tag.objects.bulk_create(
            [Tag(tag=t[0], slug=t[1]) for t in tags], ignore_conflicts=True
        )
        names = generate_username(int(options["num_users"]))
        User = get_user_model()
        users = User.objects.bulk_create(
            [User(username=n, password="turbodjango") for n in names]
        )
        print(users)
        for user in users:
            gen = DocumentGenerator()
            user = User.objects.get(username=user.username)
            profile = Profile.objects.create(user=user, bio=gen.sentence())

            articles = Article.objects.bulk_create(
                [
                    Article(
                        slug=gen.slug().replace(".", ""),
                        title=gen.sentence(),
                        description=gen.sentence(),
                        body=gen.paragraph(),
                        author=profile,
                    )
                    for _ in range(random.randrange(1, self.article_upper_bound))
                ]
            )
            print(articles)
            for article in articles:
                article.tags.add(Tag.objects.get(slug=random.choice(tags)[1]))

        # for poll_id in options["poll_ids"]:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()

        #     self.stdout.write(
        #         self.style.SUCCESS('Successfully closed poll "%s"' % poll_id)
        #     )
