# Generated by Django 4.1.7 on 2023-03-07 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PetNameGenerator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pet_type', models.CharField(choices=[('dog', 'Dog🐕'), ('cat', 'Cat'), ('rabbit', 'Rabbit'), ('fish', 'Fish'), ('horse', 'Horse'), ('hamster', 'Hamster')], default='Dog🐕', max_length=10)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('neutral', 'Gender Neutral')], default='Male', max_length=10)),
                ('color', models.CharField(choices=[('black', 'Black'), ('white', 'White'), ('brown', 'Brown'), ('gray', 'Gray'), ('red', 'Red'), ('orange', 'Orange'), ('yellow', 'Yellow'), ('green', 'Green'), ('blue', 'Blue'), ('purple', 'Purple'), ('pink', 'Pink'), ('multicolor', 'Multicolor')], default='Black', max_length=10)),
                ('origin', models.CharField(choices=[('English', 'English'), ('African', 'African'), ('Alaskan', 'Alaskan'), ('American', 'American'), ('Chinese', 'Chinese'), ('Hebrew', 'Hebrew'), ('Latin', 'Latin'), ('Hindu', 'Hindu'), ('Mexican', 'Mexican'), ('Eskimo', 'Eskimo'), ('Hispanic', 'Hispanic'), ('Native American', 'Native American'), ('Arabic', 'Arabic'), ('French', 'French'), ('Indian', 'Indian'), ('Australian', 'Australian'), ('German', 'German'), ('Irish', 'Irish'), ('Scottish', 'Scottish'), ('Biblical', 'Biblical'), ('Greek', 'Greek'), ('Italian', 'Italian'), ('Spanish', 'Spanish'), ('Celtic', 'Celtic'), ('Hawaiian', 'Hawaiian'), ('Japanese', 'Japanese')], default='English', max_length=16)),
                ('personality_traits', models.CharField(choices=[('friendly', 'Friendly'), ('playful', 'Playful'), ('energetic', 'Energetic'), ('intelligent', 'Intelligent'), ('loyal', 'Loyal'), ('curious', 'Curious'), ('affectionate', 'Affectionate'), ('independent', 'Independent'), ('calm', 'Calm'), ('protective', 'Protective')], default='Friendly', max_length=20)),
                ('historical_themes', models.CharField(choices=[('none', 'None'), ('ancient egypt', 'Ancient Egypt'), ('medieval europe', 'Medieval Europe'), ('renaissance italy', 'Renaissance Italy'), ('wild west', 'Wild West'), ('ancient china', 'Ancient China'), ('ancient greece and Rome', 'Ancient Greece and Rome')], default='None', max_length=30)),
                ('slug', models.SlugField(max_length=100)),
                ('result', models.TextField(blank=True)),
                ('request_ip', models.GenericIPAddressField(null=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
