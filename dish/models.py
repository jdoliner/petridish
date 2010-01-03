from django.db import models
from django import forms

class Dish(models.Model):
	name = models.CharField(max_length=20)
	fitness = models.ForeignKey('function.Fitness_Function', null=True)
	fitness_cap = models.IntegerField(null = True)
	evolver = models.ForeignKey('evolver.Evolver', null = True)
	generation = models.IntegerField()
	born = models.DateTimeField('birthdate')
	def __unicode__(self):
		return self.name
	def init(self, name):
		from datetime import datetime
		self.name = name
		self.generation = 0
		self.born = datetime.now()
	def organisms(self, generation = -1):
		if (generation == -1):
			generation = self.generation
		from petridish.organism.models import Organism
		return Organism.objects.filter(dish = self, generation = generation).extra(order_by = ['-fitness'])
	def eval_fitness(self):
		from petridish.function.models import Fitness_Function
		for o in self.organisms():
			try:
				o.fitness = self.fitness.call([o.unabstract()])
			except:
				o.fitness = 0
			o.save()
	def best_fitness(self):
		return self.organisms()[0].fitness
	def breed(self, target_pop_size):
		for i in range(target_pop_size):
			organisms = self.organisms()
			total_fitness = 0
			for o in organisms:
				total_fitness = total_fitness + o.fitness
			from random import randrange
			i1, i2 = randrange(total_fitness), randrange(total_fitness)
			org1, org2 = None, None
			for organism in organisms:
				if (org1 and org2):
					break
				i1 = i1 - organism.fitness
				i2 = i2 - organism.fitness
				if (i1 < 0 and org1 == None):
					org1 = organism
				if (i2 < 0 and org2 == None):
					org2 = organism
			new_org = org1.breed(org2)
			new_org.save()
		self.generation = self.generation + 1
		self.save()
	def new_generation(self):
		self.breed(len(self.organisms()))
		self.eval_fitness()
	def register(self, evolver):
		self.evolver = evolver
		self.save()
		evolver.ping(self)
	def unregister(self):
		self.evolver = None
		self.save()
		

class Dish_form(forms.Form):
	name = forms.CharField(max_length=20)

class Populate_form(forms.Form):
	type = forms.ChoiceField([('graph', 'graph')])

class Properties_form(forms.Form):
	from petridish.function.models import Fitness_Function
	name = forms.CharField(max_length=20)
	functions = Fitness_Function.objects.all()
	#fitness_f = forms.ChoiceField(map(lambda f: (f.id, f.name), functions))
