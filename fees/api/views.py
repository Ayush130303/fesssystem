from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Students, FeeStructure, FeePayment
from .serializer import UserSerializer, StudentsSerializer, FeeStructureSerializer, FeePaymentSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer

class FeeStructureViewSet(viewsets.ModelViewSet):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer

class FeePaymentViewSet(viewsets.ModelViewSet):
    queryset = FeePayment.objects.all()
    serializer_class = FeePaymentSerializer
