# Manually created on 2024-10-12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allocations', '0009_remove_allocationrequest_group'),
        ('research_products', '0003_remove_grant_group_remove_publication_group'),
        ('users', '0008_user_profile_image'),
    ]

    operations = [
        # "Research groups" have been renamed to "teams"
        migrations.RenameModel('ResearchGroup', 'Team'),

        # Teams have a new membership/role structure
        # Create a table for storing that structure
        migrations.CreateModel(
            name='TeamMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('OW', 'Owner'), ('AD', 'Admin'), ('MB', 'Member')], max_length=2)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'team')},
            },
        ),

        # Create relationships for the new table
        migrations.AddField(
            model_name='team',
            name='users',
            field=models.ManyToManyField(through='users.TeamMembership', to=settings.AUTH_USER_MODEL),
        ),

        # Move old user permissions to the new model
        migrations.RunSQL("""
            INSERT INTO users_teammembership (user_id, team_id, role) 
            SELECT pi_id, id, 'OW' 
            FROM users_team;
        """),
        migrations.RunSQL("""
            INSERT INTO users_teammembership (user_id, team_id, role)
            SELECT user_id, team_id, 'AD'
            FROM users_team_admins;
        """),
        migrations.RunSQL("""
            INSERT INTO users_teammembership (user_id, team_id, role)
            SELECT user_id, team_id, 'ME'
            FROM users_team_members;
        """),

        # Remove models/fields used to track the old permissions
        migrations.RemoveField(model_name='Team', name='pi'),
        migrations.RemoveField(model_name='Team', name='admins'),
        migrations.RemoveField(model_name='Team', name='members'),
    ]
