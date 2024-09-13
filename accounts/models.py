from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self, first_name, last_name, username, email, password = None, **kwargs):
		if not email:
			raise ValueError("User must have an email address!")

		if not username:
			raise ValueError("User must have a username!")

		user = self.model(
			first_name = first_name,
			last_name = last_name,
			email = self.normalize_email(email),
			username = username,
			)
		user.set_password(password)
		
		is_admin = kwargs.get("is_admin")
		if is_admin:
			user.is_staff = True
			user.is_admin = True
			user.is_superadmin = True
		user.save(using = self._db)
		return user

	def create_superuser(self, first_name, last_name, username, email, password = None):
		user = self.create_user(first_name, last_name, username, email, password, is_admin = True)

class User(AbstractBaseUser):
	roles = ["Customer", "Restaurant Owner"]
	roles_choices = ((index + 1, role) for index, role in enumerate(roles))

	first_name = models.CharField(max_length = 50)
	last_name = models.CharField(max_length = 50)
	username = models.CharField(max_length = 50, unique = True)
	email = models.EmailField(max_length = 100, unique = True)
	phone_no = models.CharField(max_length = 15, blank = True)
	role = models.PositiveSmallIntegerField(choices = roles_choices, blank = True, null = True)

	# required fields
	date_created = models.DateField(auto_now_add = True)
	# date_joined = models.DateField(auto_now_add = True)
	date_joined = models.DateTimeField(default = timezone.now)
	modified_date = models.DateField(auto_now_add = True)
	# last_login = models.DateField(auto_now_add = True)
	last_login = models.DateTimeField(default = timezone.now)
	is_active = models.BooleanField(default = True)
	is_staff = models.BooleanField(default = False)
	is_admin = models.BooleanField(default = False)
	is_superadmin = models.BooleanField(default = False)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["username", "first_name", "last_name"]

	objects = UserManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj = None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, blank = True, null = True)
	profile_picture = models.ImageField(upload_to = "users/profile_picture", blank = True, null = True)
	cover_photo = models.ImageField(upload_to = "users/cover_photos", blank = True, null = True)
	address_line_1 = models.CharField(max_length = 50, blank = True, null = True)
	address_line_2 = models.CharField(max_length = 50, blank = True, null = True)
	country = models.CharField(max_length = 15, blank = True, null = True)
	state = models.CharField(max_length = 15, blank = True, null = True)
	pin_code = models.CharField(max_length = 6, blank = True, null = True)
	latitude = models.CharField(max_length = 20, blank = True, null = True)
	longitude = models.CharField(max_length = 20, blank = True, null = True)
	created_at = models.DateTimeField(auto_now_add = True)
	modified_at = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.user.email