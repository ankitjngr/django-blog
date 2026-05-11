from .models import Post, Comment, Like, UserProfile


def get_all_posts():
    return Post.objects.all()


def create_post(validated_data, author):
    return Post.objects.create(
        title = validated_data.get('title'),
        content = validated_data.get('content'),
        image = validated_data.get('image'),
        author = author,
        
    )


def get_post_by_id(post_id):
    try:
        post = Post.objects.get(id=post_id)
        return post
    except Post.DoesNotExist:
        return None
    

def update_post(post, validated_data):
    for key, value in validated_data.items():
        setattr(post, key, value)
    post.save()
    return post


def delete_post(post):
    post.delete()


def CreateComment(validated_data, author, post):
    return Comment.objects.create(
        content = validated_data.get('content'),
        author = author,
        post = post
    )


def create_like(post, user):
    like, created = Like.objects.get_or_create(
        post=post, 
        user=user
        )
    return like, created

def get_user_profile(user):
    profile = UserProfile.objects.get(user=user)
    return profile