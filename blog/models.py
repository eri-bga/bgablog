from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.utils.translation import gettext as _
from users.models import CustomUser
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
import os

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Category(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('Category', slugify(self.category_slug), instance)
        return None
    
    title = models.CharField(_('Title'), max_length=250)
    subtitle = models.CharField(_('Subtitle'), max_length=250)
    category_slug = models.SlugField(_('Category Slug'), null=False, blank=False, unique=True)
    published = models.DateTimeField(_('Date Published'), default=timezone.now())
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT)
    image = models.ImageField(default='default/no_image.jpg', upload_to=image_upload_to, max_length=255)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['-published']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.post_slug:
            self.post_slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)
    

class Post(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('Category', slugify(self.category.category_slug), slugify(self.post_slug), instance)
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    title = models.CharField(max_length=250)
    subtitle = models.CharField(_('Subtitle'), max_length=250)
    post_slug = models.SlugField(max_length=250, unique=True, unique_for_date='publish', null=False, blank=False)
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT)
    body = HTMLField(blank=True, default='')
    publish = models.DateTimeField(default=timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PUBLISHED)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(default='default/no_image.jpg', upload_to=image_upload_to, max_length=255)
    tags = TaggableManager()
    
    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        ordering = ['-publish']
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        indexes = [
            models.Index(fields=['publish']),
        ]
    
    def __str__(self) -> str:
        return self.title


    def get_absolute_url(self):
        return reverse("blog:post_detail",
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.post_slug])
    
    def save(self, *args, **kwargs):
        if not self.post_slug:
            self.post_slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = HTMLField(blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
    
    def __str__(self) -> str:
        return f'Comment by {self.name} on {self.post}'