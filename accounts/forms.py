from django.forms import ModelForm, CharField, PasswordInput, ValidationError
from .models import User

class UserForm(ModelForm):
	password = CharField(widget=PasswordInput())
	confirm_password = CharField(widget=PasswordInput())
	class Meta:
		model = User
		fields = ["first_name", "last_name", "username", "email", "password"]

	def clean(self):
		cleaned_data = super().clean()
		password = cleaned_data["password"]
		confirm_password = cleaned_data["confirm_password"]

		if password != confirm_password:
			raise ValidationError("Passwords do not match.")