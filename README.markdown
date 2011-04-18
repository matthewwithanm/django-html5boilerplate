django-html5boilerplate
=======================

This project is a packaging of Paul Irish's HTML5 Boilerplate for Django
projects. It contains a base template, the required media, and—most
importantly—a collection of template tags so you can easily integrate all of
the boilerplate's tricks into your pages if the template starts to feel too
restrictive.

Installation
------------

Add `html5boilerplate` to `INSTALLED_APPS` in settings.py. If you plan to
make use of the included media (bundled JavaScript and CSS files), either copy
the media folder to your project or duplicate whatever setup you're using for
your admin media files (collectstatic, symlink, server alias, etc.)

Usage
--------

You can either extend the included template ("html5boilerplate/base.html"), or
create your own using the included template tags, which can be loaded using
`{% load html5boilerplate_tags %}`. Here is a list of the included tags:

<dl>
	<dt>google_analytics</dt>
	<dd>Embeds the GA tracking script. You can either pass it your tracking
		code, or set `GA_TRACKING_CODE` in settings.py</dd>
	<dt>tagvariants</dt>
	<dd>Creates duplicates of the wrapped opening tag, each wrapped in an IE
		conditional comment, with an added class identifying the version of IE.
		For example:
		<pre><code>{% tagvariants %}&lt;html lang="en" class="whatever">{% endtagvariants%}</code></pre>
		would result in the following:
		<pre><code>&lt;!--[if lt IE 7 ]>&lt;html lang="en" class="ie6 whatever">&lt;![endif]-->
&lt;!--[if IE 7 ]>&lt;html lang="en" class="ie7 whatever">&lt;![endif]-->
&lt;!--[if IE 8 ]>&lt;html lang="en" class="ie8 whatever">&lt;![endif]-->
&lt;!--[if IE 9 ]>&lt;html lang="en" class="ie9 whatever">&lt;![endif]-->
&lt;!--[if (gt IE 9)|!(IE)]>&lt;!-->&lt;html lang="en" class="whatever">&lt;!--&lt;![endif]--></code></pre>
		
		This would usually be used on the `&lt;html>` tag, and allows you to
		easily target versions of your favorite browser.
	</dd>
	<dt>load_jquery</dt>
	<dd>Loads jQuery by trying each item in a list of sources until one is
		successful. By default, this tag will first try to load the library
		from Google's CDN and then—if it fails—will load the bundled copy.
		However, you can override this behavior by either passing a list of
		sources to the tag or setting `JQUERY_SOURCES` in settings.py.
	</dd>
</dl>

Settings
--------

This application supports the following settings:

<dl>
	<dt>GA_TRACKING_CODE</dt>
	<dd>A default tracking code to use for the `google_analytics` template tag.
		If this is set, you can use the template tag without arguments.</dd>
	<dt>JQUERY_SOURCES</dt>
	<dd>A list of sources that jQuery can be found at, in the order in which
		they should be tried. If this is set, you can use the `load_query` tag
		without arguments.</dd>
	<dt>HTML5_BOILERPLATE_STATIC_PREFIX</dt>
	<dd>A prefix to be used for the bundled media urls. By default, the
		template will use "/static/html5boilerplate/".</dd>
</dl>