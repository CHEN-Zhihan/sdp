# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-29 05:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('typeName', models.CharField(max_length=200)),
                ('content', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('_isOpen', models.BooleanField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('index', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Course')),
            ],
        ),
        migrations.CreateModel(
            name='SDPUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CompletedEnrollment',
            fields=[
                ('enrollment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='general.Enrollment')),
                ('completionDate', models.DateField()),
            ],
            bases=('general.enrollment',),
        ),
        migrations.CreateModel(
            name='CurrentEnrollment',
            fields=[
                ('enrollment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='general.Enrollment')),
                ('progress', models.IntegerField()),
            ],
            bases=('general.enrollment',),
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('sdpuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='general.SDPUser')),
            ],
            bases=('general.sdpuser',),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('sdpuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='general.SDPUser')),
                ('completed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='general.CompletedEnrollment')),
                ('current', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='general.CurrentEnrollment')),
            ],
            bases=('general.sdpuser',),
        ),
        migrations.AddField(
            model_name='sdpuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Course'),
        ),
        migrations.AddField(
            model_name='component',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Module'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Participant'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Instructor'),
        ),
    ]
