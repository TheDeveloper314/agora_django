from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User

# Create your views here.

def registerUser(request):
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
			return redirect("registerUser")
	else:
		form = UserForm()
	context = {"form": form}
	return render(request, "accounts/registerUser.html", context)