from django import template
from django.contrib.auth import get_user_model
from django.core.cache import cache

register = template.Library()
User = get_user_model()


# @register.filter(name="has_group")
# def has_group(user: User, group_name: str) -> bool:
#     group = Group.objects.get(name=group_name)  # auth_group
#     return True if group in user.groups.all() else False  # auth_group, users_user_groups


@register.filter(name="has_group")
def has_group(user: User, group_name: str) -> bool:
    cache_key = f"user_{user.pk}_groups"
    cached_groups = cache.get(cache_key)

    if cached_groups is None:
        cached_groups = set(user.groups.values_list("name", flat=True))
        cache.set(cache_key, cached_groups)

    return group_name in cached_groups
