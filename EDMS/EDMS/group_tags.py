from django import template
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

register = template.Library()
User = get_user_model()


@register.filter(name="has_group")
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
