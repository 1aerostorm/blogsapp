from rest_framework import serializers
from .models import Account, Comment, Post

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()

    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get("request")
        if request and not request.user.is_staff:
            data.pop("email", None)

        return data

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=250)
    description = serializers.CharField(max_length=500)
    content = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    image = serializers.URLField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all()
    )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        author = getattr(instance, 'author', None) or instance.get('author')
        ret['author'] = AuthorSerializer(author, context=self.context).data
        return ret

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
