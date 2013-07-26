from django import template
register = template.Library()

@register.filter(name="all_objs_finished")
def all_objs_finished(value):
  return value.all_objs_finished()
