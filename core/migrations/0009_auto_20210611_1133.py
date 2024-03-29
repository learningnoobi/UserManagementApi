# Generated by Django 3.2.3 on 2021-06-11 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(default='Viewer', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.role', to_field='name'),
        ),
    ]
