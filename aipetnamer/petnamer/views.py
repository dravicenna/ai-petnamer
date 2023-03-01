import os

import openai
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from tenacity import (retry, stop_after_attempt,  # for exponential backoff
                      wait_random_exponential)

from .forms import PetNameGeneratorForm
from .models import PetNameGenerator

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


def get_ip(request: HttpRequest) -> str:
    """Extract client IP from request."""
    x_forwarded_for = request.headers.get("X-Forwarded-For", "")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR", "")


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_names_from_dict(**data):
    if data.get('historical_themes') != 'none':
        prompt = f"Generate 10 pet name suggestions for a {data.get('pet_type')} with {data.get('color')} fur and a {data.get('personality_traits')} personality. The name should be {data.get('gender')}-specific and inspired by {data.get('historical_themes')}:\n\n"  # noqa
    else:
        prompt = f"Generate 10 pet name suggestions for a {data.get('pet_type')} with {data.get('color')} fur and a {data.get('personality_traits')} personality. The name should be {data.get('gender')}-specific:\n\n"  # noqa
    # Make the API request
    response = openai.Completion.create(prompt=prompt, **API_PARAM)

    return response["choices"][0]["text"]


@csrf_exempt
def generate_names(request):
    if request.method == 'POST':
        form = PetNameGeneratorForm(request.POST)
        if form.is_valid():
            pet_name_generator_obj = PetNameGenerator(**form.cleaned_data)
            pet_name_generator_obj.request_ip = get_ip(request)
            previous_gen = PetNameGenerator.objects.filter(slug=pet_name_generator_obj.to_slug()).first()
            if previous_gen and previous_gen.result != 'Error':
                return JsonResponse({"names": previous_gen.result})
            try:
                pet_name_generator_obj.result = generate_names_from_dict(**form.cleaned_data)
            except BaseException as e:
                print(e)
                pet_name_generator_obj.result = 'Error'
            pet_name_generator_obj.save()
            return JsonResponse({"names": pet_name_generator_obj.result})


def home(request):
    return render(request, 'home.html', context={'form': PetNameGeneratorForm()})
