django-html5boilerplate
=======================

This project is a packaging of Paul Irish's HTML5 Boilerplate for Django
projects. It contains a base template, the required media, and—most
importantly—a collection of template tags so you can easily integrate all of
the boilerplate's tricks into your pages if the template starts to feel too
restrictive.

The bundled media and templates correspond to the [1.0 release][1] of HTML5 Boilerplate.

Installation
------------

Add `html5boilerplate` to `INSTALLED_APPS` in settings.py. If you plan to
make use of the included media (bundled JavaScript and CSS files), don't forget
to run `collectstatic` (or copy the media folder if you're using an older
version of Django (< 1.3)).

Usage
--------

You can either extend the included template ("html5boilerplate/base.html"), or
create your own using the included template tags, which can be loaded using
`{% load html5boilerplate_tags %}`.


Template Tags
-------------

### googleanalytics

Embeds the GA tracking script. You can either pass it your tracking code, or set
`GA_TRACKING_CODE` in settings.py

### tagvariants

Creates duplicates of the wrapped opening tag, each wrapped in an IE conditional
comment, with an added class identifying the version of IE.

For example:

    {% tagvariants %}<html lang="en" class="whatever">{% endtagvariants%}

would result in the following:

	<!--[if lt IE 7 ]><html lang="en" class="ie6 whatever"><![endif]-->
	<!--[if IE 7 ]><html lang="en" class="ie7 whatever"><![endif]-->
	<!--[if IE 8 ]><html lang="en" class="ie8 whatever"><![endif]-->
	<!--[if IE 9 ]><html lang="en" class="ie9 whatever"><![endif]-->
	<!--[if (gt IE 9)|!(IE)]><!--><html lang="en" class="whatever"><!--<![endif]-->
		
This would usually be used on the `<html>` tag, and allows you to easily
target versions of your favorite browser.

### loadjquery

Loads jQuery by trying each item in a list of sources until one is successful.
By default, this tag will first try to load the library from Google's CDN and
then—if it fails—will load the bundled copy. However, you can specify your own
sources by setting `JQUERY_SOURCES` in settings.py.

### loadjsuntil

A more generic version of `loadjquery`, useful for providing fallback sources
for any library. Example:

	{% loadjsuntil "jQuery.ui" %}
    	<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.8.14/jquery-ui.js" type="text/javascript" charset="utf-8"></script>
    	<script src="{{ STATIC_URL }}js/jquery-ui.min.js" type="text/javascript" charset="utf-8"></script>
	{% endloadjsuntil %}

The tag accepts one argument, which specifies a window-level object whose
existence indicates the library has been successfully loaded. The contents of
the tag are script nodes that will be written to the DOM until the object
exists.


Settings
--------

This application supports the following settings:

<dl>
	<dt>GA_TRACKING_CODE</dt>
	<dd>A default tracking code to use for the <code>googleanalytics</code>
		template tag. If this is set, you can use the template tag without
		arguments.</dd>
	<dt>JQUERY_SOURCES</dt>
	<dd>A list of sources that the `loadjquery` tag should use.</dd>
	<dt>HTML5_BOILERPLATE_STATIC_PREFIX</dt>
	<dd>A prefix to be used for the bundled static file urls. By default, the
		template will use "/static/html5boilerplate/".</dd>
</dl>

[1]:https://github.com/paulirish/html5-boilerplate/tree/v1.0stripped