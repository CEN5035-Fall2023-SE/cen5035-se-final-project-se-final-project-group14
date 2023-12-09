from django.db import models

# Model for the "TaApplicant" entity
class TaApplicant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    z_number = models.CharField(max_length=10, unique=True)
    phn_number = models.CharField(max_length=15)
    dept = models.CharField(max_length=100)
    level = models.CharField(max_length=20)  # Use choices or ForeignKey for specific levels
    password=models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Model for the "DepartmentStaff" entity
class DepartmentStaff(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phn_number = models.CharField(max_length=15)
    password=models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Model for the "Instructor" entity
class Instructor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phn_number = models.CharField(max_length=15)
    password=models.CharField(max_length=100)
    def __str__(self):
        return self.name

# Model for the "TACoimmitteeMember" entity
class TACoimmitteeMember(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phn_number = models.CharField(max_length=15)
    password=models.CharField(max_length=100)
    def __str__(self):
        return self.name
