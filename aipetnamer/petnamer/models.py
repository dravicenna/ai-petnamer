import os

import openai
from django.db import models
from django.http import HttpRequest
from django.utils.text import slugify
from dotenv import load_dotenv
from tenacity import (retry, stop_after_attempt,  # for exponential backoff
                      wait_random_exponential)

from .constants import (COLOR_CHOICES, GENDER_CHOICES,
                        HISTORICAL_THEMES_CHOICES, ORIGIN_CHOICES,
                        PERSONALITY_TRAITS_CHOICES, PET_TYPE_CHOICES)

MODEL = "text-davinci-003"
API_PARAM = {
    'engine': MODEL,
    'max_tokens': 100,
    'temperature': 0.8,
    'top_p': 1,
    # 'frequency_penalty': 0.28,
    # 'presence_penalty': 0.13,
}

# Define the API key
load_dotenv()  # take environment variables from .env.
openai.api_key = os.getenv('OPENAI_TOKEN')


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_names_from_dict(**data):
    if data.get('historical_themes') != 'none':
        prompt = f"Generate 10 pet name suggestions for a {data.get('pet_type')} with {data.get('color')} fur and a {data.get('personality_traits')} personality. The name should be {data.get('gender')}-specific and inspired by {data.get('historical_themes')}  and the name should be {data.get('origin')} origin:\n\n"  # noqa
    else:
        prompt = f"Generate 10 pet name suggestions for a {data.get('pet_type')} with {data.get('color')} fur and a {data.get('personality_traits')} personality. The name should be {data.get('gender')}-specific and the name should be {data.get('origin')} origin:\n\n"  # noqa
    # Make the API request
    response = openai.Completion.create(prompt=prompt, **API_PARAM)

    return response["choices"][0]["text"]


def get_ip(request: HttpRequest) -> str:
    """Extract client IP from request."""
    x_forwarded_for = request.headers.get("X-Forwarded-For", "")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR", "")


class PetManager(models.Manager):
    """Custom model manager for PetNameGenerator objects."""

    def _build_without_result(self, request: HttpRequest, formdata: dict):
        """Build a new PetNameGenerator object from a request and form data"""
        pg = PetNameGenerator(**formdata,
                              request_ip=get_ip(request),
                              )
        pg.slug = pg.to_slug()
        return pg

    def _save_with_result(self, pg, result):
        pg.result = result
        pg.save()

    def _last_generated(self, slug: str):
        return PetNameGenerator.objects.filter(slug=slug).first()

    def _process_and_return_result(self, request: HttpRequest, formdata: dict):
        pg = self._build_without_result(request, formdata)
        last_generated = self._last_generated(slug=pg.slug)

        if last_generated and last_generated.result != 'Error':
            result = last_generated.result
            self._save_with_result(pg, result)
            return result

        try:
            result = generate_names_from_dict(**formdata)
        except BaseException as e:
            print(e)
            result = 'Error'

        self._save_with_result(pg, result)
        return result

    def return_result(self, request: HttpRequest, formdata: dict):
        return self._process_and_return_result(request, formdata)


class PetNameGenerator(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    pet_type = models.CharField(max_length=10, choices=PET_TYPE_CHOICES, default=PET_TYPE_CHOICES[0][1])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=GENDER_CHOICES[0][1])
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default=COLOR_CHOICES[0][1])
    origin = models.CharField(max_length=16, choices=ORIGIN_CHOICES, default=ORIGIN_CHOICES[0][1])
    personality_traits = models.CharField(
        max_length=20, choices=PERSONALITY_TRAITS_CHOICES, default=PERSONALITY_TRAITS_CHOICES[0][1])
    historical_themes = models.CharField(
        max_length=30, choices=HISTORICAL_THEMES_CHOICES, default=HISTORICAL_THEMES_CHOICES[0][1])
    slug = models.SlugField(max_length=100)
    result = models.TextField(blank=True)
    request_ip = models.GenericIPAddressField(null=True)

    objects = PetManager()

    class Meta:
        ordering = ('-created_at',)

    def to_slug(self):
        str_to_slug = f'{self.pet_type}-{self.gender}-{self.color}-{self.origin}-{self.personality_traits}-{self.historical_themes}'  # noqa
        return slugify(str_to_slug)

    def save(self, *args, **kwargs):
        self.slug = self.to_slug()
        super(PetNameGenerator, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'Created at {self.created_at}'
