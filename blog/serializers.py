from rest_framework import serializers
from blog.models import Category, Post, Comment, Profile, Tag, Follow, PostMedia
from django.contrib.auth import get_user_model

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "slug")


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "slug",
            "content",
            "categories",
            "is_published",
            "created_at",
            "updated_at",
            "like_count",
            "tags",
        )

    def get_like_count(self, obj):
        return obj.like_count()

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long."
            )
        return value

    def validate_content(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(
                "Content must be at least 20 characters long."
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ("id", "post", "user", "content", "created_at", "is_approved")


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "user", "bio", "profile_image")


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    following = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]

    def validate(self, data):
        follower = self.context["request"].user
        following = data.get("following")

        if follower == following:
            raise serializers.ValidationError("You can't follow yourself")

        if Follow.objects.filter(follower=follower, following=following).exists():
            raise serializers.ValidationError("You following this user")

    def create(self, validated_data):
        validated_data["follower"] = self.context["request"].user
        return super().create(validated_data)


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ["id", "post", "file"]
        read_only_fields = ["post"]
