from django.template import Context, loader
from django.shortcuts import render_to_response
from petridish.graph.models import Graph, Breed

def graph_id(request, graph_id):
	G = Graph.objects.filter(pk = graph_id)[0]
	V = G.num_v
	E = G.e()
	template = loader.get_template('graph/graph_id.html')
	return render_to_response('graph/graph_id.html', {'organism': G, 'V' : V, 'E' : E})
def breed(request):
	if (request.method == 'POST'):
		form = Breed(request.POST)
		if form.is_valid():
			sire = form.cleaned_data['sire']
			dame = form.cleaned_data['dame']
			baby = sire.breed_subg_swp(dame)
			return graph_id(request, baby)
	else:
		form = Breed()
		return render_to_response('graph/breed.html', {'form': form})
