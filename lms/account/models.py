from django.db import models
from django.contrib.auth.models import(BaseUserManager,AbstractBaseUser)

# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self,full_name,email,contact_no,address,is_student=False,is_teacher=False,is_manager=False,password=None):
        if not email:
            raise ValueError('user must have an email address')
        user=self.model(
            full_name=full_name,
            email=self.normalize_email(email),
            contact_no=contact_no,
            is_student=is_student,
            is_teacher=is_teacher,
            is_manager=is_manager,
            address=address,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,password=None):
        user=self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
        email = models.EmailField(
            verbose_name='email address',
            max_length=255,
            unique=True
        )
        is_student = models.BooleanField(default=False)
        is_teacher = models.BooleanField(default=False)
        is_manager = models.BooleanField(default=False)
        is_admin = models.BooleanField(default=False)
        is_active = models.BooleanField(default=True)

        objects = AccountManager()
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []

        def has_perm(self, perm, obj=None):
            "Does the user have a specific permission?"
            # Simplest possible answer: Yes, always
            return True

        def has_module_perms(self, app_label):
            "Does the user have permissions to view the app `app_label`?"
            # Simplest possible answer: Yes, always
            return True

        @property
        def is_staff(self):
            "Is the user a member of staff?"
            # Simplest possible answer: All admins are staff
            return self.is_admin
