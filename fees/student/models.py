# from django.db import models
# from api.models import User
# # Create your models here.
# class Students(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     roll_no=models.CharField(unique=True,max_length=10)
#     course=models.CharField(max_length=100)
#     semester=models.IntegerField()
#     profile=models.ImageField(upload_to="media/",default="media/prof.JPG")

#     def __str__(self):
#         return f"{self.user.username} - {self.roll_no}"
