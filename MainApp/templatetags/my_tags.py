from django import template
register = template.Library()


def is_empty(value, alt):
   if value:
       return value
   return alt

def newline(text):
    return text.replace('\n','<br>')


register.filter('is_empty', is_empty)
register.filter('newline', newline)
