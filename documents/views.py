from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Document, DocumentCategory
from .serializers import (
    DocumentSerializer, DocumentListSerializer, DocumentCreateSerializer,
    DocumentCategorySerializer
)
import logging

logger = logging.getLogger(__name__)


class DocumentViewSet(viewsets.ModelViewSet):
    """文档视图集"""
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'category']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_permissions(self):
        """安全方法(GET/HEAD/OPTIONS)允许匿名，写操作需要登录"""
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        """根据动作选择序列化器"""
        if self.action == 'list':
            return DocumentListSerializer
        elif self.action == 'create':
            return DocumentCreateSerializer
        return DocumentSerializer
    
    def get_queryset(self):
        """获取查询集"""
        queryset = Document.objects.all()
        
        # 如果不是超级用户，只能看到自己的文档
        if not self.request.user.is_superuser:
            queryset = queryset.filter(author=self.request.user)
        
        return queryset.select_related('author', 'category')
    
    def perform_create(self, serializer):
        """创建文档"""
        serializer.save(author=self.request.user)
        logger.info(f"Document created by user {self.request.user.username}")
    
    def perform_update(self, serializer):
        """更新文档"""
        serializer.save()
        logger.info(f"Document {serializer.instance.id} updated by user {self.request.user.username}")
    
    @action(detail=False, methods=['get'])
    def my_documents(self, request):
        """获取当前用户的文档"""
        documents = Document.objects.filter(author=request.user)
        serializer = DocumentListSerializer(documents, many=True, context={'request': request})
        return Response(serializer.data)


class DocumentCategoryViewSet(viewsets.ModelViewSet):
    """文档分类视图集"""
    queryset = DocumentCategory.objects.all()
    serializer_class = DocumentCategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        """分类的读取开放，写操作需要登录"""
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def tree(self, request):
        """获取分类树"""
        categories = DocumentCategory.objects.filter(parent=None)
        serializer = DocumentCategorySerializer(categories, many=True)
        return Response(serializer.data)


def document_list_view(request):
    """文档列表页面视图"""
    return render(request, 'documents/document_list.html')