from django.template import Context, loader
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpRequest
from petridish.dish.models import Dish
from petridish.organism.models import Organism 

def new(request):
	from petridish.models import Dish_form
	if (request.method == 'POST'):
		form = Dish_form(request.POST)
		if(form.is_valid()):
			name = form.cleaned_data['name']
			dish = Dish()
			dish.init(name)
			dish.save()
			return redirect(dish_id, d_id = dish.id)
	else:
		form = Dish_form()
		return render_to_response('dish/new.html', {'action': reverse(new), 'form': form})

def properties(request, d_id):
	from petridish.dish.models import Properties_form
	if (request.method == 'POST'):
		form = Properties_form(request.POST)
		if(form.is_valid()):
			from petridish.function.models import Fitness_Function
			dish = Dish.objects.get(pk = d_id)
			dish.name = form.cleaned_data['name']
			id = form.cleaned_data['fitness_f']
			function = Fitness_Function.objects.get(id = id)
			dish.function = function
			dish.save()
			return redirect(dish_id, d_id = dish.id)
	else:
		form = Properties_form()
		return render_to_response('dish/properties.html', {'action': reverse(properties, args = [d_id]), 'form': form})

def dishes_toolbar():
	tools = []
	tools.append(('New', reverse(new)))
	return tools

def dish(request):
	dishes = Dish.objects.all()
	return render_to_response('dish/dish.html', {'dishes': dishes, 'tools': dishes_toolbar()})
	

def dish_id_toolbar(d_id):
	tools = []
	tools.append(('My Dishes', reverse(dish))),
	tools.append(('Populate', reverse(populate, args = [d_id])))
	tools.append(('Properties', reverse(properties, args = [d_id])))
	tools.append(('Clear', reverse(clear, args = [d_id])))
	tools.append(('Delete', reverse(delete, args = [d_id])))
	return tools

def dish_id(request, d_id):
	dish = Dish.objects.get(pk = d_id)
	organisms = Organism.objects.filter(dish = dish)
	template = loader.get_template('dish/dish_id.html')
	context = Context({'dish': dish, 'fitness_function': dish.fitness, 'organisms': organisms, 'tools': dish_id_toolbar(d_id)})
	return HttpResponse(template.render(context))

def populate(request, d_id):
	from petridish.dish.models import Populate_form
	from petridish.graph.views import populate as graph_populate
	if (request.method == 'POST'):
		form = Populate_form(request.POST)	
		if(form.is_valid()):
			type = form.cleaned_data['type']
			if (type == 'graph'):
				req = HttpRequest()
				req.method = 'GET'
				return(graph_populate(req, d_id))
			else:
				pass #this should be an error
	else:
		form = Populate_form()
		return render_to_response('dish/populate.html', {'action': reverse(populate, args = [d_id]), 'form': form})		

def clear(request, d_id):
	dish = Dish.objects.get(pk = d_id)
	organisms = Organism.objects.filter(dish = dish)
	for o in organisms:
		try:
			o.graph
		except:
			pass
		else:
			o.graph.delete()
	return dish_id(request, d_id)

def delete(request, d_id):
	clear(request, d_id)
	dish = Dish.objects.get(pk = d_id)
	dish.delete()
	return redirect(dish) 
