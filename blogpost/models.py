from django.db import models
from django.utils import timezone
from django.urls import reverse


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    content = models.TextField()
    preview_image = models.ImageField(upload_to='blogpost/images/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('blogpost:post_detail', args=[str(self.slug)])

    def __str__(self):
        return self.title
