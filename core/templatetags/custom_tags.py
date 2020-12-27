from django import template

register = template.Library()


def subtract(value, arg):
    return value - arg


def convert_to_list(value):
    l = []
    for i in range(value):
        l.append(i)
    return l

register.filter('subtract', subtract)
register.filter('convert_to_list', convert_to_list)