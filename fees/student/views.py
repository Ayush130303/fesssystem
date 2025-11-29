import requests
import time
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from api.models import User, Students, FeeStructure, FeePayment, Announcement
from django.utils import timezone

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        email = request.POST.get("Email")
        roll_no = request.POST.get("roll_no")
        course = request.POST.get("course")
        semester = request.POST.get("semester")

        if password != password1:
            return render(request, "register.html", {"error": "Passwords do not match!"})

        user_payload = {
            "username": username,
            "password": password,
            "email": email,
            "role": "student"
        }

        user_res = requests.post(f"{settings.API_BASE_URL}/users/", json=user_payload)
        if user_res.status_code != 201:
            return render(request, "register.html", {"error": "User creation failed!"})

        user_id = user_res.json().get("id")

        student_payload = {
            "user_id": user_id,
            "roll_no": roll_no,
            "course": course,
            "semester": semester
        }

        student_res = requests.post(f"{settings.API_BASE_URL}/students/", json=student_payload)
        if student_res.status_code != 201:
            print(student_res.status_code, student_res.text)  # Debug
            return render(request, "register.html", {"error": f"Student profile creation failed! {student_res.text}"})

        return redirect("login")

    return render(request, "register.html")

from rest_framework.authtoken.models import Token

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, "login.html", {"error": "Invalid username or password!"})

        login(request, user)

        # Get or create DRF token
        token, created = Token.objects.get_or_create(user=user)
        request.session["access_token"] = token.key

        return redirect("dash")

    return render(request, "login.html")

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def dash(request):
    if request.user.is_superuser:
        return render(request, "ad_dash.html")

    token = request.session.get("access_token")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Token {token}"

    try:
        response = requests.get(f"{settings.API_BASE_URL}/announcements/", headers=headers)
        if response.status_code == 200:
            announcements = response.json()
        else:
            announcements = []
    except Exception as e:
        print("Error fetching announcements:", e)
        announcements = []

    return render(request, "dashboard.html", {"announcements": announcements})


def user_logout(request):
    logout(request)
    return redirect("dash")


def feestru(request):
    return render(request, "feestruc.html")


def updateprof(request, pk):
    user = get_object_or_404(User, pk=pk)
    student = get_object_or_404(Students, user=user)

    if request.method == 'POST':
        token = request.session.get("access_token")
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Token {token}"

        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        user_payload = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email")
        }

        if password:
            if password == password1:
                user_payload["password"] = password
            else:
                return render(request, "update.html", {"error": "Passwords do not match!", "user": user, "student": student})

        user_res = requests.patch(f"{settings.API_BASE_URL}/users/{pk}/", json=user_payload, headers=headers)

        student_payload = {
            "course": request.POST.get("course"),
            "semester": request.POST.get("semester")
        }

        student_res = requests.patch(f"{settings.API_BASE_URL}/students/{student.id}/", json=student_payload, headers=headers)

        if user_res.status_code == 200 and student_res.status_code == 200:
            return redirect("dash")

        return render(request, "update.html", {"error": "Update failed!", "user": user, "student": student})

    return render(request, "update.html", {"user": user, "student": student})


def payment(request, pk):
    user = get_object_or_404(User, pk=pk)
    student = get_object_or_404(Students, user=user)
    return render(request, 'payement.html', {"student": student})


def paygateway(request):
    roll = request.POST.get("rollno")
    ishostel = request.POST.get("hostel")
    cat = request.POST.get("feeCategory")

    user = request.user
    student = get_object_or_404(Students, user=user)

    try:
        fee = FeeStructure.objects.get(fee_id=cat)
        amount = fee.amount
    except FeeStructure.DoesNotExist:
        amount = 0

    if ishostel == "Yes":
        amount += 7500

    return render(request, "gateway.html", {"amount": amount, "student": student})

from django.core.mail import send_mail
@login_required(login_url='login')
def paystatus(request):
    if request.method == "POST":
        user = request.user
        student = get_object_or_404(Students, user=user)

        mode = request.POST.get("mode")
        amount = float(request.POST.get("amount"))
        transaction_id = f"TXN{int(time.time())}{random.randint(1000,9999)}"

        payment = FeePayment.objects.create(
            student=student,
            amount_paid=amount,
            mode=mode,
            transaction_id=transaction_id,
            payment_date=timezone.now()
        )

        api_payload = {
            "student": student.id,
            "amount_paid": amount,
            "mode": mode,
            "transaction_id": transaction_id
        }

        token = request.session.get("access_token")
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Token {token}"

        response = requests.post(
            f"{settings.API_BASE_URL}/fee-payments/",
            json=api_payload,
            headers=headers
        )

        if response.status_code in [200, 201]:
            send_mail(
                subject="Payment Successful",
                message=(
                    f"Dear {user.username},\n\n"
                    f"Your payment of ₹{amount} via {mode} was successful.\n"
                    f"Transaction ID: {transaction_id}\n"
                    f"Date: {payment.payment_date.strftime('%d-%m-%Y %I:%M %p')}\n\n"
                    "Thank you."
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[student.user.email],
                fail_silently=False,
            )

        return render(request, "paystatus.html", {
            "payment": payment,
            "api_result": response.json()
        })

    return render(request, "gateway.html")