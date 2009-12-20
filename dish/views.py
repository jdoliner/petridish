from django.template import Context, loader
from django.http import HttpResponse
from petridish.dish.models import Dish

def dish_id(request, dish_id):
	dish = Dish.objects.filter(pk = dish_id)[0]
	organisms = dish.organisms()
	template = loader.get_template('dish/dish_id.html')
	context = Context({'dish': dish, 'organisms': organisms})
	return HttpResponse(template.render(context))
