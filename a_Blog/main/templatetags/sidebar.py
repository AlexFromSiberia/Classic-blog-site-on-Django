from django import template
from main.models import Post, Tag

register = template.Library()


@register.inclusion_tag('main/popular_posts_tpl.html')
def get_popular_post(cnt=3):
    """Get popular posts."""
    posts = Post.objects.order_by('-views')[:cnt]
    return {'posts': posts}


@register.inclusion_tag('main/tags_tpl.html')
def get_tags_post():
    """Get tags."""
    tags = Tag.objects.all
    return {'tags': tags}

