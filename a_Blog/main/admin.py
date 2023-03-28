from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    """Form for ckEditor"""
    # content - field in our model
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    """Admin for Post model"""
    prepopulated_fields = {'slug': ('title',)}
    form = PostAdminForm
    save_as = True
    # from your model (то что будет в СПИСКЕ всех записей)
    list_display = ('id', 'title', 'slug', 'author', 'created_at', 'photo', 'get_photo', 'views', 'category')
    # при переходе в каждый Пост будем видеть поля:
    fields = ('title', 'slug', 'author', 'tags', 'content', 'created_at', 'photo', 'get_photo', 'views', 'category')
    # поля также можно сделать ссылками
    list_display_links = ('id', 'title')
    # добавить поля по которым можно делать поиск
    search_fields = ('title',)
    # по каким полям будет возможность фильтра
    list_filter = ('author', 'category', 'tags')
    readonly_fields = ('id', 'created_at', 'get_photo', 'views')
    # кнопка save бутет отображаться и внизу и вверхху для удобства
    save_on_top = True

    def get_photo(self, obj):
        """Escape an errof if there is no photo"""
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

    get_photo.short_description = 'Миниатюра'


class TagAdmin(admin.ModelAdmin):
    """Autofill slug field in admin panel"""
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    """Autofill slug field in admin panel"""
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
