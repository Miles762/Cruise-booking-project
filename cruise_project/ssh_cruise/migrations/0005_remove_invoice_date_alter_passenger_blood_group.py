# Generated by Django 5.1.3 on 2024-12-04 02:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ssh_cruise", "0004_sshcruise_sshpackageinfo_alter_invoice_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="invoice",
            name="date",
        ),
        migrations.AlterField(
            model_name="passenger",
            name="blood_group",
            field=models.CharField(max_length=5),
        ),
    ]
