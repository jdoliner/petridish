from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),
	(r'^graph/(?P<graph_id>\d+)/$', 'petridish.graph.views.graph_id'),
	(r'^dish/(?P<dish_id>\d+)/$', 'petridish.dish.views.dish_id'),
	(r'^dish/(?P<dish_id>\d+)/generation=(?P<generation>\d+)/$', 'petridish.dish.views.dish_id'),
	(r'^organism/(?P<organism_id>\d+)/$', 'petridish.organism.views.organism_id'),
)
