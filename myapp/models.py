from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager



# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_mediator',True)
        return self.create_user(email, password, **extra_fields)
    



class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    is_nurse = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)
    is_mediator = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    

class hospitalShiftDetails(models.Model):
    shiftID = models.AutoField(primary_key=True)
    hospital = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=40,default="open")

    def __str__(self):
        return self.hospital.first_name+"_"+self.hospital.last_name
    

class AppliedNurses(models.Model):
    applicationID=models.AutoField(primary_key=True)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    appliedShift = models.ForeignKey(hospitalShiftDetails, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    

    def __str__(self):
        return str(self.applicant.email)+"-"+str(self.appliedShift.shiftID)