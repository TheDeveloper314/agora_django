from django.shortcuts import render

# Create your views here.

def registerVendor(request):
	return render(request, "vendor/registerVendor.html")