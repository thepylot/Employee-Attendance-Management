from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class ProfilePic(models.Model):
    """User profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profilepics/', blank=True)
   
    def create_user_profile_pic(sender, **kwargs):
        if kwargs['created']:
            user_profile = ProfilePic.objects.create(user=kwargs['instance'])
           
    post_save.connect(create_user_profile_pic, sender=User)   

class BaseLeaveModel(models.Model):

    class Meta:
        abstract=True

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    STATUS_CHOICES = (

        ('waiting', 'WAITING'),
        ('approved', 'APPROVED'),
        ('declined', 'DECLINED'),
    )

    leave_type = models.CharField(max_length=255)
    leave_start_date  = models.DateField()
    leave_end_date = models.DateField()
    leave_start_time = models.TimeField()
    leave_end_time = models.TimeField()
    leave_reason = models.TextField()
    status = models.CharField(max_length = 30, choices = STATUS_CHOICES, default = "waiting")
    days = models.IntegerField(default=0)

    def __str__(self):
        return self.leave_type

    def save(self, *args, **kwargs):
        if self.status == 'declined':
            self.days = 0
        return super(BaseLeaveModel, self).save(*args, **kwargs)    

class Leave(BaseLeaveModel):
    pass

class ArchivedLeave(BaseLeaveModel):
    pass

class AnnualLimit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    annual_leave_limit = models.IntegerField(blank=True)

    def __str__(self):
        return self.user.name