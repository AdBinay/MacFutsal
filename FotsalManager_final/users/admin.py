from django.contrib import admin
from .models import Profile,Batch

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ["id","name"]
    search_fields = ["name"]

@admin.register(Profile)
class ProfileUser(admin.ModelAdmin):
    list_display = ['id','user']
    search_fields = ['user__first_name','user__last_name']

