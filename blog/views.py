from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from .service import get_all_posts, create_post, get_post_by_id, update_post, delete_post


# Create your views here.

@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = get_all_posts()
        serializer = PostSerializer(posts, many=True)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            post = create_post(serializer.validated_data)
            return Response({'success': True, 'data': PostSerializer(post).data},
                            status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, post_id):

    post = get_post_by_id(post_id)

    if not post:
        return Response({'success': False, 'error': 'Post not found'}, status =status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response({'success': True, 'data': serializer.data},status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            updated_post = update_post(post, serializer.validated_data)
            updated = PostSerializer(updated_post)
            return Response({'success': True, 'data': updated.data},status=status.HTTP_200_OK)
        
    elif request.method == 'DELETE':
        delete_post(post)
        return Response({'success': True, 'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)