from django.template import Context, loader
from django.http import HttpResponse
from petridish.dish.models import Dish
from petridish.organism.models import Organism

def dish_id(request, dish_id):
	dish = Dish.objects.get(pk = dish_id)
	organisms = Organism.objects.filter(dish = dish)
	template = loader.get_template('dish/dish_id.html')
	context = Context({'dish': dish, 'organisms': organisms})
	return HttpResponse(template.render(context))
