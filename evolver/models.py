from django.db import models
from django import forms

class Evolver(models.Model):
	name = models.CharField(max_length = 20)
	def __unicode__(self):
		return map(lambda d: x.name, self.dishes())
	def dishes(self):
		from petridish.dish.models import Dish
		return Dish.objects.filter(evolver = self)
	def run(self):
		while(1):
			for dish in self.dishes():
				if(dish.fitness_cap <= dish.best_fitness()):
					dish.new_generation()
				else:
					dish.unregister()
	def ping(self, dish):
		pass

class Evolver_register_form(forms.Form):
	evolvers = Evolver.objects.all()
	evolvers = forms.ChoiceField(map(lambda e: (e.id, e.name), evolvers))
