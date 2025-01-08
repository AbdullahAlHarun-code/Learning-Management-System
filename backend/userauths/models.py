from django.db import models
from django.db.models.signals import post_save
# Custom User Model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=150)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=True)
    otp = models.CharField(unique=True, max_length=100, blank=True, null=True)
    refresh_token = models.CharField(max_length=1000, blank=True, null=True)
    # is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        email_username, _ = self.email.split('@')
        if self.full_name == '' or self.full_name == None:
            self.full_name = email_username
        if self.username == '' or self.username == None:
            self.username = email_username
        
        # Hash the password if it's not already hashed
        if self.pk is None or not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)

        return super(User, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', default="default-user.jpg", blank=True, null=True)
    full_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.full_name)
        
    def save(self, *args, **kwargs):
        if self.full_name == '' or self.full_name == None:
            if self.user.full_name:
                self.full_name = self.user.full_name
            else:
                self.full_name = self.user.username
        return super(Profile, self).save(*args, **kwargs)
   

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            instance.save()
            Profile.objects.create(user=instance)
        except Exception as e:
            print(f"Error creating profile: {e}")


def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)