from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from oneplate.validators import validate_no_special_characters
# Create your models here.

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

    likes = GenericRelation('Like', related_query_name='review')

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

    likes = GenericRelation('Like', related_query_name='comment')

    def __str__(self):
        return self.content[:30]
        
    class Meta:
        db_table = 'user'

class Like(models.Model):
    dt_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    content_type_id = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    like_object = GenericForeignKey('content_type_id', 'object_id')

    def __str__(self):
        return f"({self.user}, {self.like_object})"

    class Meta:
        db_table = 'like'
        unique_together = ['user', 'content_type_id', 'object_id']


# Review와 Comment 모델의 ContentType ID를 가져오는 예시
# 13이 review모델 14가 comment 모델
review_content_type_id = ContentType.objects.get_for_model(Review).id
comment_content_type_id = ContentType.objects.get_for_model(Comment).id

print(f"Review 모델의 ContentType ID: {review_content_type_id}")
print(f"Comment 모델의 ContentType ID: {comment_content_type_id}")