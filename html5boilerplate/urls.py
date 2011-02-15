from django.conf.urls.defaults import *
import views

urlpatterns = patterns(views.__name__,
)

urlpatterns += patterns('django.views.generic.simple',
    (r'crossdomain.xml', 'direct_to_template', {'template': 'html5boilerplate/crossdomain.xml'}),
    (r'robots.txt', 'direct_to_template', {'template': 'html5boilerplate/robots.txt'}),
)
