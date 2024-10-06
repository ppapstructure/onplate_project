from rest_framework import serializers
from oneplate.models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'nickname', 'email', 'intro',]
#
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'email', 'intro']

    def to_representation(self, instance):
        print("Custom UserSerializer is being used!")  # 디버그 메시지
        return super().to_representation(instance)


