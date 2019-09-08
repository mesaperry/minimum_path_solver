'''
graph implementation modified from the original here:
https://runestone.academy/runestone/books/published/pythonds/Graphs/Implementation.html



TODO:


'''

import tkinter as tk
from math import sqrt

node_r = 20 #size of node circles

class Vertex:
	def __init__(self, data):
		self.data = data
		self.connected_to = {}
		self.parent = None

	def addConnected(self, vert, edge_data):
		self.connected_to[vert] = edge_data

	def getConnectedVert(self):
		return self.connected_to.keys()

	def getConnectedEdge(self):
		return self.connected_to.values()

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

	def addEdge(self,vd1,vd2,edge_data=None):
		v1 = self.getVert(vd1)
		v2 = self.getVert(vd2)
		v1.addConnected(v2, edge_data)
		v2.addConnected(v1, edge_data)

	def getData(self,vertex):
		if vertex in self.vertices.keys():
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
			self.c.focus_set()
			self.g = Graph()
			self.selected_node = None
			self.start_node = None
			self.end_node = None
			self.state = 'editing'
			self.s_current_vert = None
			self.s_to_parse = []
			self.s_passed = []

			self.c.bind('<Button-1>', self.canvasLeftClick)
			self.c.bind('<Button-2>', self.canvasMiddleClick)
			self.c.bind('<Button-3>', self.canvasRightClick)
			self.c.bind('<space>', self.canvasSpace)

		def drawCircle(self, x, y):
			x0 = x - node_r
			y0 = y - node_r
			x1 = x + node_r
			y1 = y + node_r
			return self.c.create_oval(x0, y0, x1, y1, fill='black', tags=(x,y))

		def drawLine(self, x0, y0, x1, y1):
			return self.c.create_line(x0, y0, x1, y1)

		def getCoords(self, node):
			x = int((self.c.coords(node)[2] + self.c.coords(node)[0])/2)
			y = int((self.c.coords(node)[3] + self.c.coords(node)[1])/2)
			return x, y

		def circleClicked(self, x, y):
			for circle in self.g.vertices.values():
				found_x, found_y = self.getCoords(circle)
				dist = sqrt((found_x-x)**2 + (found_y-y)**2)
				if dist <= node_r: #check if click is within circle bounds
					return circle
			else:
				return None

		def applyOGColor(self, node):
			if node == self.start_node:
				self.c.itemconfig(node, fill='green')
			elif node == self.end_node:
				self.c.itemconfig(node, fill='red')
			else:
				self.c.itemconfig(node, fill='black')

		def displayMessage(self, message):
			size = 30
			x = int(width / 2)
			y = int(height - size)
			return self.c.create_text(x, y,
							   font="Times "+str(size)+" bold",
							   text=message)


		def canvasLeftClick(self, event):
			mouse_x, mouse_y = event.x, event.y

			if self.state == 'editing':
				clicked_node = self.circleClicked(mouse_x, mouse_y)

				if clicked_node: #if a node was selected
					if not self.selected_node: #if no node already selected
						self.c.itemconfig(clicked_node, fill='grey')
						self.selected_node = clicked_node #select this node
					else: #selecting second node to connect
						v1 = self.g.getVert(clicked_node) #check if nodes already connected
						v2 = self.g.getVert(self.selected_node)
						if v2 in v1.getConnectedVert():
							return

						self.applyOGColor(self.selected_node)
						x0, y0 = self.getCoords(self.selected_node)
						x1, y1 = self.getCoords(clicked_node)
						line = self.drawLine(x0, y0, x1, y1)
						self.g.addEdge(self.selected_node, clicked_node, line)
						self.selected_node = None

				else: #if clicked on empty space
					for circle in self.g.vertices.values():
						found_x, found_y = self.getCoords(circle)
						dist = sqrt((found_x-mouse_x)**2 + (found_y-mouse_y)**2)
						if dist <= node_r*3: #don't create if too close to existing node
							return

					if self.selected_node: #if a node is already selected, create a new node and connect it
						self.applyOGColor(self.selected_node)
						circle = self.drawCircle(mouse_x, mouse_y)
						self.g.addVert(circle)
						old_x, old_y = self.getCoords(self.selected_node)
						line = self.drawLine(mouse_x, mouse_y, old_x, old_y)
						self.g.addEdge(self.selected_node, circle, line)
						self.selected_node = None
					else: #create a new node
						circle = self.drawCircle(mouse_x, mouse_y)
						self.g.addVert(circle)


		def canvasMiddleClick(self, event):
			mouse_x, mouse_y = event.x, event.y
			
			if self.state == 'editing':
				clicked_node = self.circleClicked(mouse_x, mouse_y)

				if self.selected_node: #deselect current node
					self.c.itemconfig(self.selected_node, fill='black')
					self.selected_node = None
					if not clicked_node:
						return
				if self.start_node: #remove previous start node
					self.c.itemconfig(self.start_node, fill='black')
					self.start_node = None

				if clicked_node:
					if clicked_node == self.end_node: #overwrite end node
						self.end_node = None

					self.c.itemconfig(clicked_node, fill='green')
					self.start_node = clicked_node


		def canvasRightClick(self, event):
			mouse_x, mouse_y = event.x, event.y
			
			if self.state == 'editing':
				clicked_node = self.circleClicked(mouse_x, mouse_y)

				if self.selected_node: #deselect current node
					self.c.itemconfig(self.selected_node, fill='black')
					self.selected_node = None
					if not clicked_node:
						return
				if self.end_node: #remove previous end node
					self.c.itemconfig(self.end_node, fill='black')
					self.end_node = None

				if clicked_node:
					if clicked_node == self.start_node: #overwrite start node
						self.start_node = None

					self.c.itemconfig(clicked_node, fill='red')
					self.end_node = clicked_node

		def canvasSpace(self, event):
			if self.start_node and self.end_node and self.state=='editing':
				self.state = 'solving'

				self.s_to_parse.append(self.g.getVert(self.start_node))
				self.c.after(0, self.solve)


		def solve(self): #recursively call
			vert = self.s_to_parse.pop(0)
			if vert==self.g.getVert(self.end_node):
				vert = vert.parent
				path_count = 0
				while not vert==self.g.getVert(self.start_node):
					self.c.itemconfig(self.g.getData(vert), fill='blue')
					vert = vert.parent
					path_count += 1
				self.displayMessage('Found minimum path with '+str(path_count+2)+' nodes')
				return

			if not (vert==self.g.getVert(self.start_node) or vert==self.g.getVert(self.end_node)): #keep start and end nodes
				self.c.itemconfig(self.g.getData(vert), fill='light blue')
			self.s_passed.append(vert)

			for neighbor in vert.getConnectedVert():
				if neighbor not in self.s_passed:
					self.s_to_parse.append(neighbor)
					neighbor.parent = vert


			if self.s_to_parse: #continue recursion if remaining connected nodes
				self.c.after(200, self.solve)
			else: #no remaining connected nodes and end node was not found
				self.displayMessage('Start node and end node not connected')
				return



		def draw(self):
			self.c.after(50, self.draw)





	app = App(canvas)
	app.draw()
	root.mainloop()

if __name__== "__main__":
	main()
