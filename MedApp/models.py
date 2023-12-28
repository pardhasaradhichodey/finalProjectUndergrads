from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE

# Create your models here.
class User(models.Model):
    UserId=models.AutoField(primary_key=True)
    email=models.TextField(unique=True)
    name=models.TextField()
    phone=models.CharField(max_length=12)
    password=models.CharField(max_length=25)
    latitude=models.FloatField()
    longitude=models.FloatField()
class Beneficiary(models.Model):
    BenId=models.AutoField(primary_key=True)
    name=models.TextField()
    RelToUser=models.TextField()
    Age=models.IntegerField()
    Gender=models.TextField()
    UserId=models.ForeignKey(User,on_delete=models.CASCADE)
class DiagnosticCentre(models.Model):
    CentreId=models.AutoField(primary_key=True)
    email=models.TextField(unique=True)
    name=models.TextField()
    phone=models.CharField(max_length=12)
    password=models.CharField(max_length=25)
    latitude=models.FloatField()
    longitude=models.FloatField()
class Tests(models.Model):
    TestId=models.AutoField(primary_key=True)
    name=models.TextField()
    Description=models.TextField()
class TestsOffered(models.Model):
    TOId=models.AutoField(primary_key=True)
    CentreId=models.ForeignKey(DiagnosticCentre,on_delete=models.CASCADE)
    TestId=models.ForeignKey(Tests,on_delete=models.CASCADE)
    Price=models.IntegerField()
    TestsPerDay=models.IntegerField()
    class Meta:
        unique_together=('CentreId','TestId')
class Hospital(models.Model):
    email=models.TextField(unique=True)
    Hospital_name=models.TextField()
    phone=models.CharField(max_length=12)
    latitude=models.FloatField()
    longitude=models.FloatField()
    Gen_Beds=models.IntegerField()
    Bed_vent=models.IntegerField()
    Gen_Bed_price=models.IntegerField()
    Bed_Vent_price=models.IntegerField()
class Doctor(models.Model):
    DoctorId=models.AutoField(primary_key=True)
    email=models.TextField(unique=True)
    name=models.TextField()
    phone=models.CharField(max_length=12)
    password=models.CharField(max_length=25)
    Hospital_id=models.ForeignKey(Hospital,on_delete=CASCADE)
    patient_count_per_day=models.IntegerField()
    Consultation_fee=models.IntegerField()
class SlotBookAndReport(models.Model):
    SlotId=models.AutoField(primary_key=True)
    BeneId=models.ForeignKey(Beneficiary,on_delete=CASCADE)
    TestId=models.ForeignKey(TestsOffered,on_delete=CASCADE)
    DateOfTest=models.DateField()
    report=models.ImageField(upload_to='xrays/')
    status=models.BooleanField()
class DoctorConsult(models.Model):
    Opid=models.AutoField(primary_key=True)
    slotId=models.ForeignKey(SlotBookAndReport,on_delete=CASCADE)
    Doctor_Id=models.ForeignKey(Doctor,on_delete=CASCADE)
    ConsultDate=models.DateField()
class BedBook(models.Model):
    BedBookId=models.AutoField(primary_key=True)
    slotId=models.ForeignKey(SlotBookAndReport,on_delete=CASCADE)
    Hospital_Id=models.ForeignKey(Hospital,on_delete=CASCADE)
    TypeOfBed=models.TextField()
    StartDate=models.DateField()
    EndDate=models.DateField()
