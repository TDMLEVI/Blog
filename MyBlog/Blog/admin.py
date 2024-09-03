from django.contrib import admin
from .models import Post, ContentBlock, Category, UserProfile, Comment

class ContentBlockInline(admin.StackedInline):
    model = ContentBlock
    extra = 1  # Number of extra blank forms to display

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ContentBlockInline]

admin.site.register(ContentBlock)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Comment)