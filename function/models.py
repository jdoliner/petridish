from django.db import models
from petridish.organism.models import Organism
import re

class Function(models.Model):
	name = models.CharField(max_length=20)
	num_args = models.IntegerField()
	code = models.TextField()
	def parse(self, code):
		parse = re.search(r'^def (\w+)\(([a-zA-Z0-9_, ]*)\):(.*)', code, re.DOTALL)
		self.name = parse.group(1)
		self.num_args = len(re.findall(r'([a-zA-Z0-9_]+)\s*(?:,|$)', parse.group(2)))
		self.code = code
		self.save()
	def call(self, args):
		if (len(args) != self.num_args):
			assert(0)
		import pdb
		pdb.set_trace()
		code = self.code + '\n' + 'function_name_dummy = ' + self.name + '\n'
		try:
			exec(code)
		except:
			pass
		else:
			pass
			#return function_name_dummy(args)

class Fitness_Function(Function):
	def eval_fitness(self):
		organisms = Organism.objects.filter(generation = self.generation)
		for o in organisms:
			try:
				try:
					o.graph
				except:
					pass
				else:
					o.fitness = self.call(o.graph)
					o.save()
					continue
				o.fitness = 0
			except:
				#we get here if the function call fails
				o.fitness = -1 
			o.save()
