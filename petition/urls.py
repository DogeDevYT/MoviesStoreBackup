from django.urls import path
from .views import petition_view, like_petition_view

urlpatterns = [
    path('', petition_view, name='petition_view'),
    # URL for liking/unliking a petition
    path('<int:petition_id>/like/', like_petition_view, name='like_petition'),
]
