from django.contrib import admin

from .models import PetNameGenerator


@admin.register(PetNameGenerator)
class PetNameGeneratorAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("pet_type", "gender", "color")}
    list_display = (
        'created_at',
        'request_ip',
        'pet_type',
        'gender',
        'color',
        'personality_traits',
        'historical_themes',
        'slug',
        'result',
    )
    search_fields = ('created_at', 'request_ip')
    ordering = ('-created_at',)
