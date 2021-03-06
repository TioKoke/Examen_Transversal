# Generated by Django 4.0.5 on 2022-07-07 17:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('WebCaosNews', '0005_alter_categoria_imagen_alter_noticia_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticia',
            name='nombre_usu',
            field=models.CharField(default='--', max_length=100),
        ),
        migrations.AddField(
            model_name='noticia',
            name='register_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(default='--', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(default='--', max_length=100),
        ),
    ]
