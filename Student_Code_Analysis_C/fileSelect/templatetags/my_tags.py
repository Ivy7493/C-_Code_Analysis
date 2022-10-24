from django import template

register = template.Library()

@register.filter
def get_by_index(l, i):
    return l[i]

@register.filter
def countTabs(l):
    count = l.count('$')
    countArray = [""]*count
    return countArray;

@register.filter
def replaceTabs(l):
    return l.replace('$',"")

@register.filter
def addCPP(l):
    return l + '.cpp'

@register.filter
def addH(l):
    return l + '.h'



