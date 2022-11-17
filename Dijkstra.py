
import numpy as np
from ColaPrioridad import *
import pygame, random, math
pygame.init()
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("circulo")

class Grafo:
	def __init__(self, origen=[], destino=[], peso=[], dirigido=False):
		self.origen		= np.array(origen)
		self.destino	= np.array(destino)
		self.costo		= np.array(peso)
		if not dirigido:
			self.origen		= np.concatenate([origen, destino])
			self.destino	= np.concatenate([destino, origen])
			self.costo		= np.concatenate([peso, peso])
		self.numNodos	= len(self.origen)
        
	def muestra(self):
		print("inicio: ",	self.origen)
		print("fin:    ",	self.destino)
		print("Costo:  ",	self.costo)
		print("Número de Nodos:   ", self.numNodos)
		
	def defineVisitados(self):
		visitados = []
		for i in range(self.numNodos): visitados.append(False)
		return visitados
		
	def __recRec(self, rec, fin):
		recorrido = []
		recorrido.append(fin)
		sig = rec[fin]
		while sig != -1:
			recorrido.insert(0, sig)
			sig = rec[sig]
		return recorrido

	#---------------------------------------------------------------
	def __vertAdyNoVisitados(self, actual, visitados, minCos, padre, cola):
		for j in range(len(self.origen)):
			if int(self.origen[j])==actual and visitados[int(self.destino[j])]==False: 
				if minCos[int(self.destino[j])]>minCos[actual]+self.costo[j] :
					# se toma si el costo es menor a través del nodo actual
					minCos[int(self.destino[j])] = minCos[actual]+self.costo[j]
					padre[int(self.destino[j])] = actual # la mejora se obtuvo a través de actual
					cola.push((self.destino[j], minCos[int(self.destino[j])])) # se da de alta en la cola		

	#-------algoritmo de los caminos mas cortos dado un origen------
	def Dijkstra(self, ini, fin):
		#djg	= Grafo(self.origen, self.destino, self.costo)
		minCos	= [] #variable de costo minimo 
		padre	= [] 
		arc		= 0 # contador de arcos 
		cola	= ColaPrioridad() 
		visitados = self.defineVisitados()
        
		for i in range(self.numNodos):
			padre.append(-1)
			minCos.append(1000000)

		minCos[ini] = 0	# registro de los datos del origen
		padre[ini]  = -1
		actual = ini    # el nodo inicial es el nodo actual
		cola.push((ini,0))  # se da de alta en la cola de prioridades
		nVerts = self.numNodos
		
		while arc<=nVerts and not cola.isEmpty() and actual!=fin:
			if not visitados[cola.peek()]: 
				actual = cola.pop()  # define nodo actual al del frente de la cola
				#print(arc)
				visitados[actual] = True  # lo marca como visitado
				self.__vertAdyNoVisitados(actual, visitados, minCos, padre, cola)
				arc = arc+1 # cuenta un arco mas
			else: cola.pop() # se elimina el nodo de la cola 
		return self.__recRec(padre, fin)  
