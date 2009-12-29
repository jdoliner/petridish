from django.template import Context, loader
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from petridish.graph.models import Graph, Breed_form, Populate_form, Populate
from petridish.dish.views import dish_id

def graph_id(request, graph_id):
	G = Graph.objects.filter(pk = graph_id)[0]
	V = G.num_v
	E = G.e()
	template = loader.get_template('graph/graph_id.html')
	return render_to_response('graph/graph_id.html', {'organism': G, 'V' : V, 'E' : E})

def breed(request):
	if (request.method == 'POST'):
		form = Breed_form(request.POST)
		if form.is_valid():
			sire = form.cleaned_data['sire']
			dame = form.cleaned_data['dame']
			baby = sire.breed_subg_swp(dame)
			return graph_id(request, baby)
	else:
		form = Breed_form()
		return render_to_response('graph/breed.html', {'form': form})

def populate(request, d_id):
	if (request.method == 'POST'):
		form = Populate_form(request.POST)
		if form.is_valid():
			pop_size = form.cleaned_data['pop_size']
			graph_size = form.cleaned_data['graph_size']
			p = form.cleaned_data['p']
			Populate(d_id, pop_size, graph_size, p)
			return dish_id(request, d_id) 
	else:
		form = Populate_form()
		return render_to_response('graph/populate.html', {'action' : reverse(populate, args = [d_id]), 'form' : form})
