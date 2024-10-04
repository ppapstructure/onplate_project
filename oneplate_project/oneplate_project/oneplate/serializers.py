from rest_framework import serializers
from oneplate.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'email', 'intro',]

