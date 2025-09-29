from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, DocumentCategoryViewSet, document_list_view

# 创建路由器
router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'categories', DocumentCategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('list/', document_list_view, name='document_list'),
]