from django.db import models

from petridish.organism.models import Organism

# Create your models here.

class Dish(models.Model):
	name = models.CharField(max_length=200)
	generation = models.IntegerField()
	born = models.DateTimeField('birthdate')
	def __unicode__(self):
		return self.name
	def organisms(self):
		return Organism.objects.filter(dish=self.pk, generation = self.generation)
