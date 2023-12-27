from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers


User = get_user_model()


class UserReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):

        with transaction.atomic():
            user = User.objects.create_user(**validated_data, is_active=False)
            return user

