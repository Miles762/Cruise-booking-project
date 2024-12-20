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

    class Meta:
        managed = False
        db_table = 'ssh_passenger'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Stateroom(models.Model):
    stateroom_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=30)
    size = models.IntegerField()
    number_of_bed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ssh_stateroom'

    def __str__(self):
        return self.type


class Side(models.Model):
    side_id = models.AutoField(primary_key=True)
    side_name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'ssh_sides'

    def __str__(self):
        return self.side_name


class SshTrSrS(models.Model):
    id = models.AutoField(primary_key=True)  # Primary key column
    stateroom_id = models.SmallIntegerField()  # Corresponds to `tinyint` in MySQL
    side_id = models.SmallIntegerField()       # Corresponds to `tinyint` in MySQL
    trip_id = models.CharField(max_length=5)   # Corresponds to `varchar(5)` in MySQL
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'ssh_tr_sr_s'
        #unique_together = ('stateroom_id', 'side_id', 'trip_id')  # Composite unique constraint

    def __str__(self):
        return f"ID: {self.id}, Stateroom: {self.stateroom_id}, Side: {self.side_id}, Trip: {self.trip_id}, Price: {self.price_per_night}"



# class SshTrSrS(models.Model):
    # stateroom_id = models.IntegerField(primary_key=True)
    # side_id = models.IntegerField()
    # trip_id = models.CharField(max_length=5)
    # price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    # stateroom_id = models.SmallIntegerField(primary_key=True)  # Corresponds to `tinyint` in MySQL
    # side_id = models.SmallIntegerField(primary_key=True)      # Corresponds to `tinyint` in MySQL
    # trip_id = models.CharField(max_length=5, primary_key=True)  # Corresponds to `varchar(5)` in MySQL
    # price_per_night = models.DecimalField(max_digits=8, decimal_places=2)  # Corresponds to `decimal(8,2)` in MySQL


    # class Meta:
    #     db_table = 'ssh_tr_sr_s'
    #     unique_together = ('stateroom_id', 'side_id', 'trip_id')  # This creates a composite unique constraint
    #     managed = False  # Ensures Django doesn't attempt to alter the table schema

    # def __str__(self):
    #     return f"{self.stateroom_id}-{self.side_id}-{self.trip_id}"



class Package(models.Model):
    package_id = models.AutoField(primary_key=True)
    package_name = models.CharField(max_length=30)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'ssh_packages'

    def __str__(self):
        return self.package_name


# class Invoice(models.Model):
#     invoice_id = models.AutoField(primary_key=True)
#     due_date = models.DateField()
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     room_cost = models.DecimalField(max_digits=10, decimal_places=2)
#     package_cost = models.DecimalField(max_digits=10, decimal_places=2)
#     Date = models.DateField()

#     class Meta:
#         managed = False
#         db_table = 'ssh_invoice'

#     def __str__(self):
#         return f"Invoice #{self.invoice_id}"

class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    Date = models.DateField()  # Date the invoice was issued
    due_date = models.DateField()  # Due date for payment
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total amount on the invoice
    payment_method = models.CharField(
        max_length=30, null=True, blank=True
    )  # Payment method (nullable)
    room_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # Cost of the room
    package_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # Cost of the package

    class Meta:
        managed = False  # The table is managed outside Django migrations
        db_table = "ssh_invoice"  # Explicit table name

    def __str__(self):
        return f"Invoice #{self.invoice_id}"

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    payment_date = models.DateField(auto_now_add=True)  # Automatically set payment date
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    payment_method = models.CharField(max_length=30)  # Payment method
    ssh_invoice_invoice_id = models.ForeignKey(
        Invoice,  # Reference to the Invoice model
        on_delete=models.CASCADE,  # Cascade deletes if the invoice is deleted
        db_column="ssh_invoice_invoice_id",  # Map to the database column name
    )

    class Meta:
        managed = True  # This table is managed by Django
        db_table = "ssh_payment"  # Explicit table name

    def __str__(self):
        return f"Payment #{self.payment_id} linked to Invoice #{self.ssh_invoice_invoice_id.invoice_id}"

# class Payment(models.Model):
#     payment_id=models.AutoField(primary_key=True)
#     #payment_id = models.AutoField(primary_key=True)
#     payment_date = models.DateField(auto_now_add=True)
#     payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_method = models.CharField(max_length=30)
#     ssh_invoice_invoice_id = models.ForeignKey(
#         'Invoice',  # Reference the Invoice model
#         on_delete=models.CASCADE,
#         db_column='ssh_invoice_invoice_id'  # Map to the database column name
#     ),#models.ForeignKey(Invoice, on_delete=models.CASCADE)

#     class Meta:
#         managed = True
#         db_table = 'ssh_payment'

#     def __str__(self):
#         return f"Payment #{self.payment_id}"


class SshCruise(models.Model):
    ssh_trip_trip_id = models.CharField(max_length=5)
    ssh_passenger_passenger_id = models.IntegerField()
    group_id = models.CharField(max_length=8)
    ssh_stateroom_stateroom_id = models.IntegerField()
    ssh_sides_side_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ssh_cruise'


class SshPackageInfo(models.Model):
    package_id = models.IntegerField()
    trip_id = models.CharField(max_length=5)
    passenger_id = models.IntegerField()
    group_id = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'ssh_package_info'
