from django.db import models
from django.contrib.auth.models import AbstractUser
from oneplate.validators import validate_no_special_characters

# Create your models here.
<<<<<<< HEAD
<<<<<<< HEAD
'''
user 모델에 profile_pic 요소를 추가해서 프로필사진 업로드 유무확인
user - comment -review 관계 구현하고 해당페이지 우선 접근제어 없이 crud 구현하기
'''
=======
>>>>>>> back


class User(AbstractUser):

    nickname = models.CharField(
        max_length=18,
        # unique=True,
        null=True,
        validators=[validate_no_special_characters],
        error_messages={'unique': '이미 사용중인 닉네임입니다.'},
    )
    profile_pic = models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pics')
    intro = models.CharField(max_length=60, blank=True)

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return self.email

# Review
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)  # review_id를 기본 키로 설정
    title = models.CharField(max_length=30)

    cook_name = models.CharField(max_length=20)
    cook_ingredient = models.TextField()

    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, default=None)

    image1 = models.ImageField(upload_to='ai_pics', blank=True)

    image2 = models.ImageField(upload_to='review_pics', blank=True)

    content = models.TextField()

    dt_created = models.DateTimeField(auto_now_add=True)

    dt_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'review'
        ordering = ['-dt_created']

# Comment
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)

    content = models.TextField(max_length=500, blank=False)

    dt_created = models.DateTimeField(auto_now_add=True)

    dt_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:30]
        
    class Meta:
        db_table = 'user'

