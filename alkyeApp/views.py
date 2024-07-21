from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Post, Comment
from rest_framework.pagination import PageNumberPagination
from .serializers import PostSerializer, CommentSerializer
from rest_framework import status
from .serializers import UserSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def postListCreate(request):
    """
    Handles GET and POST requests for the list of posts.
    GET: Returns a list of all posts.
    POST: Creates a new post. Requires the user to be authenticated.
    """
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # Save post with the authenticated user as the author
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def postPagination(request):
    """
    Handles GET requests for paginated list of posts.
    """
    if request.method == 'GET':
        posts = Post.objects.all().order_by('published_date')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def postDetailsById(request, pk):
    """
    Handles GET, PUT, and DELETE requests for a single post by ID.
    GET: Returns the post details.
    PUT: Updates the post. Requires the user to be authenticated.
    DELETE: Deletes the post. Requires the user to be authenticated.
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def commentListCreate(request, pk):
    """
    Handles GET and POST requests for comments on a specific post.
    GET: Returns a list of comments for the specified post.
    POST: Creates a new comment for the specified post. Requires the user to be authenticated.
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)  # Associate the comment with the post and the authenticated user as author
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def like_post(request, pk):
    """
    Handles POST requests to like or unlike a post.
    If the post is already liked by the user, it will be unliked, and vice versa.
    Requires the user to be authenticated.
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        return Response({"message": "Unliked the post."}, status=status.HTTP_200_OK)
    else:
        post.likes.add(request.user)
        return Response({"message": "Liked the post."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_user(request):
    """
    Handles POST requests to register a new user.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
