from django.db import models
import datetime
from petridish.dish.models import Dish

# Create your models here.

class Organism(models.Model):
	born = models.DateTimeField('birthdate')
	dish = models.ForeignKey('dish.Dish')
	generation = models.IntegerField()
	fitness = models.IntegerField()
	def init(self, dish, generation):
		self.fitness = 0
		self.born = datetime.datetime.now()
		if (type(dish) == Dish):
			self.dish = dish
		else:
			self.dish = Dish.objects.get(id = dish)
		self.generation = generation
	def unabstract(self):
		try:
			self.graph
		except:
			pass
		else:
			return self.graph
		assert(0)
	def breed(self, mate):
		return self.unabstract().breed(mate.unabstract())
