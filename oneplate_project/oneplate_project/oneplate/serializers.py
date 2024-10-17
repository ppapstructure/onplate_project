from rest_framework import serializers
from oneplate.models import User, Review, Comment, Like

class UserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False, allow_empty_file=True, use_url=True)
    class Meta:
        model = User
        fields = ['id', 'nickname', 'email', 'profile_pic', 'intro']
        read_only_fields = ['email']  # 이메일을 수정하지 않으려면 읽기 전용으로 설정
        extra_kwargs = {
            'profile_pic': {'required': False},  # readOnly 대신 required 설정으로 처리
        }

    def to_representation(self, instance):
        print("Custom UserSerializer is being used!")  # 디버그 메시지
        return super().to_representation(instance)

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # 작성자 정보
    review = serializers.PrimaryKeyRelatedField(read_only=True)  # 리뷰 정보
    class Meta:
        model = Comment
        fields = ['comment_id', 'content', 'dt_created', 'author', 'review']

# Review
class ReviewListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # 간단한 정보만 포함 (닉네임 정도)

    class Meta:
        model = Review
        fields = ['review_id', 'title', 'author', 'cook_ingredient','image1','dt_created','rating']

class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    # 아래껄로 바꾸는게 맞지 싶다.
    # author = serializers.StringRelatedField(read_only=True)
    review_id = serializers.IntegerField(read_only=True)
    # related_name을 통해서 comment_set 이름변경 가능
    comment = CommentSerializer(many=True, read_only=True, source='comment_set') # 연결된 댓글들

    class Meta:
        model = Review
        fields = [
            'review_id',
            'title',
            'author',
            'cook_name',
            'cook_ingredient',
            'rating',
            'image1',
            'image2',
            'content',
            'comment',
        ]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'content_type_id', 'object_id', 'dt_created']



# class LikeSerializer(serializers.ModelSerializer):
#     content_type = serializers.CharField(write_only=True)  # 'review' or 'comment'
#     object_id = serializers.IntegerField(write_only=True)
#
#     class Meta:
#         model = Like
#         fields = ['id', 'user', 'content_type_id', 'object_id']
#         read_only_fields = ['id', 'user']
#
#     def validate_content_type(self, value):
#         if value not in ['review', 'comment']:
#             raise serializers.ValidationError("content_type must be either 'review' or 'comment'")
#         return value