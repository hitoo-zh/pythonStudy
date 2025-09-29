from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Document, DocumentCategory


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class DocumentCategorySerializer(serializers.ModelSerializer):
    """文档分类序列化器"""
    class Meta:
        model = DocumentCategory
        fields = ['id', 'name', 'description', 'parent', 'created_at']


class DocumentSerializer(serializers.ModelSerializer):
    """文档序列化器"""
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)
    category = DocumentCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'content', 'author', 'author_id', 'category', 'category_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """创建文档"""
        category_id = validated_data.pop('category_id', None)
        
        document = Document.objects.create(**validated_data)
        
        # 设置分类
        if category_id:
            try:
                category = DocumentCategory.objects.get(id=category_id)
                document.category = category
                document.save()
            except DocumentCategory.DoesNotExist:
                pass
        
        return document
    
    def update(self, instance, validated_data):
        """更新文档"""
        category_id = validated_data.pop('category_id', None)
        
        # 更新基本字段
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # 更新分类
        if category_id is not None:
            try:
                category = DocumentCategory.objects.get(id=category_id)
                instance.category = category
            except DocumentCategory.DoesNotExist:
                pass
        
        instance.save()
        return instance


class DocumentListSerializer(serializers.ModelSerializer):
    """文档列表序列化器（简化版）"""
    author = UserSerializer(read_only=True)
    category = DocumentCategorySerializer(read_only=True)
    
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'author', 'category', 'created_at', 'updated_at'
        ]


class DocumentCreateSerializer(serializers.ModelSerializer):
    """文档创建序列化器"""
    class Meta:
        model = Document
        fields = [
            'title', 'content', 'category'
        ]
    
    def create(self, validated_data):
        """创建文档"""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)