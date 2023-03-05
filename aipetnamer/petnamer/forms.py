from django import forms

from .models import PetNameGenerator


class PetNameGeneratorForm(forms.ModelForm):
    class Meta:
        model = PetNameGenerator
        fields = ['pet_type', 'gender', 'color', 'origin', 'personality_traits', 'historical_themes']

    def clean_pet_type(self):
        pet_type = self.cleaned_data.get('pet_type')
        if not pet_type:
            raise forms.ValidationError("Please choose a pet type.")
        return pet_type

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Please choose a gender.")
        return gender

    def clean_color(self):
        color = self.cleaned_data.get('color')
        if not color:
            raise forms.ValidationError("Please choose a color.")
        return color

    def clean_origin(self):
        origin = self.cleaned_data.get('origin')
        if not origin:
            raise forms.ValidationError("Please choose a origin.")
        return origin

    def clean_personality_traits(self):
        personality_traits = self.cleaned_data.get('personality_traits')
        if not personality_traits:
            raise forms.ValidationError("Please enter at least one personality trait.")
        return personality_traits

    def clean_historical_themes(self):
        historical_themes = self.cleaned_data.get('historical_themes')
        if not historical_themes:
            raise forms.ValidationError("Please choose a historical theme.")
        return historical_themes
