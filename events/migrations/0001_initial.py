# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-27 08:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import image_cropping.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_counter', models.IntegerField(default=0, editable=False, verbose_name='Visninger')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Publiseringsdato')),
                ('last_changed_date', models.DateTimeField(auto_now=True, null=True, verbose_name='Redigeringsdato')),
                ('publication_date', models.DateTimeField(blank=True, null=True, verbose_name='Publikasjonstid')),
                ('published', models.NullBooleanField(default=True, help_text='Dato har høyere prioritet enn dette feltet.', verbose_name='Publisert')),
                ('short_name', models.CharField(blank=True, help_text='Brukes på steder hvor det ikke er plass til å skrive hele overskriften, for eksempel kalenderen.', max_length=20, null=True, verbose_name='kort navn')),
                ('organizer', models.CharField(blank=True, help_text='Den som står bak arrangementet', max_length=100, verbose_name='organisert av')),
                ('location', models.CharField(max_length=100, verbose_name='sted')),
                ('event_start', models.DateTimeField(null=True, verbose_name='start')),
                ('event_end', models.DateTimeField(blank=True, null=True, verbose_name='slutt')),
                ('facebook_url', models.CharField(blank=True, help_text='URL-en til det tilsvarende arrangementet på Facebook', max_length=100, verbose_name='facebook-url')),
                ('registration_required', models.BooleanField(default=False, verbose_name='påmelding')),
                ('registration_deadline', models.DateTimeField(blank=True, null=True, verbose_name='påmeldingsfrist')),
                ('registration_start', models.DateTimeField(blank=True, null=True, verbose_name='påmelding åpner')),
                ('deregistration_deadline', models.DateTimeField(blank=True, null=True, verbose_name='avmeldingsfrist')),
                ('places', models.PositiveIntegerField(blank=True, null=True, verbose_name='antall plasser')),
                ('has_queue', models.NullBooleanField(help_text='Om ventelisten er på, vil det være mulig å melde seg på selv om arrangementet er fullt. De som er i ventelisten vil automatisk bli påmeldt etter hvert som plasser blir ledige.', verbose_name='har venteliste')),
                ('headline', models.CharField(blank=True, max_length=100, verbose_name='tittel')),
                ('lead_paragraph', models.TextField(blank=True, help_text='Vises på forsiden og i artikkelen', verbose_name='ingress')),
                ('body', models.TextField(blank=True, help_text='Vises kun i artikkelen. Man kan her bruke <a href="http://en.wikipedia.org/wiki/Markdown" target="_blank">markdown</a> for å formatere teksten.', verbose_name='brødtekst')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('event_picture', models.ImageField(blank=True, help_text='Bilder som er større enn 1000x400 px ser best ut. Du kan beskjære bildet etter opplasting.', null=True, upload_to='uploads/event_pictures', verbose_name='Arrangementbilde')),
                ('event_cropping', image_cropping.fields.ImageRatioField('event_picture', '1000x400', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='Beskjæring')),
                ('front_picture', models.ImageField(blank=True, help_text='Bilder som er større enn 250x250 px og er kvadratiske ser best ut. Du kan beskjære bildet etter opplasting.', null=True, upload_to='uploads/front_page_pictures', verbose_name='Forsidebilde')),
                ('front_cropping', image_cropping.fields.ImageRatioField('front_picture', '250x250', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='Beskjæring')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_created', to=settings.AUTH_USER_MODEL, verbose_name='Opprettet av')),
                ('last_changed_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_edited', to=settings.AUTH_USER_MODEL, verbose_name='Endret av')),
                ('open_for', models.ManyToManyField(blank=True, help_text='Hvilke grupper som får lov til å melde seg på arrangementet. Hvis ingen grupper er valgt er det åpent for alle.', to='auth.Group', verbose_name='Åpen for')),
            ],
            options={
                'verbose_name': 'arrangement',
                'verbose_name_plural': 'arrangement',
                'db_table': 'content_event',
                'permissions': (('administer', 'Can administer models'),),
            },
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Påmeldingsdato')),
                ('number', models.PositiveIntegerField(blank=True, help_text='Kønummer som tilsvarer plass på ventelisten/påmeldingsrekkefølge.', null=True, verbose_name='kønummer')),
                ('attending', models.BooleanField(default=True, help_text='Hvis denne er satt til sann har man en plass på arrangementet ellers er det en ventelisteplass.', verbose_name='har plass')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='bruker')),
            ],
            options={
                'verbose_name': 'påmelding',
                'verbose_name_plural': 'påmeldte',
                'db_table': 'content_eventregistration',
            },
        ),
    ]