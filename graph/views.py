from django.template import Context, loader
from django.http import HttpResponse
from petridish.graph.models import Graph

def graph_id(request, graph_id):
	G = Graph.objects.filter(pk = graph_id)[0]
	V = G.v()
	E = G.e()
	template = loader.get_template('graph/graph_id.html')
	context = Context({'V' : V, 'E' : E})
	return HttpResponse(template.render(context))
