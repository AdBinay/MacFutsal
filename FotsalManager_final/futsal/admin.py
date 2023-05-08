from django.contrib import admin
from . import models
# Register your models here.

admin.site.register([
    models.Post,
    models.Players,
    models.Team,
    models.Coordinator,
    models.GameManager,
    models.Match
    ])