from django import template

register = template.Library()

@register.inclusion_tag('nmrpro_js.html')
def nmrpro_js():
    return {'load_js':True}

@register.inclusion_tag('nmrpro_js.html')
def nmrpro_css():
    return {'load_css':True}


@register.inclusion_tag('nmrpro_js.html')
def nmrpro_assets():
    return {'load_js':True, 'load_css':True}

@register.inclusion_tag('specdraw.html')
def specdraw(spec_url, full_page=False):
    return {'spec_url':spec_url, 'full_page':full_page}