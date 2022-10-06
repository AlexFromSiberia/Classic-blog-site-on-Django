from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag
# для возможности подсчёта просмотров
from django.db.models import F


class Home(ListView):
    model = Post
    # явно укажем template
    template_name = 'main/index.html'
    # переопределить имя переменной "object_list" чтобы в template использовать переменную 'posts'
    context_object_name = 'posts'
    paginate_by = 4
    # несуществующие страницы(в списке такого значения нет) будут показаны как 404
    allow_empty = False

    # переопределим метод get_context_data
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # теперь эту переменную мы можем ДОПОЛНИТЬ любыми нужными данными
        context['title'] = 'Classic Blog Design'
        return context


class PostsByCategory(ListView):
    model = Post
    template_name = 'main/by_category.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False

    def get_queryset(self):
        # используем фильтр по модели Post, по слагу из модели Category используя '__'
        # из Post.category  вытащим Category.slug
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class GetPost(DetailView):
    model = Post
    template_name = 'main/DetailView.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class PostsByTag(ListView):
    model = Post
    template_name = 'main/by_category.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False

    def get_queryset(self):
        # используем фильтр по модели Post, по слагу из модели Tags используя '__'
        # из Post.tags  вытащим tags.slug
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class Search(ListView):
    template_name = 'main/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        # icontains - для поиска, метод не чувствителен к регистру
        # request.GET - массив, из него методом get() забираем 's'  - name in templates
        # то что ввёл пользователь
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

        # теперь передадим эти данные в context переменную
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # чтобы работала пагинация
        # в шаблон html пагинатора тоже добавим {{ s }}
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context

