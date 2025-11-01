from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    USER_ROLES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Students(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    roll_no=models.CharField(unique=True,max_length=10)
    course=models.CharField(max_length=100)
    semester=models.IntegerField()
    profile=models.ImageField(upload_to="media/",default="media/prof.JPG")

    def __str__(self):
        return f"{self.user.username} - {self.roll_no}"
    
class FeeStructure(models.Model):
    fee_id = models.CharField(max_length=20, null=False)
    semester = models.IntegerField()
    course = models.CharField(max_length=100)
    amount = models.FloatField()

    def __str__(self):
        return f"Semester {self.semester} - ₹{self.amount}"

class FeePayment(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='payments')
    fees = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.FloatField()
    payment_date = models.DateTimeField(default=timezone.now)
    mode = models.CharField(max_length=20)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Payment by {self.student.id} on {self.payment_date.strftime('%Y-%m-%d')}"

