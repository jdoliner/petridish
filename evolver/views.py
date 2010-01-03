from django.shortcuts import redirect, render_to_response
from django.core.urlresolvers import reverse

def register(request, d_id):
	from petridish.dish.models import Dish
	from petridish.evolver.models import Evolver_register_form
	dish = Dish.objects.get(id = d_id)
	if(request.method == 'POST'):
		form = Evolver_register_form(request.POST)
		if(form.is_valid()):
			from petridish.evolver.models import Evolver
			dish.register(Evolver.objects.get(id = form.cleaned_data['evolver']))
			return redirect(dish_id, d_id = dish.id)
	else:
		form = Evolver_register_form()
		return render_to_response('evolver/register.html', {'action': reverse(register, args = [d_id]), 'form': form})
