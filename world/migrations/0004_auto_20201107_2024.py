# Generated by Django 3.1.2 on 2020-11-07 20:24
from django.db import migrations
import json
from django.contrib.gis.geos import fromstr
from pathlib import Path

DATA_FILE = 'data.json'

def load_data(apps, schema_editor):
    Pub = apps.get_model('world','Pub')
    jsonfile = Path(__file__).parents[2] / DATA_FILE

    with open(str(jsonfile), encoding="utf8") as datafile:
        objects = json.load(datafile)
        for object in objects['elements']:
            try:
                objectType = object['type']
                if objectType == 'node':
                    tags = object['tags']
                    name = tags.get('name', 'no-name')
                    longitude = object.get('lon', 0)
                    latitude = object.get('lat', 0)
                    location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
                    Pub(name=name,location=location).save()
            except KeyError:
                pass


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0003_pub'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]