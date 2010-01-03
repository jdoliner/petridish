from django.template import Context, loader
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpRequest
from petridish.dish.models import Dish
from petridish.organism.models import Organism 

def new(request):
	from petridish.dish.models import Dish_form
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
			dish.fitness = function
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
	from petridish.evolver.views import register
	tools = [
	('My Dishes', reverse(dish)),
	('Populate', reverse(populate, args = [d_id])),
	('Register', reverse(register, args = [d_id])),
	('Properties', reverse(properties, args = [d_id])),
	('Clear', reverse(clear, args = [d_id])),
	('Delete', reverse(delete, args = [d_id])),
	]
	return tools

def dish_id_scrollers(d_id, generation):
	scrollers = []
	if (int(generation) != 0):
		scrollers.append(('|<<', reverse(dish_id, args = [d_id, 0])))
		scrollers.append(('<', reverse(dish_id, args = [d_id, int(generation) - 1])))
	scrollers.append(('-', reverse(dish_id, args = [d_id])))
	scrollers.append(('>', reverse(dish_id, args = [d_id, int(generation) + 1])))
	scrollers.append(('>>|', reverse(dish_id, args = [d_id])))
	return scrollers 

def dish_id(request, d_id, generation = -1):
	dish = Dish.objects.get(pk = d_id)
	if (generation == -1):
		generation = dish.generation
	organisms = dish.organisms(generation)
	return render_to_response('dish/dish_id.html', {'dish': dish, 'fitness_function': dish.fitness, 'organisms': organisms, 'tools': dish_id_toolbar(d_id), 'scrollers': dish_id_scrollers(d_id, generation)})

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

def go(request, d_id):
	dish = Dish.objects.get(pk = d_id)
	dish.new_generation()
	return redirect(dish_id, d_id = d_id)

def clear(request, d_id):
	dish = Dish.objects.get(pk = d_id)
	organisms = Organism.objects.filter(dish = dish)
	for o in organisms:
		o.unabstract().delete()
	dish.generation = 0
	dish.save()
	return redirect(dish_id, d_id = d_id)

def delete(request, d_id):
	clear(request, d_id)
	d = Dish.objects.get(pk = d_id)
	d.delete()
	return redirect(dish) 
