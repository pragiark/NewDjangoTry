from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#Custom model Manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICED = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICED,
                              default='draft')
    # Segments custom manager
    objects = models.Manager()  # manager domyslny
    published = PublishedManager()  # Manadzer niestandardowy

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


