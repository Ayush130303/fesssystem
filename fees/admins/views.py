import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from api.models import Students
from django.contrib.auth import logout

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dash(request):
    return render(request, "ad_dash.html", {"year": timezone.now().year})

@login_required
@user_passes_test(is_admin)
def view_announcements(request):
    token = request.session.get("access_token")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Token {token}"

    response = requests.get(f"{settings.API_BASE_URL}/announcements/", headers=headers)
    announcements = response.json() if response.status_code == 200 else []

    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("message")
        payload = {"title": title, "body": body, "user": request.user.id}
        requests.post(f"{settings.API_BASE_URL}/announcements/", headers=headers, json=payload)
        return redirect("view-announcements")

    return render(request, "annoucemnet.html", {"announcements": announcements})

@login_required
@user_passes_test(is_admin)
def fee_structure(request):
    token = request.session.get("access_token")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Token {token}"

    response = requests.get(f"{settings.API_BASE_URL}/fee-structure/", headers=headers)
    fees = response.json() if response.status_code == 200 else []

    if request.method == "POST":
        fee_id=request.POST.get("fee_id")
        course = request.POST.get("course")
        semester = request.POST.get("semester")
        amount = request.POST.get("amount")
        payload = {"fee_id":fee_id,"course": course, "semester": semester, "amount": float(amount)}
        requests.post(f"{settings.API_BASE_URL}/fee-structure/", headers=headers, json=payload)
        return redirect("fee-structure")

    return render(request, "fee_struct.html", {"fees": fees})

from api.models import FeePayment 
@login_required
@user_passes_test(is_admin)
def fee_submissions(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')  # Ensure user is logged in

    if user.is_superuser:
        payments = FeePayment.objects.select_related('student').all().order_by('-payment_date')
    else:
        payments = FeePayment.objects.filter(student__user=user).select_related('student').order_by('-payment_date')

    return render(request, "feesub.html", {"payments": payments})

@login_required
@user_passes_test(is_admin)
def view_students(request):
    token = request.session.get("access_token")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Token {token}"

    response = requests.get(f"{settings.API_BASE_URL}/students/", headers=headers)
    students = response.json() if response.status_code == 200 else []

    return render(request, "studentlist.html", {"students": students})

@login_required
def admin_logout(request):
    logout(request)
    return redirect("login")
