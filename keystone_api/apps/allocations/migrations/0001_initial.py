# Generated by Django 4.2.7 on 2024-01-03 13:56

import apps.allocations.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_alter_researchgroup_admins_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=150, null=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField(max_length=1600)),
                ('submitted', models.DateField(auto_now=True, verbose_name='Submission Date')),
                ('approved', models.DateField(blank=True, null=True, verbose_name='Approval Date')),
                ('active', models.DateField(blank=True, null=True, verbose_name='Active Date')),
                ('expire', models.DateField(blank=True, null=True, verbose_name='Expiration Date')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.researchgroup')),
            ],
            bases=(apps.allocations.models.RGAffiliatedModel, models.Model),
        ),
        migrations.CreateModel(
            name='ProposalReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approve', models.BooleanField()),
                ('private_comments', models.CharField(blank=True, max_length=500, null=True)),
                ('public_comments', models.CharField(blank=True, max_length=500, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='allocations.proposal')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            bases=(apps.allocations.models.RGAffiliatedModel, models.Model),
        ),
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sus', models.PositiveIntegerField(verbose_name='Service Units')),
                ('final', models.PositiveIntegerField(blank=True, null=True, verbose_name='Final Usage')),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='allocations.cluster')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='allocations.proposal')),
            ],
            bases=(apps.allocations.models.RGAffiliatedModel, models.Model),
        ),
    ]
