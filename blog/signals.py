import cloudinary
from django.db.models.signals import post_delete
from django.dispatch import receiver
from blog.models import ArticleImages, Article


def destroy_image_on_cloudinary(id, **options):
    cloudinary.uploader.destroy(id, **options)


@receiver(post_delete, sender=ArticleImages)
def post_delete_manager(instance, **kwargs):
    picture_id = instance.picture.public_id
    destroy_image_on_cloudinary(picture_id, **kwargs)


@receiver(post_delete, sender=Article)
def post_delete_manager(instance, **kwargs):
    for article_image in instance.pictures.all():
        destroy_image_on_cloudinary(article_image.picture.public_id, **kwargs)
