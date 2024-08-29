from django import template
from django.contrib.auth import get_user_model
from django.core.cache import cache

register = template.Library()
User = get_user_model()


@register.filter(name="has_group")
def has_group(user: User, group_name: str) -> bool:
    """
    Jinja tag to check if a user is in a specific group.

    Args:
        user (User): The user to check.
        group_name (str): The name of the group.

    Returns:
        bool: True if the user is in the group, False otherwise.
    """
    cache_key = f"user_{user.pk}_groups"
    cached_groups = cache.get(cache_key)

    if cached_groups is None:
        cached_groups = set(user.groups.values_list("name", flat=True))
        cache.set(cache_key, cached_groups)

    return group_name in cached_groups
