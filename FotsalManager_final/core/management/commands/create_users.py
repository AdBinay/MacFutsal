from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from users.models import Batch
import random

class Command(BaseCommand):
    help = 'Create Random Batches for testing purpose'

    def handle(self, *args, **options):
        data = [
            {
            "first_name":"Ravi",
            "last_name":"Sankar",
            "username" : "hacker32@gmail.com",
            },
            {
            "first_name":"Trishana",
            "last_name":"Lamshal",
            "username" : "lamshal321@gmail.com",
            },
            {
            "first_name":"Roshan",
            "last_name":"Gaire",
            "username" : "gaire25@gmail.com",
            },
            {
            "first_name":"Gamer",
            "last_name":"Angel",
            "username" : "anjel899@gmail.com",
            },
            {
            "first_name":"Amrit",
            "last_name":"Bhattrai",
            "username" : "bhattrai241@gmail.com",
            },
            {
            "first_name":"Tej",
            "last_name":"Gurung",
            "username" : "grg234@gmail.com",
            },
            {
            "first_name":"Mahesh",
            "last_name":"Limbu",
            "username" : "maheshlimbu31@gmail.com",
            },
            {
            "first_name":"Arjun",
            "last_name":"Nepali",
            "username" : "nepaliarjun67@gmail.com",
            },
        ]

        for user_data in data:
            user , _  = User.objects.get_or_create(**user_data)
            user.set_password("newcome")
            user.save()
            user.profile.batch = random.choice(Batch.objects.all())
            user.profile.save()
            print(user_data["first_name"],"created.")