from django.db import models
from django.utils.text import slugify


class PetNameGenerator(models.Model):
    PET_TYPE_CHOICES = [
        ('dog', 'Dog🐕'),
        ('cat', 'Cat'),
        ('rabbit', 'Rabbit'),
        ('fish', 'Fish'),
        ('horse', 'Horse'),
        ('hamster', 'Hamster'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('neutral', 'Gender Neutral'),
    ]
    COLOR_CHOICES = [
        ('black', 'Black'),
        ('white', 'White'),
        ('brown', 'Brown'),
        ('gray', 'Gray'),
        ('red', 'Red'),
        ('orange', 'Orange'),
        ('yellow', 'Yellow'),
        ('green', 'Green'),
        ('blue', 'Blue'),
        ('purple', 'Purple'),
        ('pink', 'Pink'),
        ('multicolor', 'Multicolor'),
    ]
    PERSONALITY_TRAITS_CHOICES = [
        ('friendly', 'Friendly'),
        ('playful', 'Playful'),
        ('energetic', 'Energetic'),
        ('intelligent', 'Intelligent'),
        ('loyal', 'Loyal'),
        ('curious', 'Curious'),
        ('affectionate', 'Affectionate'),
        ('independent', 'Independent'),
        ('calm', 'Calm'),
        ('protective', 'Protective'),
    ]
    ORIGIN_CHOICES = [
        ('English', 'English'),
        ('African', 'African'),
        ('Alaskan', 'Alaskan'),
        ('American', 'American'),
        ('Chinese', 'Chinese'),
        ('Hebrew', 'Hebrew'),
        ('Latin', 'Latin'),
        ('Hindu', 'Hindu'),
        ('Mexican', 'Mexican'),
        ('Eskimo', 'Eskimo'),
        ('Hispanic', 'Hispanic'),
        ('Native American', 'Native American'),
        ('Arabic', 'Arabic'),
        ('French', 'French'),
        ('Indian', 'Indian'),
        ('Australian', 'Australian'),
        ('German', 'German'),
        ('Irish', 'Irish'),
        ('Scottish', 'Scottish'),
        ('Biblical', 'Biblical'),
        ('Greek', 'Greek'),
        ('Italian', 'Italian'),
        ('Spanish', 'Spanish'),
        ('Celtic', 'Celtic'),
        ('Hawaiian', 'Hawaiian'),
        ('Japanese', 'Japanese')
    ]
    HISTORICAL_THEMES_CHOICES = [
        ('none', 'None'),
        ('ancient egypt', 'Ancient Egypt'),
        ('medieval europe', 'Medieval Europe'),
        ('renaissance italy', 'Renaissance Italy'),
        ('wild west', 'Wild West'),
        ('ancient china', 'Ancient China'),
        ('ancient greece and Rome', 'Ancient Greece and Rome'),
    ]

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
        # return f'{self.pet_type}-{self.gender}-{self.color}'
