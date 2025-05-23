# Generated by Django 5.1.4 on 2025-04-07 10:05

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField(verbose_name='Kitob narxi')),
                ('quantity', models.IntegerField(verbose_name='Kitob soni')),
                ('image', models.ImageField(upload_to='media/', verbose_name='Kitob rasmi')),
                ('description', models.TextField(verbose_name='Kitob tavsifi')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Yaratilgan sana')),
                ('isDeleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField()),
                ('category', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
            ],
        ),
        migrations.CreateModel(
            name='reference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('description', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cost_name_references', to='home.book_model')),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('description', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('sold_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Income_category_references', to='home.book_model')),
            ],
        ),
        migrations.AddField(
            model_name='book_model',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_category_references', to='home.reference', verbose_name='Kitob turi'),
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sale_date', models.DateTimeField(default=datetime.datetime.now)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='home.product')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('balance', models.FloatField(default=0)),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.gender')),
            ],
        ),
        migrations.CreateModel(
            name='staff_payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Staff_work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_work', models.IntegerField()),
                ('price', models.FloatField()),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.staff')),
            ],
        ),
    ]
