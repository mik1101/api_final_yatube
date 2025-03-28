from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostVS, CommentVS, GroupVS, FollowVS

router = DefaultRouter()
router.register(r'posts', PostVS, basename='posts')
router.register(r'groups', GroupVS, basename='groups')
router.register(r'posts/(?P<id_post>\d+)/comments',
                CommentVS, basename='comments')
router.register(r'follow', FollowVS, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
