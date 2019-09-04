'''
based on graph implementation from here:
https://runestone.academy/runestone/books/published/pythonds/Graphs/Implementation.html
'''

import tkinter as tk
from math import sqrt
from random import randint

node_r = 10

def main():
	class Vertex():
		def __init__(self, key):
			self.id = key
			self.connectedTo = {}

		def addNeighbor(self, nbr, weight=0):
			self.connectedTo[nbr] = weight

		def __str__(self):
			return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

		def getConnections(self):
			return self.connectedTo.keys()

		def getId(self):
			return self.id

		def getWeight(self,nbr):
			return self.connectedTo[nbr]

	class graph:
		def __init__(self):
			self.vertList = {}
			self.numVertices = 0

		def addVertex(self,key):
			self.numVertices = self.numVertices + 1
			newVertex = Vertex(key)
			self.vertList[key] = newVertex
			return newVertex

		def getVertex(self,n):
			if n in self.vertList:
				return self.vertList[n]
			else:
				return None

		def __contains__(self,n):
			return n in self.vertList

		def addEdge(self,f,t,cost=0):
			if f not in self.vertList:
				nv = self.addVertex(f)
			if t not in self.vertList:
				nv = self.addVertex(t)
			self.vertList[f].addNeighbor(self.vertList[t], cost)

		def getVertices(self):
			return self.vertList.keys()

		def __iter__(self):
			return iter(self.vertList.values())

	def drawCircle(x, y):
		x0 = x - node_r
		y0 = y - node_r
		x1 = x + node_r
		y1 = y + node_r
		return c.create_oval(x0, y0, x1, y1, fill='black', tags=(x,y))

	def drawLine(x0, y0, x1, y1):
		return c.create_line(x0, y0, x1, y1)

	root = tk.Tk()
	root.attributes('-fullscreen', True)
	width, height = root.winfo_screenwidth(), root.winfo_screenheight()


	main_graph = graph()
	selected_node = True

	def callback(event):
		mouse_x, mouse_y = event.x, event.y

		if main_graph.numVertices == 0: #place first node
			node = drawCircle(mouse_x, mouse_y)
			main_graph.addVertex(node)
		else: #place subsequent nodes
			print(selected_node)
			if not selected_node: #first, select node to branch from
				found_node = c.find_closest(mouse_x, mouse_y)
				found_x = int((c.coords(found_node)[2] + c.coords(found_node)[0])/2)
				found_y = int((c.coords(found_node)[3] + c.coords(found_node)[1])/2)
				dist = sqrt((found_x-mouse_x)**2 + (found_y-mouse_y)**2)
				if dist <= node_r:
					c.itemconfig(found_node, fill='grey')
					selected_node = found_node
			else: #then create a neighbor node
				node = drawCircle(mouse_x, mouse_y)
				main_graph.addVertex(node)
				c.itemconfig(selected_node, fill='black')
				selected_node = None


	def motion(event):
		mouse_x, mouse_y = event.x, event.y

	c = tk.Canvas(root, width=width, height=height)
	root.bind('<Button-1>', callback)
	root.bind('<Motion>', motion)
	c.pack()

	root.mainloop()

if __name__== "__main__":
	main()
