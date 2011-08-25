from django import template
from django.conf import settings
from django.template import TemplateSyntaxError
import re
try:
    from bs4 import BeautifulSoup
except ImportError:
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        raise    

import urllib


register = template.Library()

_HTML5_BOILERPLATE_STATIC_PREFIX = getattr(settings, 'HTML5_BOILERPLATE_STATIC_PREFIX', '/static/html5boilerplate/')
_DEFAULT_JQUERY_SOURCES = (
    '//ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.js',
    _HTML5_BOILERPLATE_STATIC_PREFIX + 'js/libs/jquery-1.5.1.min.js',
)


@register.inclusion_tag('html5boilerplate/includes/google_analytics.html',
                        takes_context=True)
def googleanalytics(context, ga_tracking_code=None):
    """
    The GA script.
    """
    if ga_tracking_code is None:
        ga_tracking_code = getattr(settings, 'GA_TRACKING_CODE', None)
    if ga_tracking_code is None:
        raise TemplateSyntaxError('The googleanalytics template tag requires a tracking code. You must either pass it as an argument or set GA_TRACKING_CODE in settings.py.')
        
    return {
        'ga_tracking_code': ga_tracking_code,
    }


class TagVariantsNode(template.Node):
    
    VARIANTS = (
        ('ie6', '<!--[if lt IE 7 ]>', '<![endif]-->'),
        ('ie7', '<!--[if IE 7 ]>', '<![endif]-->'),
        ('ie8', '<!--[if IE 8 ]>', '<![endif]-->'),
        ('', '<!--[if (gte IE 9)|!(IE)]><!-->', '<!--<![endif]-->'),
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


def _generate_js_embed(tag_name, test_obj, html):
    soup = BeautifulSoup(html)

    tags = []
    for tag in soup.findAll():
        if tag.name != 'script':
            raise TemplateSyntaxError, '%s can only contain script tags.' % tag_name
        else:
            tags.append(tag)

    prop_chain = test_obj.split('.')
    conditions = []
    for i in range(len(prop_chain)):
        conditions.append('window.%s' % '.'.join(prop_chain[:i + 1]))
    teststr = ' && '.join(conditions)
    output = ''
    for tag in tags:
        escaped_tag = urllib.quote(str(tag)).replace("'", r"\'")
        output += '\n<script>%s || document.write(unescape(\'%s\'));</script>' % (teststr, escaped_tag)
    return output


class LoadJsUntilNode(template.Node):
    def __init__(self, test_obj, nodelist):
        self.test_obj, self.nodelist = test_obj, nodelist
    
    def render(self, context):
        html = self.nodelist.render(context)
        test_obj = template.Variable(self.test_obj).resolve(context)
        return _generate_js_embed('loadjsuntil', test_obj, html)


@register.tag
def loadjsuntil(parser, token):
    """
    Allows you to specify a list of sources from which a JavaScript library
    should be loaded. Each source will be tried until one successfully results
    in the creation of the specified window-level object.
    
    Usage:
    
    {% loadjsuntil "jQuery.ui" %}
        <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.8.14/jquery-ui.js" type="text/javascript" charset="utf-8"></script>
	    <script src="{{ STATIC_URL }}main/js/libs/jquery-ui.min.js" type="text/javascript" charset="utf-8"></script>
	{% endloadjsuntil %}
	"""
    nodelist = parser.parse(('endloadjsuntil',))
    parser.delete_first_token()
    args = token.split_contents()[1:]
    tag_name = token.contents.split()[0]
    if len(args) < 1:
        raise TemplateSyntaxError, '%s tag requires a window-level object to test for.' % tag_name
    elif len(args) != 1:
        raise TemplateSyntaxError, '%s tag accepts exactly 1 argument.' % tag_name
    test_obj = args[0]
    return LoadJsUntilNode(test_obj, nodelist)

    
@register.simple_tag
def loadjquery():
    """
    Loads jQuery from the paths specified in JQUERY_SOURCES
    """
    html = ''
    for source in getattr(settings, 'JQUERY_SOURCES', _DEFAULT_JQUERY_SOURCES):
        html += '<script src="%s" type="text/javascript" charset="utf-8"></script>' % source
    return _generate_js_embed('loadjquery', 'jQuery', html)


@register.simple_tag
def html5boilerplate_static_prefix_setting():
    """
    For internal use only.
    """
    return _HTML5_BOILERPLATE_STATIC_PREFIX
