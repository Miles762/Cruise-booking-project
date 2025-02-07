# Generated by Django 5.1.3 on 2024-12-02 20:36

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Port",
            fields=[
                (
                    "port_id",
                    models.SmallIntegerField(
                        help_text="Unique identifier for each port",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(help_text="Name of the port", max_length=30)),
                (
                    "state",
                    models.CharField(
                        help_text="State where the port is located", max_length=30
                    ),
                ),
                (
                    "country",
                    models.CharField(
                        help_text="Country where the port is located", max_length=30
                    ),
                ),
                (
                    "street_address",
                    models.CharField(
                        help_text="Street address of the port", max_length=30
                    ),
                ),
                (
                    "zip_code",
                    models.CharField(
                        help_text="ZIP or postal code of the port location",
                        max_length=6,
                    ),
                ),
                (
                    "nearest_airport_name",
                    models.CharField(
                        help_text="Nearest airport to the port", max_length=30
                    ),
                ),
                (
                    "number_of_parking_spots",
                    models.SmallIntegerField(
                        help_text="Number of parking spots available at the port"
                    ),
                ),
            ],
            options={
                "verbose_name": "Port",
                "verbose_name_plural": "Ports",
                "db_table": "ssh_port",
            },
        ),
    ]
