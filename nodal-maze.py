import time
import tkinter as tk
from random import randint

def main():
	# class node():
	# 	def __init__(self, key):
	#         self.id = key
	#         self.connectedTo = {}

	#     def addNeighbor(self, nbr, weight=0):
	#         self.connectedTo[nbr] = weight

	#     def __str__(self):
	#         return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

	#     def getConnections(self):
	#         return self.connectedTo.keys()

	#     def getId(self):
	#         return self.id

	#     def getWeight(self,nbr):
	#         return self.connectedTo[nbr]

	def drawCircle(x, y):
		r = int(width / 300)
		x0 = x - r
		y0 = y - r
		x1 = x + r
		y1 = y + r
		c.create_oval(x0, y0, x1, y1, fill='black')

	def drawLine(x0, y0, x1, y1):
		c.create_line(x0, y0, x1, y1)

	master = tk.Tk()
	master.attributes('-fullscreen', True)
	width, height = master.winfo_screenwidth(), master.winfo_screenheight()

	c = tk.Canvas(master, width=width, height=height)
	c.pack()


	x, y = 0, 0
	for node in range(100):
		xo, yo = x, y

		r = int(width / 100)
		x = randint(r, width-r)
		y = randint(r, height-r)
		drawCircle(x, y)

		if node != 0:
			drawLine(x, y, xo, yo)

		master.update()
		time.sleep(.25)

	master.mainloop()

if __name__== "__main__":
	main()
