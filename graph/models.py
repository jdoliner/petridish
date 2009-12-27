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
		selfv = range(self.num_v)
		selfe = self.e()
		matev = range(self.num_v, self.num_v + mate.num_v)
		matee = mate.e()
		matee = map(lambda e: (e[0] + self.num_v, e[1] + self.num_v), matee)
		#select a subset of the vertices to induce subgraphs
		selfsubg = random.sample(selfv, random.randrange(len(selfv))+1)
		selfcomp = list(set(selfv) - set(selfsubg))
		matesubg = random.sample(matev, random.randrange(len(matev))+1)
		matecomp = list(set(selfv) - set(selfsubg))
		#which edges are entirely internal
		selfe_internal = filter(lambda e: e[0] in selfv and e[1] in selfv, selfe)
		matee_internal = filter(lambda e: e[0] in matev and e[1] in matev, matee)
		#edges that start in the subgraph but go outside
		selfe_cross = filter(lambda e: e[0] in selfv and not e[1] in selfv, selfe)
		matee_cross = filter(lambda e: e[0] in matev and not e[1] in matev, matee)
		#associations to reconnect the subgraphs; map from selfcomp->matesubg and matecomp->selfsubg
		self_to_mate = {}
		for i in range(len(selfcomp)):
			self_to_mate[selfcomp[i]] = matesubg[i%len(matesubg)]
		mate_to_self = {}
		for i in range(len(matecomp)):
			mate_to_self[matecomp[i]] = selfsubg[i%len(selfsubg)]
		for e in selfe_cross:
			e[1] = self_to_mate[e[1]]
		for e in matee_cross:
			e[1] = mate_to_self[e[1]]
		g = Graph()
		g.init(self.dish, self.generation + 1)
		g.num_v = len(selfsubg) + len(matesubg)
		g.adde(selfe_internal + matee_internal + selfe_cross + matee_cross)
	def random(self, size, p):
		self.num_v = size
		edges = []
		for fr in range(size):
			for to in range(size):
				if(random.random() < p and fr != to):
					edges.append((fr,to))
		self.cleare()
		self.adde(edges)
