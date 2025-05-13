# blog/management/commands/seed_posts.py
from django.core.management.base import BaseCommand
from faker import Faker
from blog.models import Category, Post
from django.utils import timezone
import random
import requests
from io import BytesIO
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'Seeds the database with 25 random blog posts and random images'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create some categories if they don’t exist
        categories = ['Tech', 'Health', 'Travel', 'Lifestyle', 'Education']
        category_objs = []

        for cat in categories:
            obj, created = Category.objects.get_or_create(name=cat)
            category_objs.append(obj)

        # Create 25 fake posts
        for _ in range(25):
            # Fetch a random image from Lorem Picsum
            image_url = f"https://picsum.photos/800/600?random={random.randint(1, 1000)}"
            response = requests.get(image_url)
            image_content = BytesIO(response.content)
            image_name = f"post_images/{random.randint(1, 10000)}.jpg"  # Random name for the image file

            # Create the Post object with the random image
            post = Post.objects.create(
                post_title=fake.sentence(nb_words=6),
                description=fake.paragraph(nb_sentences=5),
                image=ContentFile(image_content.read(), image_name),
                create_date=timezone.now(),
                category=random.choice(category_objs)
            )

        self.stdout.write(self.style.SUCCESS('✔️ 25 random posts with images created.'))
