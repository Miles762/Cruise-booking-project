from django.db import models


class Passenger(models.Model):
    passenger_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    street_address = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Stateroom(models.Model):
    stateroom_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=30)
    size = models.IntegerField()

    def __str__(self):
        return self.type


class Side(models.Model):
    side_id = models.AutoField(primary_key=True)
    side_name = models.CharField(max_length=30)

    def __str__(self):
        return self.side_name


class Package(models.Model):
    package_id = models.AutoField(primary_key=True)
    package_name = models.CharField(max_length=30)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.package_name


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    room_cost = models.DecimalField(max_digits=10, decimal_places=2)
    package_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice #{self.invoice_id}"


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_date = models.DateField(auto_now_add=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=30)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment #{self.payment_id}"

class SshTrSrS(models.Model):
    stateroom_id = models.IntegerField(primary_key=True)
    side_id = models.IntegerField()
    trip_id = models.CharField(max_length=5)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'ssh_tr_sr_s'
        managed = False  # Prevent Django from altering the database
