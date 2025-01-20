from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    name = models.TextField()
    country = models.IntegerField()
    max_credits = models.DecimalField(max_digits=10, decimal_places=2, default=100000)
    is_active = models.BooleanField(default=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='token')
    refresh_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
