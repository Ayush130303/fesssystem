from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from api.models import *
from django.contrib.auth import logout
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

        
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already taken!"})

        
        if Students.objects.filter(roll_no=roll_no).exists():
            return render(request, "register.html", {"error": "Roll No already registered!"})

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role="student"
        )

        student = Students.objects.create(
            user=user,
            roll_no=roll_no,
            course=course,
            semester=semester
        )

        return redirect("login")

    return render(request, "register.html")


from django.contrib.auth import authenticate,login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "login.html", {"error": "Invalid username or password!"})

        # valid login
        login(request, user)   # create session

        # redirect based on role
        # if user.role == "admin":
        #     return redirect("admin_dashboard")   # replace with your admin URL name
        # elif user.role == "student":
        #     return redirect("student_dashboard") 
        # else:
        #     return redirect("home")
        return redirect("dash")

    return render(request, "login.html")

def dash(request):
    return render(request,"dashboard.html")

def user_logout(request):
    logout(request)
    return redirect('dash')

def feestru(request):
    return render(request,"feestruc.html")

from django.shortcuts import render, get_object_or_404
def updateprof(request, pk):
    user = get_object_or_404(User, pk=pk)
    student = get_object_or_404(Students, user=user)

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        email = request.POST.get("email")
        course = request.POST.get("course")
        semester = request.POST.get("semester")
        profile = request.FILES.get("profile")

        if password and password1:
            if password != password1:
                return render(request, "update.html", {"error": "Passwords do not match!", "user": user, "student": student})
            user.password = make_password(password)

        user.username = username
        user.email = email
        user.save()

        student.course = course
        student.semester = semester
        if profile:
            student.profile = profile
        student.save()

        return redirect("dash")

    return render(request, "update.html", {"user": user, "student": student})



