# Generated by Django 4.2.4 on 2023-09-03 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_rename_wishlist_auctionlisting_favourite'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]
