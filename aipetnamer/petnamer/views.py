
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import PetNameGeneratorForm
from .models import PetNameGenerator


@csrf_exempt
def generate_names(request: HttpRequest):
    if request.method == 'POST':
        form = PetNameGeneratorForm(request.POST)
        if form.is_valid():
            result = PetNameGenerator.objects.return_result(request, form.cleaned_data)
            return JsonResponse({"names": result})


def home(request: HttpRequest):
    return render(request, 'home.html', context={'form': PetNameGeneratorForm()})
