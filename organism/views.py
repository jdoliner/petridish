from django.template import Context, loader
from django.http import HttpResponse
from petridish.organism.models import Organism
from petridish.graph.views import graph_id

def organism_id(request, organism_id):
	organism = Organism.objects.get(pk = organism_id)
	try:
		organism.graph
	except organism.DoesNotExist:
		pass
	else:
		return graph_id(request, organism_id)
	template = loader.get_template('organism/organism_id.html')
	context = Context({'organism': organism})
	return HttpResponse(template.render(context))
