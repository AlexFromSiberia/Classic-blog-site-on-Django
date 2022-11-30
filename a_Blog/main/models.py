from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Category model"""
    title = models.CharField(max_length=255 )
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)

    def __str__(self):
        """Returns category title as string, instead of object address"""
        return self.title

    def get_absolute_url(self):
        """Getting url address for a category"""
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)

    def __str__(self):
        """Returns tag title as string, instead of object address"""
        return self.title

    def get_absolute_url(self):
        """Getting url address for a tag"""
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Post(models.Model):
    """Main model"""
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    author = models.CharField(max_length=100, verbose_name='Автор')
    content = models.TextField(blank=True)
    # Creation name will be added automatically
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='ссылка на фото')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def get_absolute_url(self):
        """Getting url address for a post"""
        return reverse('post', kwargs={'slug': self.slug})

    def __str__(self):
        """Returns post title as string, instead of object address"""
        return self.title

    class Meta:
        # '-' means reversed order
        ordering = ['-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

