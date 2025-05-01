from django.shortcuts import render, redirect
import requests

API_BASE = "http://127.0.0.1:8000/api"

def home(request):
    return render(request, "home.html")

def signup_form(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
        }
        response = requests.post(f"{API_BASE}/register/", json=data)
        if response.status_code == 201:
            return redirect('login_form')
        return render(request, "signup.html", {"error": "Signup failed"})
    return render(request, "signup.html")


def login_form(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
        }
        response = requests.post(f"{API_BASE}/login/", json=data)
        if response.status_code == 200:
            token = response.json()['access']
            request.session['token'] = token
            request.session['username'] = data["username"]
            return redirect('dashboard')
        return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


def dashboard(request):
    token = request.session.get("token")
    if not token:
        return redirect("login_form")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE}/profile/", headers=headers)

    if response.status_code == 200:
        return render(request, "dashboard.html", {"username": response.json()["username"]})
    else:
        return redirect("login_form")


def logout_user(request):
    request.session.flush()
    return redirect("home")