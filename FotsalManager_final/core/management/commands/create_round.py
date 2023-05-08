from django.core.management.base import BaseCommand, CommandError
from futsal import models as futsal_model

class Command(BaseCommand):
    help = 'Create Random Batches for testing purpose'

    def handle(self, *args, **options):
        for batch_name in ["General Round","Semi Final","Final"]:
            futsal_model.GameRound.objects.get_or_create(name=f"{batch_name}")
            