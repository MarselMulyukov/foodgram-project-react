from django.urls import include, path

from .views import SubscribeView, SubscriptionListAPIView

urlpatterns = [
    path("users/subscriptions/", SubscriptionListAPIView.as_view(),),
    path("", include("djoser.urls")),
    path("users/<int:pk>/subscribe/", SubscribeView.as_view(),),
    path("auth/", include("djoser.urls.authtoken")),
]
