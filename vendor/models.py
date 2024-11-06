from django.db import models
from accounts.models import User, UserProfile

# Create your models here.

class Vendor(models.Model):
	user = models.OneToOneField(User, related_name = "user", on_delete = models.CASCADE)
	user_profile = models.OneToOneField(UserProfile, related_name = "userprofile", on_delete = models.CASCADE)
	vendor_name = models.CharField(max_length = 50)
	vendor_license = models.ImageField(upload_to = "vendors/licenses")
	is_approved = models.BooleanField(default = False)
	created_at = models.DateTimeField(auto_now_add = True)
	modified_at = models.DateTimeField(auto_now = True)

	def __str__(self):
		return self.vendor_name

	# def save(self, *args, **kwargs):
	# 	if self.pk:
	# 		orig = Vendor.objects.get(pk = self.pk)
	# 		if self.is_approved != orig.is_approved:
	# 			if self.is_approved:
	# 				send_email(request, "vendor_approval", self.user)
	# 			else:
	# 				send_email(request, "vendor_rejection", self.user)
					
	# 	return super(Vendor, self).save(*args, **kwargs)