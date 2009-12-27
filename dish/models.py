from django.db import models

class Dish(models.Model):
	name = models.CharField(max_length=200)
	generation = models.IntegerField()
	born = models.DateTimeField('birthdate')
	def __unicode__(self):
		return self.name
