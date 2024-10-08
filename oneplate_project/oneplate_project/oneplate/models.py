from django.db import models
from django.contrib.auth.models import AbstractUser
from oneplate.validators import validate_no_special_characters

# Create your models here.
'''
user 모델에 profile_pic 요소를 추가해서 프로필사진 업로드 유무확인
user - comment -review 관계 구현하고 해당페이지 우선 접근제어 없이 crud 구현하기
'''
class User(AbstractUser):

    nickname = models.CharField(
        max_length=18,
        # unique=True,
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

# Review
'''
title
cook_name
cook_ingredient
rating
image1
image2
content
dt_created
dt_updated
'''

'''
class Review(models.Model):
    title = models.CharField(max_length=30)

    restaurant_name = models.CharField(max_length=20)

    restaurant_link = models.URLField(validators=[validate_restaurant_link])

    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, default=None)

    image1 = models.ImageField(upload_to='review_pics')

    image2 = models.ImageField(upload_to='review_pics', blank=True)

    image3 = models.ImageField(upload_to='review_pics', blank=True)

    content = models.TextField()

    dt_created = models.DateTimeField(auto_now_add=True)

    dt_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-dt_created']
'''

'''
auto_now_add?
# Comment
class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)

    dt_created = models.DateTimeField(auto_now_add=True)

    dt_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:30]
'''

