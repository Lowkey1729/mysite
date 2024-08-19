
from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'blog'
router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
urlpatterns = [
    path('', include(router.urls)),
    # path('', views.PostView, name='post_list'),
    # path('', views.post_list, name='post_list'),
    # path('<int:id>/', views.post_detail, name='post_detail'),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>',
        views.post_detail,
        name='post_detail'
    ),
    path('<int:post_id>/share/', views.post_share, name='post_share')
]
