from django.core.management.base import BaseCommand, CommandError
from users import models as user_model

class Command(BaseCommand):
    help = 'Create Random Batches for testing purpose'

    def handle(self, *args, **options):
        for batch_name in range(2069,2080):
            user_model.Batch.objects.get_or_create(name=f"{batch_name}")
            