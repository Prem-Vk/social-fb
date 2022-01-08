# Generated by Django 2.2.25 on 2022-01-07 12:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], default='M', max_length=1)),
                ('email', models.EmailField(blank=True, max_length=200)),
                ('bio', models.TextField(default='no bio...', max_length=300)),
                ('country', models.CharField(blank=True, max_length=200)),
                ('birth_date', models.DateField(default=django.utils.timezone.now)),
                ('avatar', models.ImageField(default='avatar.png', upload_to='avatars/')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_status', models.CharField(choices=[('A', 'Accepted'), ('P', 'Pending')], max_length=10)),
                ('friend1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend1', to=settings.AUTH_USER_MODEL)),
                ('friend2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend2', to='loginAndRegistration.Profile', verbose_name='Friend Request accepted or pending')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='friends', through='loginAndRegistration.relation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='posts', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])])),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='loginAndRegistration.Profile')),
                ('liked', models.ManyToManyField(blank=True, related_name='likes', to='loginAndRegistration.Profile')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
