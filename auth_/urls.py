from django.urls import path
from rest_framework.routers import DefaultRouter

from auth_ import views

urlpatterns = [
    #    path('activations/activate/<str:uuid>/', views.activate),
]

router = DefaultRouter()
router.register(r'activations', views.ActivationViewSet)  # noqa
router.register(r'users', views.UserViewSet)
urlpatterns += router.urls
