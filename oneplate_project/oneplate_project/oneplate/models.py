from django.db import models
from django.contrib.auth.models import AbstractUser
from oneplate.validators import validate_no_special_characters

# Create your models here.
'''
username = None 추가해보자 없어지나
'''
class User(AbstractUser):
    nickname = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        validators=[validate_no_special_characters],
        error_messages={'unique': '이미 사용중인 닉네임입니다.'},
    )
    # profile_pic

    intro = models.CharField(max_length=60, blank=True)

    class Meta:
        db_table = 'app_user'

    def __str__(self):
        return self.email
