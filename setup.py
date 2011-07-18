import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.markdown')

setup(
    name = "django-html5boilerplate",
    version = "0.1",
    description='Provides an easy way to use Paul Irish\'s HTML5 Boilerplate in Django projects.',
    url = 'http://github.com/matthewwithanm/django-html5boilerplate',
    license = 'BSD',
    long_description=README,

    author = 'Matthew Tretter',
    author_email = 'matthew@exanimo.com',
    packages = [
        'html5boilerplate',
        'html5boilerplate.templates',
        'html5boilerplate.templatetags',
    ],
    package_data = {'html5boilerplate': ['templates/*', 'static/*']},
    install_requires = ['BeautifulSoup>=3.2.0'], # TODO: Relax this requirement a bit. I'm sure it works with a much earlier version.
    zip_safe = False,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)