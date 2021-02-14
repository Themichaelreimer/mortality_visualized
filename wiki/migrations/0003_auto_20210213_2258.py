# Generated by Django 3.1.6 on 2021-02-13 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0002_auto_20210208_0151'),
    ]

    operations = [
        migrations.CreateModel(
            name='WikiCause',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='WikiSpecialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='infobox',
        ),
        migrations.AddField(
            model_name='article',
            name='disease',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wiki.wikidisease'),
        ),
        migrations.AddField(
            model_name='article',
            name='first_sentence',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='wikidisease',
            name='other_names',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wikicasefatalityrate',
            name='region_name',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='wikideath',
            name='region_name',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='wikifrequency',
            name='region_name',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='wikimortalityrate',
            name='region_name',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
        migrations.DeleteModel(
            name='Infobox',
        ),
        migrations.AddField(
            model_name='wikidisease',
            name='specialty',
            field=models.ManyToManyField(to='wiki.WikiSpecialty'),
        ),
    ]
