from django.db import models
from django.contrib.auth.models import User


class DocumentCategory(models.Model):
    """文档分类模型"""
    name = models.CharField(max_length=100, verbose_name="分类名称")
    description = models.TextField(blank=True, verbose_name="描述")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name="父分类")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = "文档分类"
        verbose_name_plural = "文档分类"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Document(models.Model):
    """文档模型"""
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(blank=True, verbose_name="内容")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    category = models.ForeignKey(DocumentCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="分类")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "文档"
        verbose_name_plural = "文档"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title