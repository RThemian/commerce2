# Generated by Django 4.1.7 on 2023-04-29 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_created_at_product_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Watches', 'Watches'), ('Nature Photography', 'Nature Photography'), ('Clothes', 'Clothes')], default='Nature Photography', max_length=255),
        ),
    ]
