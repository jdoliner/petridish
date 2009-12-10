from django.db import models

try:
	from petridish.organism.models import Organism
except:
	pass

# Create your models here.

class Dish(models.Model):
	name = models.CharField(max_length=200)
	generation = models.IntegerField()
	born = models.DateTimeField('birthdate')
	def __unicode__(self):
		return self.name
	def organisms(self):
		return Article.objects.filter(dish=self.pk, generation = self.generation)
