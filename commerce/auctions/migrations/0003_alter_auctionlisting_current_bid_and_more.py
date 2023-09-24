# Generated by Django 4.2.4 on 2023-08-20 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlisting_alter_user_id_bids_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='current_bid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]