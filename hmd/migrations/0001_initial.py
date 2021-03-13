# Generated by Django 3.0.8 on 2021-03-07 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='LifeTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(choices=[('m', 'm'), ('f', 'f'), ('a', 'a')], default='a', max_length=1)),
                ('age', models.IntegerField()),
                ('probability', models.DecimalField(decimal_places=5, max_digits=10)),
                ('cumulative_probability', models.DecimalField(decimal_places=5, max_digits=10)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hmd.Country')),
            ],
        ),
        migrations.CreateModel(
            name='CountryBirths',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(choices=[('m', 'm'), ('f', 'f'), ('a', 'a')], default='a', max_length=1)),
                ('population', models.IntegerField()),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hmd.Country')),
            ],
        ),
        migrations.CreateModel(
            name='CountryAgePopulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(choices=[('m', 'm'), ('f', 'f'), ('a', 'a')], default='a', max_length=1)),
                ('age', models.IntegerField()),
                ('population', models.IntegerField()),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hmd.Country')),
            ],
        ),
        migrations.CreateModel(
            name='CountryAgeDeaths',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(choices=[('m', 'm'), ('f', 'f'), ('a', 'a')], default='a', max_length=1)),
                ('age', models.IntegerField()),
                ('population', models.IntegerField()),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hmd.Country')),
            ],
        ),
    ]
