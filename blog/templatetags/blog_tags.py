from django import template

from blog.models import Post

register = template.Library()

@register.simple_tag
def postcount():
    return Post.objects.count()

@register.inclusion_tag('blog/latestpost.html')
def latest_post(count):
    latest = Post.objects.order_by('-publish')[:count]
    return {'latestpost':latest}

