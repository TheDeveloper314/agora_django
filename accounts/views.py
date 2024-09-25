from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.

def registerUser(request):
	if request.user.is_authenticated:
		messages.warning(request, "You are already logged in!")
		return redirect("myAccount")
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			# --- Create user using the form ---
			# password = form.cleaned_data["password"]
			# user = form.save(commit = False)
			# user.set_password(password)
			# user.role = User.roles.index("Customer") + 1
			# user.save()

			# --- Create user using create_user method ---
			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data["last_name"]
			username = form.cleaned_data["username"]
			email = form.cleaned_data["email"]
			password = form.cleaned_data["password"]
			user = User.objects.create_user(first_name = first_name, last_name = last_name, username = username, email = email, password = password)
			user.role = User.roles.index("Customer") + 1
			user.save()
			messages.success(request, "You have registered successfully.")
			return redirect("registerUser")
	else:
		form = UserForm()
	context = {"form": form}
	return render(request, "accounts/registerUser.html", context)

def login(request):
	if request.user.is_authenticated:
		messages.warning(request, "You are already logged in!")
		return redirect("myAccount")
	if request.method == "POST":
		email = request.POST["email"]
		password = request.POST["password"]
		user = auth.authenticate(email = email, password = password)
		if user:
			auth.login(request, user)
			messages.success(request, "Successfully logged in")
			return redirect("myAccount")
		else:
			messages.error(request, "Invalid credentials")
			return redirect("login")

	return render(request, "accounts/login.html")

def logout(request):
	auth.logout(request)
	messages.info(request, "Successfully logged out")
	return redirect("login")

@login_required(login_url = "login")
def myAccount(request):
	user = request.user
	user_role = user.get_role()
	if not user_role and user.is_superadmin:
		redirect_url = f"/admin"
	else:
		redirect_url = f"{user_role.lower()}Dashboard"
	return redirect(redirect_url)

@login_required(login_url = "login")
def customerDashboard(request):
	if request.user.get_role().lower() != "customer":
		raise PermissionDenied
	return render(request, "accounts/customerDashboard.html")

@login_required(login_url = "login")
def vendorDashboard(request):
	if request.user.get_role().lower() != "vendor":
		raise PermissionDenied
	return render(request, "accounts/vendorDashboard.html")