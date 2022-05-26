from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
from django.shortcuts import reverse
from PIL import Image


# Create your models here.
class Post(models.Model):
    name = models.CharField(blank=True, max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],   )
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    components = models.TextField(blank=True)

    def __str__(self):
        if len(self.name) > 10:
            return str(self.name[:10] + '...')
        else:
            return str(self.name)

    def num_likes(self):
        return self.liked.all().count()

    # num of comments here
    def num_comments(self):
        return self.comment_set.all().count()

    def all_comments(self):
        return self.comment_set.all()

    def get_absolute_url(self):
        return reverse('posts:detail-post', kwargs={'pk': self.pk})

    def crop_center(self, pil_img, crop_width: int, crop_height: int) -> Image:
        """
        Функция для обрезки изображения по центру.
        """
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                             (img_height - crop_height) // 2,
                             (img_width + crop_width) // 2,
                             (img_height + crop_height) // 2))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(self.image)
        if(self.image):
            img = Image.open(self.image.path)
            new_img = self.crop_center(img, 1200, 1200)
            new_img.save(self.image.path)

    class Meta:
        ordering = ('-created',)


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.post.pk}"
