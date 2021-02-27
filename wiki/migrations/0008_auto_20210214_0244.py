# Generated by Django 3.1.6 on 2021-02-14 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0007_wikidisease_causes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikicasefatalityrate',
            name='frequency_int',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='wikideath',
            name='frequency_int',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='wikifrequency',
            name='frequency_int',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='wikimortalityrate',
            name='frequency_int',
            field=models.BigIntegerField(null=True),
        ),
    ]