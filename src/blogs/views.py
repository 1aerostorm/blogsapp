from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Account, Post
from .permissions import ReadOnlyOrAdmin
from .queries import fetch_posts, submit_post, get_post, get_post_comments
from .serializers import AccountSerializer, AuthorSerializer, PostSerializer
from .validation import post_list_params

class AccountListCreateAPIView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [ReadOnlyOrAdmin]

class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [ReadOnlyOrAdmin]

    def get_queryset(self):
        return Post.objects.none()

    def list(self, request, *args, **kwargs):
        author_id, sort_by, sort_order, offset, limit = post_list_params(request)

        rows = fetch_posts(author_id, sort_by, sort_order, offset, limit)

        results = []
        for r in rows:
            author = {
                "id": r[6],
                "username": r[7],
                "email": r[8],
            }

            author_data = AuthorSerializer(
                author,
                context={"request": request}
            ).data

            last_comment = None
            if r[9]:
                last_comment = {
                    "id": r[9],
                    "content": r[10],
                    "created_at": r[11],
                    "username": r[12],
                }

            results.append({
                "id": r[0],
                "title": r[1],
                "description": r[2],
                "content": r[3],
                "image": r[4],
                "created_at": r[5],
                "author": author_data,
                "last_comment": last_comment,
            })

        return Response(results)

    def perform_create(self, serializer):
        data = serializer.validated_data

        submit_post(data["author"].id, data["title"], data["description"],
            data.get("content"), data.get("image")
        )

class PostDetailAPIView(APIView):
    def get(self, request, post_id):
        comment_limit = int(request.GET.get('comment_limit', 10))
        comment_offset = int(request.GET.get('comment_offset', 0))

        r = get_post(post_id)
        if not r:
            return Response({'error': 'Post not found'}, status=404)

        author = {
            "id": r[6],
            "username": r[7],
            "email": r[8],
        }

        author_data = AuthorSerializer(
            author,
            context={"request": request}
        ).data

        post_data = {
            "id": r[0],
            "title": r[1],
            "description": r[2],
            "content": r[3],
            "image": r[4],
            "created_at": r[5],
            "author": author_data,
        }

        comments_rows = get_post_comments(post_id, comment_offset, comment_limit)

        post_data['comments'] = [
            {'id': r[0], 'username': r[1], 'content': r[2], 'created_at': r[3]}
            for r in comments_rows
        ]

        return Response(post_data)
