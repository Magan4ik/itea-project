from typing import Type

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.accounts_serializers import UserCreateSerializer, UserReadSerializer

from accounts.utils import send_activation_email

User = get_user_model()


def clean_data(**params) -> dict:
    clean_params = dict()
    for key in params:
        clean_params[key] = params[key][0]

    return clean_params


class UserView(APIView):

    def get(self, request: Request) -> Response:
        cleaned_data = clean_data(**request.query_params)
        user_list = User.objects.filter(
            **cleaned_data
        )
        if user_list.exists():
            read_serializer = UserReadSerializer(user_list, many=True)
            return Response(read_serializer.data, status=status.HTTP_200_OK)
        return Response({"errors": ["user not found"]}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request: Request) -> Response:
        create_serializer = UserCreateSerializer(data=request.data)
        if create_serializer.is_valid():
            user = create_serializer.save()
            send_activation_email(user)
            read_serializer = UserReadSerializer(user)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": create_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ActivateView(APIView):

    def post(self, request: Request) -> Response:
        cleaned_data = clean_data(**request.data)
        token = cleaned_data.pop("token")
        try:
            user = User.objects.get(**cleaned_data)
        except User.DoesNotExist:
            return Response({"errors": ["something went wrong"]}, status=status.HTTP_400_BAD_REQUEST)

        if token == user.register_token and not user.is_active:
            user.is_active = True
            user.save()
            return Response({"message": ["user has been successfully activated"]}, status=status.HTTP_200_OK)

        return Response({"errors": ["something went wrong"]}, status=status.HTTP_400_BAD_REQUEST)
