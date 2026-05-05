from .models import Post


def get_all_posts():
    return Post.objects.all()


def create_post(validated_data):
    return Post.objects.create(
        title = validated_data.get('title'),
        content = validated_data.get('content'),
        image = validated_data.get('imgae'),
        author = validated_data.get('author'),
        
    )


def get_post_by_id(post_id):
    try:
        return Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return None
    

def update_post(post, validated_data):
    for key, value in validated_data.items():
        setattr(post, key, value)
    post.save()
    return post


def delete_post(post):
    post.delete()
