from django import template
from django.conf import settings
from django.template import TemplateSyntaxError
import re


register = template.Library()

_HTML5_BOILERPLATE_MEDIA_PREFIX = getattr(settings, 'HTML5_BOILERPLATE_MEDIA_PREFIX', '/static/html5boilerplate/')
_DEFAULT_JQUERY_SOURCES = (
    '//ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.js',
    _HTML5_BOILERPLATE_MEDIA_PREFIX + 'js/libs/jquery-1.4.2.js',
)


@register.inclusion_tag('html5boilerplate/includes/google_analytics.html',
                        takes_context=True)
def google_analytics(context, ga_tracking_code=None):
    """
    The GA script.
    """
    if ga_tracking_code is None:
        ga_tracking_code = getattr(settings, 'GA_TRACKING_CODE', None)
    if ga_tracking_code is None:
        raise TemplateSyntaxError('The google_analytics template tag requires a tracking code. You must either pass it as an argument or set GA_TRACKING_CODE in settings.py.')
        
    return {
        'ga_tracking_code': ga_tracking_code,
    }


class TagVariantsNode(template.Node):
    
    VARIANTS = (
        ('ie6', '<!--[if lt IE 7 ]>', '<![endif]-->'),
        ('ie7', '<!--[if IE 7 ]>', '<![endif]-->'),
        ('ie8', '<!--[if IE 8 ]>', '<![endif]-->'),
        ('ie9', '<!--[if IE 9 ]>', '<![endif]-->'),
        ('', '<!--[if (gt IE 9)|!(IE)]><!-->', '<!--<![endif]-->'),
    )
    
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        tag = self.nodelist.render(context)
        output_lines = []
        
        # This may be somewhat fragile, but parsing as HTML seems like overkill.
        for variant, wrapper_open, wrapper_close in TagVariantsNode.VARIANTS:
            if variant:
                new_tag, replacement_count = re.subn('(\s*class\s*=\s*)([\'"])', '\\1\\2%s ' % variant, tag)
                if replacement_count == 0:
                    new_tag = re.sub('(/?>\s*$)', ' class="%s" \\1' % variant, tag)
            else:
                new_tag = tag
            output_lines.append(wrapper_open + new_tag + wrapper_close)
        return '\n'.join(output_lines)


@register.tag
def tagvariants(parser, token):
    """
    Adds variants of the wrapped tag for specific browsers, adding classes for
    versions of IE.
    
    Example:
        
        {% tagvariants %}
        <body css="border:0;" class="my-class">
        {% endtagvariants %}

    """
    nodelist = parser.parse(('endtagvariants',))
    parser.delete_first_token()
    args = token.split_contents()
    return TagVariantsNode(nodelist)


class LoadJsNode(template.Node):
    def __init__(self, window_obj, sources, resolve_arguments=True):
        self.window_obj, self.sources, self.resolve_arguments = window_obj, sources, resolve_arguments

    def render(self, context):
        # TODO: Support nested window objects better.
        primary_source = self.sources[0]
        window_obj = self.window_obj
        if self.resolve_arguments:
            primary_source = template.Variable(primary_source).resolve(context)
            window_obj = template.Variable(self.window_obj).resolve(context)            
        fallback_sources = self.sources[1:]
        
        output = '<script src="%s"></script>' % primary_source
        for source in fallback_sources:
            if self.resolve_arguments:
                source = template.Variable(source).resolve(context)
            output += '\n<script>!window.%s && document.write(unescape(\'%%3Cscript src="%s"%%3E%%3C/script%%3E\'))</script>' % (window_obj, source)
        return output


@register.tag
def load_js(parser, token):
    pieces = token.split_contents()[1:]
    if len(pieces) < 2:
        raise TemplateSyntaxError, '%s tag requires at least two arguments' % token.contents.split()[0]
    window_obj = pieces.pop(0)
    return LoadJsNode(window_obj, pieces)

    
@register.tag
def load_jquery(parser, token):
    sources = token.split_contents()[1:]
    if len(sources) < 1:
        sources = getattr(settings, 'JQUERY_SOURCES', _DEFAULT_JQUERY_SOURCES)
        return LoadJsNode('jQuery', sources, False)
    if not sources:
        raise TemplateSyntaxError, 'The %s tag requires a list of sources. You must either pass it arguments or set JQUERY_SOURCES in settings.py.' % token.contents.split()[0]
    return LoadJsNode('"jQuery"', sources, True)


@register.simple_tag
def html5boilerplate_static_prefix_setting():
    """
    For internal use only.
    """
    return _HTML5_BOILERPLATE_MEDIA_PREFIX