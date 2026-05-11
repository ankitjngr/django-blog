from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer, CommentSerializer, UserSerializer, ProfileSerializer
from .service import get_all_posts, create_post, get_post_by_id, update_post, delete_post, CreateComment, create_like, get_user_profile


# Create your views here.

@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = get_all_posts()
        serializer = PostSerializer(posts, many=True)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            
            post = create_post(
                serializer.validated_data, 
                author = request.user
                )
            

            return Response({'success': True, 'data': PostSerializer(post).data},
                            status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail(request, post_id):

    post = get_post_by_id(post_id)

    if not post:
        return Response({'success': False, 'error': 'Post not found'}, status =status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response({'success': True, 'data': serializer.data},status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        if request.user != post.author:
            return Response({'success': False, 'error': 'You do not have permission to edit this post'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            updated_post = update_post(post, serializer.validated_data)
            updated = PostSerializer(updated_post)
            return Response({'success': True, 'data': updated.data},status=status.HTTP_200_OK)
        
    elif request.method == 'DELETE':
        if request.user != post.author:
            return Response({'success': False, 'error': 'You do not have permission to delete this post'}, status=status.HTTP_403_FORBIDDEN)
        delete_post(post)
        return Response({'success': True, 'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])
def comment_list(request, pk):
    if request.method == 'GET':
        post = get_post_by_id(post_id=pk)
        if not post:
            return Response({'success': False, 'error': 'Post not found'},
                            status=status.HTTP_400_BAD_REQUEST)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        post = get_post_by_id(post_id=pk)
        if not post:
            return Response({'success': False, 'error': 'Post not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment =CreateComment(
                serializer.validated_data,
                author=request.user,
                post=post
            )
            return Response({'success': True, 'data': CommentSerializer(comment).data}, status=status.HTTP_200_OK)
        
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
        post = get_post_by_id(post_id=pk)
        if not post: 
            return Response({'success': False, 'error': 'Post not found'},status=status.HTTP_400_BAD_REQUEST)
        like, created = create_like(post, request.user)
        if created:
            return Response({'success': True, 'message': 'Post liked successfully'}, status=status.HTTP_201_CREATED)
        
        like.delete()
        return Response({'success': True, 'message': 'Post unliked successfully'}, status=status.HTTP_200_OK)
    


@api_view(['POST'])
def register_api(request):
    print('register_api called with postman')

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'success': True, 'data': UserSerializer(user).data},
                        status=status.HTTP_201_CREATED)
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


from .service import get_user_profile

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def userprofile(request):

    profile = get_user_profile(request.user)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response({'success': True, 'data': serializer.data}, status=200)

    elif request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=200)

        return Response({'success': False, 'errors': serializer.errors}, status=400)