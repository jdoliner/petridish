from django.db import models
import random
import re
from petridish.organism.models import Organism

class Graph(Organism):
	num_v = models.IntegerField()
	edges = models.TextField()
	regex = re.compile('{(\d*),(\d*)}')
	def e(self):
		return map(lambda x: (int(x[0]), int(x[1])), self.regex.findall(self.edges))
	def addv(self):
		self.v = self.v + 1
		self.save()
	def adde(self, edges):
		newedges = ''
		for edge in edges:
			fr = edge[0]
			to = edge[1]
			if (fr > (self.num_v-1) or to > (self.num_v-1)):
				pass
			else:
				newedges = newedges + '{' + str(fr) + ',' + str(to) + '}'
		self.edges = self.edges + newedges
		self.save()
	def cleare(self):
		self.edges = ''
		self.save()
	def breed_subg_swp(self, mate):
		selfv = self.v()
		matev = mate.v()
		#select a subset of the vertices to induce subgraphs
		selfsubg = random.sample(selfv, random.randrange(len(selfv))+1)
		selfcomp = list(set(selfv) - set(selfsubg))
		matesubg = random.sample(matev, random.randrange(len(matev))+1)
		matecomp = list(set(selfv) - set(selfsubg))
		#which edges are entirely internal
		selfe_internal = self.e().filter(fr__in=selfsubg, to__in=selfsubg)
		matee_internal = mate.e().filter(fr__in=selfsubg, to__in=selfsubg)
		#edges that start in the subgraph but go outside
		selfe_cross = self.e().filter(fr__in=selfsubg).filter(to__in=selfcomp) 
		matee_cross = mate.e().filter(fr__in=matesubg).filter(to__in=matecomp)
		#associations to reconnect the subgraphs; map from selfcomp->matesubg and matecomp->selfsubg
		self_to_mate = {}
		for i in range(len(selfcomp)):
			self_to_mate[selfcomp[i]] = matesubg[i%len(matesubg)]
		mate_to_self = {}
		for i in range(len(matecomp)):
			mate_to_self[matecomp[i]] = selfsubg[i%len(selfsubg)]
		for e in selfe_cross:
			e.to = self_to_mate[e.to]
		for e in matee_cross:
			e.to = mate_to_self[e.to]
		g = Graph()
		g.dish = self.dish
		g.G(list(selfsubg) + list(matesubg), list(selfe_internal) + list(matee_internal) + list(selfe_cross) + list(matee_cross))
	def random(self, size, p):
		self.num_v = size
		edges = []
		for fr in range(size):
			for to in range(size):
				if(random.random() < p and fr != to):
					edges.append((fr,to))
		self.cleare()
		self.adde(edges)
