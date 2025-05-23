# Generated by Django 5.0.6 on 2024-09-01 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='carteirinha',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='data_nascimento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='documento',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='documento_responsavel',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='endereco',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nome_responsavel',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='telefone_contato',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='telefone_emergencia',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='telefone_responsavel',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
