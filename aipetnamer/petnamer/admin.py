from django.contrib import admin

from .models import PetNameGenerator


@admin.register(PetNameGenerator)
class PetNameGeneratorAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'request_ip',
        'pet_type',
        'gender',
        'color',
        'origin',
        'personality_traits',
        'historical_themes',
        'slug',
        'result',
    )
    search_fields = ('created_at', 'request_ip')
    ordering = ('-created_at',)
    list_filter = ('request_ip',)
