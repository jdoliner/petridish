from django.template import Context, loader
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpRequest
from petridish.dish.models import Dish, Populate_form
from petridish.organism.models import Organism 

def toolbar(dish_id):
	tools = []
	tools.append(('Populate', reverse(populate, args = [dish_id])))
	tools.append(('Clear', reverse(clear, args = [dish_id])))
	return tools

def dish_id(request, dish_id):
	dish = Dish.objects.get(pk = dish_id)
	organisms = Organism.objects.filter(dish = dish)
	template = loader.get_template('dish/dish_id.html')
	context = Context({'dish': dish, 'organisms': organisms, 'tools': toolbar(dish_id)})
	return HttpResponse(template.render(context))

def populate(request, dish_id):
	from petridish.graph.views import populate as graph_populate
	if (request.method == 'POST'):
		form = Populate_form(request.POST)	
		if(form.is_valid()):
			type = form.cleaned_data['type']
			if (type == 'graph'):
				req = HttpRequest()
				req.method = 'GET'
				return(graph_populate(req, dish_id))
			else:
				pass #this should be an error
	else:
		form = Populate_form()
		return render_to_response('dish/populate.html', {'action': '/dish/' + str(dish_id) + '/populate/', 'form': form})		

def clear(request, dish_id):
	dish - Dish.objects.get(pk = dish_id)
	organisms = Organism.objects.filter(dish = dish)
	for o in organisms:
		try:
			o.graph
		except:
			pass
		else:
			o.graph.delete()
		o.delete()
	return dish_id(request, dish_id)
