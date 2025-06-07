from django.contrib import admin

from django.contrib import admin
from .models import Category, Tag, Post, Follow, Comment, Profile, PostMedia


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "is_published")
    list_filter = ("is_published", "categories", "tags")
    search_fields = ("title", "content", "author__email")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories", "tags", "likes")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "following", "created_at")
    search_fields = ("follower__email", "following__email")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at", "is_approved")
    list_filter = ("is_approved",)
    search_fields = ("post__title", "user__email", "content")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")
    search_fields = ("user__email",)


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display = ("post", "file")
    search_fields = ("post__title",)
