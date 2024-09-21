from django.shortcuts import render, redirect
from accounts.forms import UserForm
from vendor.forms import VendorForm
from accounts.models import User, UserProfile
from django.contrib import messages

# Create your views here.

def registerVendor(request):
	if request.method == "POST":
		form = UserForm(request.POST)
		v_form = VendorForm(request.POST, request.FILES)

		if form.is_valid() and v_form.is_valid():
			# save the user using form
			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data["last_name"]
			username = form.cleaned_data["username"]
			email = form.cleaned_data["email"]
			password = form.cleaned_data["password"]
			user = User.objects.create_user(first_name = first_name, last_name = last_name, username = username, email = email, password = password)
			user.role = User.roles.index("Vendor") + 1
			user.save()

			# save the vendor using v_form
			vendor = v_form.save(commit = False)
			user_profile = UserProfile.objects.get(user = user)
			vendor.user = user
			vendor.user_profile = user_profile
			vendor.is_approved = False
			vendor.save()
			messages.success(request, "Restaurant created successfully. Please wait for approval.")
			return redirect("registerVendor")
	
	else:
		form = UserForm()
		v_form = VendorForm()

	context = {
		"form": form,
		"v_form": v_form,
	}
	return render(request, "vendor/registerVendor.html", context)