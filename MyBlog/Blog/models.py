from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=500)
    slug = models.PositiveIntegerField(unique=True, blank=True, null=True)
    intro = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    BlogCover = models.ImageField(upload_to='blog_covers/')
    views = models.PositiveIntegerField(default=0)
    last_viewed = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = self.id
            self.save()

    def increment_views(self):
        self.views += 1
        self.last_viewed = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class ContentBlock(models.Model):
    BLOCK_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
    ]
    post = models.ForeignKey(Post, related_name='content_blocks', on_delete=models.CASCADE)
    block_type = models.CharField(max_length=10, choices=BLOCK_TYPES)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.block_type} - {self.post.title}'
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', null=True, blank=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
    
    @property
    def count_replies(self):
        # A recursive function to count all replies
        def get_all_replies(comment):
            children = comment.children.all()
            count = len(children)
            for child in children:
                count += get_all_replies(child)
            return count
        
        return get_all_replies(self)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username