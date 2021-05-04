from django.urls import path
from core import views
from rest_framework.routers import DefaultRouter

app_name = 'core'

router = DefaultRouter()
router.register(r'task', views.TaskViewSet)

urlpatterns = router.urls

urlpatterns += [
#    path('public_offer/', views.PublicOfferView.as_view()),
]
