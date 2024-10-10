from django.contrib import admin
from .models import CardOne, CardTwo



@admin.register(CardOne)
class CardOneAdmin(admin.ModelAdmin):
    list_display = ('id', 'image1', 'title', 'description')

@admin.register(CardTwo)
class CardTwoAdmin(admin.ModelAdmin):
    list_display = ('id', 'image2', 'title2', 'description')
