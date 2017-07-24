from django import template

register = template.Library()

@register.inclusion_tag('member/member_menu.html')
def user_menu(request):
    if request.session.get('id') is not None:
        _id = int(request.session.get('id'))
        _user = request.session.get('username')
        if _id > 0:
            return {'user':{'is_logined':True, 'username':_user}}
    return {'user':{'is_logined':False}}