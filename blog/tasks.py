from celery import shared_task
from .models import Post
from user.models import User


@shared_task(name="create_scheduled_post")
def create_scheduled_post(title="Scheduled Post", content="This is an automated post", author_id=1):
    print(f"Task called with: title={title}, content={content}, author_id={author_id}")
    author = User.objects.get(id=author_id)
    Post.objects.create(
        title=title,
        content=content,
        author=author,
    )