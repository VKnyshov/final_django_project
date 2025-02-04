from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "user", "text", "created_at", "updated_at"]  # ✅ Додано `updated_at`
        read_only_fields = ["id", "user", "created_at", "updated_at"]  # ✅ `updated_at` оновлюється автоматично
