# Generated by Django 5.1.7 on 2025-05-13 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0009_alter_order_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profileimg',
            field=models.ImageField(default='product_img/backimg.jpg', upload_to='product_img'),
        ),
    ]
