# Generated by Django 4.2.4 on 2023-09-06 23:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_delete_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='bids_registered',
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='starting_bid',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='bids',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.auctionlisting'),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='bids_registered',
            field=models.ManyToManyField(blank=True, related_name='listings', to='auctions.bids'),
        ),
    ]
