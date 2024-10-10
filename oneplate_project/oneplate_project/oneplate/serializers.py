from rest_framework import serializers
from oneplate.models import User, Review

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


# Review
class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = [
            'title',
            'author',
            'cook_name',
            'cook_ingredient',
            'rating',
            'image1',
            'image2',
            'content',
        ]
