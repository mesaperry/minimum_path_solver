'''
based on graph implementation from here:
https://runestone.academy/runestone/books/published/pythonds/Graphs/Implementation.html
'''

import tkinter as tk
from math import sqrt

node_r = 10 #size of node circles

class Vertex:
	def __init__(self, data):
		self.data = data
		self.connected_to = {}

	def addConnected(self, vert, edge_data):
		self.connected_to[vert] = edge_data

	def getConnectedVert(self):
		return self.connectedTo.keys()

	def getConnectedEdge(self):
		return self.connectedTo.values()

	def getData(self):
		return self.data

class Graph:
	def __init__(self):
		self.vertices = {}
		self.numVertices = 0

	def addVert(self,data):
		self.numVertices = self.numVertices + 1
		newVertex = Vertex(data)
		self.vertices[newVertex] = data
		return newVertex

	def addEdge(self,v1,v2,edge_data=None):
		v1.addConnected(v2, edge_data)
		v2.addConnected(v1, edge_data)

	def getData(self,vertex):
		if vertex in self.vertices.keys:
			return self.vertices[vertex]
		else:
			return None

	def getVert(self,data):
		for key, value in self.vertices.items():
			if value == data:
				vert = key
				return vert

	def getVertices(self):
		return self.vertices.keys()


def main():
	root = tk.Tk()
	root.title = 'nodal-maze'
	root.attributes('-fullscreen', True)
	width, height = root.winfo_screenwidth(), root.winfo_screenheight()

	canvas = tk.Canvas(root, width=width, height=height)
	canvas.pack()

	class App:
		def __init__(self, canvas):
			self.c = canvas
			self.g = Graph()
			self.selected_node = None

			self.c.bind('<Button-1>', self.canvasClick)
			# self.c.tag_bind(canvas_item_id ,'<ButtonPress-1>', self.itemClicked)

		def drawCircle(self, x, y):
			x0 = x - node_r
			y0 = y - node_r
			x1 = x + node_r
			y1 = y + node_r
			return self.c.create_oval(x0, y0, x1, y1, fill='black', tags=(x,y))

		def drawLine(self, x0, y0, x1, y1):
			return self.c.create_line(x0, y0, x1, y1)

		def createSpecifier(self, shape):
			return

		def getCoords(self, node):
			x = int((self.c.coords(node)[2] + self.c.coords(node)[0])/2)
			y = int((self.c.coords(node)[3] + self.c.coords(node)[1])/2)
			return x, y

		def itemClicked(self, event):
			return

		def canvasClick(self, event):
			mouse_x, mouse_y = event.x, event.y

			if self.g.numVertices == 0: #place first node
				circle = self.drawCircle(mouse_x, mouse_y)
				new_node = (circle,)
				self.g.addVert(new_node)
			else: #place subsequent nodes
				if not self.selected_node: #first, select node to branch from
					found_node = self.c.find_closest(mouse_x, mouse_y)
					found_x, found_y = self.getCoords(found_node)
					dist = sqrt((found_x-mouse_x)**2 + (found_y-mouse_y)**2)
					if dist <= node_r:
						self.c.itemconfig(found_node, fill='grey')
						self.selected_node = found_node
				else: #then create a neighbor node
					circle = self.drawCircle(mouse_x, mouse_y)
					new_node = (circle,)
					self.g.addVert(new_node)
					self.c.itemconfig(self.selected_node, fill='black')
					new_x, new_y = self.getCoords(new_node)
					old_x, old_y = self.getCoords(self.selected_node)
					line = self.drawLine(new_x, new_y, old_x, old_y)
					new_edge = (line,)
					self.g.addEdge(self.g.getVert(self.selected_node), self.g.getVert(new_node), new_edge)
					self.selected_node = None

		def draw(self):
			self.c.after(50, self.draw)




	app = App(canvas)
	app.draw()
	root.mainloop()

if __name__== "__main__":
	main()
