# Generated by Django 5.1 on 2024-08-29 04:54

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(default=uuid.uuid4, editable=False, unique=True, verbose_name='slug')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='data de atualização')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='data de criação')),
                ('category', models.CharField(max_length=60, verbose_name='categoria')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='quantia')),
                ('genre', models.CharField(choices=[('EX', 'Despesa'), ('RV', 'Receita')], max_length=7, verbose_name='gênero')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.account', verbose_name='conta')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
