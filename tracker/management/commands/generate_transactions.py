import random

from django.core.management.base import BaseCommand
from faker import Faker

from tracker.models import Category, Transaction, User


class Command(BaseCommand):
    help = "Generate Random Transactions"

    def handle(self, *args, **options):
        fake = Faker()

        categories = [
            "Food",
            "Bills",
            "Rent",
            "Salary",
            "Medical",
            "Social",
            "Transport",
            "Vacation",
        ]

        for category in categories:
            Category.objects.get_or_create(name=category)

        user = User.objects.filter(username="admin")

        if not user:
            user = User.objects.create_superuser(username="admin", password="admin")

        categories = Category.objects.all()
        types = [x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES]
        for i in range(20):
            Transaction.objects.create(
                user=User.objects.get(username="admin"),
                category=random.choice(categories),
                type=random.choice(types),
                amount=random.uniform(1, 2500),
                date=fake.date_between(start_date="-1y", end_date="today"),
            )
