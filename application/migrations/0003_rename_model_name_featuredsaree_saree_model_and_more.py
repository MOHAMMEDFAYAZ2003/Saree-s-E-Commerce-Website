# Generated by Django 5.1.4 on 2025-03-05 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_alter_featuredsaree_product_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='featuredsaree',
            old_name='model_name',
            new_name='saree_model',
        ),
        migrations.RenameField(
            model_name='saree',
            old_name='model_name',
            new_name='saree_model',
        ),
    ]
