from io import BytesIO

from PIL import Image
from django.core.files import File
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Game(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='game')
    desc = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    preview = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def make_preview(self, image, size=(200, 200)):
        image = Image.open(image)
        image.convert('RGB')
        image.thumbnail(size)

        thumb_io = BytesIO()
        image.save(thumb_io, 'JPEG', quality=85)

        preview = File(thumb_io, name=image.name)
        return preview

    def get_preview(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.preview.url
        else:
            if self.image:
                self.preview = self.make_preview(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.preview.url
            else:
                return ''
