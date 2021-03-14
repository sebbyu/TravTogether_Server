from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.text import slugify
import os
import shutil
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import csv
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now

def get_locations(filename):
  places = []
  with open(filename, encoding='utf8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
      place = ""
      if row[6] in ['CHN', 'USA', 'RUS']:
        place = f'{row[0]}, {row[4]}, {row[1]}'
      else:
        place = f'{row[0]}, {row[1]}'
      places.append((f'{row[0]}, {row[4]}, {row[1]}', place))
    return tuple(places)
LOCATIONS = get_locations(os.path.abspath(os.path.join(settings.STATIC_ROOT,
  'locations/world-cities.csv')))

GENDER = (
  ('Male', 'Male'),
  ('Female', 'Female'),
  ('Non-binary', 'Non-binary'),
)

ETHNICITY = (
  ('American Indian / Alaska Native', 'American Indian / Alaska Native'),
  ('Asian', 'Asian'),
  ('Black / African American', 'Black / African American'),
  ('Hispanic / Latino', 'Hispanic / Latino'),
  ('Native Hawaiian / Other Pacific Islander', 'Native Hawaiian / Other Pacific Islander'),
  ('White', 'White'),
)

AGE_RANGE = (
  ("10-", "10-"),
  ("10-20", "10-20"),
  ("20-30", "20-30"),
  ("30-40", "30-40"),
  ("40-50", "40-50"),
  ("50-60", "50-60"),
  ("60+", "60+"),
)

storage = FileSystemStorage(settings.MEDIA_ROOT)

def upload_to(instance, filename):
  dir_name = instance.slug
  return f'profile_images/{dir_name}/{filename}'

class UserManager(BaseUserManager):
  def create_user(self, email, password, **other_fields):
    if not email:
      raise ValueError(_('Email is required'))
    email = self.normalize_email(email)
    user = self.model(
      email=email,
      **other_fields
    )
    user.set_password(password)
    user.save()
    return user

  def create_superuser(self, email, password, **other_fields):
    other_fields.setdefault('is_admin', True)
    other_fields.setdefault('is_staff', True)
    superuser = self.create_user(
      email=email, password=password, **other_fields
    )
    return superuser

class User(AbstractBaseUser):
  email = models.EmailField(_("email"), max_length=254, unique=True)
  slug = models.SlugField(_("slug"), unique=True, blank=True)
  nickname = models.CharField(_("nickname"), max_length=50, unique=True, blank=True)
  gender = models.CharField(_("gender"), max_length=20, choices=GENDER, blank=True)
  age = models.CharField(_("age"), max_length=50, choices=AGE_RANGE, blank=True)
  ethnicity = models.CharField(_("ethnicity"), max_length=50, choices=ETHNICITY, blank=True)
  bio = models.TextField(_("bio"), blank=True)
  location = models.CharField(_("location"), max_length=250, choices=LOCATIONS, blank=True)
  fromFirebase = models.BooleanField(_("fromFirebase"), default=False)
  is_admin = models.BooleanField(_("is_admin"), default=False)
  is_staff = models.BooleanField(_("is_staff"), default=False)
  is_active = models.BooleanField(_("is_active"), default=True)

  objects = UserManager()

  USERNAME_FIELD = "email"

  class Meta:
    ordering = ('nickname',)

  def __str__(self):
    return f'{self.nickname}'

  def save(self, *args, **kwargs):
    if not self.nickname:
      self.nickname = slugify(self.email.split('@')[0])
    self.slug = slugify(self.email.split('@')[0])
    super(User, self).save(*args, **kwargs)

  def has_perm(self, perm, obj=None):
    return self.is_active
  
  def has_module_perms(self, app_label):
    return self.is_admin





