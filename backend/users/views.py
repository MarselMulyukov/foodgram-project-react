from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from .models import Follow
from .serializers import SubscriptionSerializer

User = get_user_model()


class SubscriptionListAPIView(ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class SubscribeView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        user = request.user
        follow, created = Follow.objects.get_or_create(
            author=author,
            user=user
        )
        if not created:
            data = {"error": "Already in followings"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data = SubscriptionSerializer(
            instance=author,
            context={"request": request}
        ).data
        return Response(data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        user = request.user
        follow = Follow.objects.filter(author=author, user=user)
        if follow:
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        error = {"errors": "You are not subscribed"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
