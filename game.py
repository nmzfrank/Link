import random
import pygame
from pygame.locals import *
from sys import exit

pic_name = ['1.jpg','2.jpg','3.jpg','4.jpg','5.jpg','6.jpg','7.jpg','8.jpg','9.jpg','10.jpg','11.jpg','12.jpg','13.jpg','14.jpg','15.jpg','16.jpg','17.jpg','18.jpg',]
bios_x = 100
bios_y = 70

class Pic(object):
	"""docstring for Point"""
	def __init__(self, pos_x, pos_y, filename= None):
		super(Pic, self).__init__()
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.filename = filename
		self.blocked = 0
		self.display = False


class UI(object):
	"""docstring for UI"""
	def __init__(self):
		super(UI, self).__init__()
		pygame.init()
		self.screen = pygame.display.set_mode((800,640),0,32)
		self.map = []
		self.keyPress = 0
		self.pressed = []
		self.count = 80
		for i in range(12):
			self.map.append([])
			self.map[i] = range(10)
		self.newGame()

	def newGame(self):
		map = []
		for i in range(12):
			for j in range(10):
				map.append(Pic(i,j))
		random.shuffle(map)
		count = 0
		index = 0
		for item in map:
			if (item.pos_x == 0 or item.pos_x == 11 or item.pos_y == 0 or item.pos_y == 9):
				item.filename = 'blank.jpg'
			else:
				item.filename = pic_name[index]
				item.blocked = 1
				item.display = True
				count += 1
				if count == 8:
					index += 1
					count = 0
			self.map[item.pos_x][item.pos_y] = item
		self.display()

	def display(self):
		for i in range(12):
			for j in range(10):
				item = self.map[i][j]
				picture = pygame.image.load(item.filename).convert()
				px = item.pos_x * 50 + bios_x
				py = item.pos_y * 50 + bios_y
				self.screen.blit(picture,(px,py))


	def mainloop(self):
		while(True):
			for event in pygame.event.get():
				if event.type == QUIT:
					exit()
				if event.type == MOUSEBUTTONDOWN:
					self.mouseDown(event)
			pygame.display.update()

	def mouseDown(self,event):
		mx = event.pos[0]
		my = event.pos[1]
		pos_x,pos_y = self.normalize(mx,my)
		if (pos_x > 0 and pos_x < 11 and pos_y > 0 and pos_y < 9):
			if (self.keyPress == 0):
				self.keyPress = 1
				self.pressed = [pos_x,pos_y]
			else:
				self.keyPress = 0
				if(self.test(pos_x,pos_y)):
					self.clear(pos_x,pos_y)
		return 

	def clear(self, px, py):
		self.map[px][py].blocked = 0
		self.map[px][py].filename = 'blank.jpg'
		self.map[self.pressed[0]][self.pressed[1]].blocked = 0
		self.map[self.pressed[0]][self.pressed[1]].filename = 'blank.jpg'
		self.count -= 2
		self.display()
		print px,py
		if self.count == 0:
			self.win()

	def checkBlocked(self,x1,y1,x2,y2):
		print "checking (",x1 ,",",y1,")(",x2,",",y2,")"
		if(x1 == x2):
			if(y1 > y2):
				y1,y2 = y2,y1
			for i in range(y1,y2+1,1):
				if self.map[x1][i].blocked == 1:
					return False
		elif(y1 == y2):
			if(x1 > x2):
				x1,x2 = x2,x1
			for i in range(x1,x2+1,1):
				if self.map[i][y1].blocked == 1:
					return False
		else:
			return False
		return True

	def test(self,px,py):
		sx = self.pressed[0]
		sy = self.pressed[1]
		self.map[px][py].blocked = 0
		self.map[sx][sy].blocked = 0
		if(sx == px):
			candidate = self.getValid(sx,sy,1)
			for i in candidate:
				if(self.checkBlocked(i,sy,i,py) and self.checkBlocked(i,py,px,py)):
					return True
		elif(sy == py):
			candidate = self.getValid(sx,sy,2)
			for i in candidate:
				if(self.checkBlocked(sx,i,px,i) and self.checkBlocked(px,i,px,py)):
					return True
		else:
			candidate = self.getValid(sx,sy,1)
			for i in candidate:
				if(self.checkBlocked(i,sy,i,py) and self.checkBlocked(i,py,px,py)):
					return True
			candidate = self.getValid(sx,sy,2)
			for i in candidate:
				if(self.checkBlocked(sx,i,px,i) and self.checkBlocked(px,i,px,py)):
					return True
		self.map[px][py].blocked = 1
		self.map[sx][sy].blocked = 1
		return False


	def getValid(self,px,py,type):
		if type == 1:
			result = [px]
			for i in range(px+1,12,1):
				if (self.map[i][py].blocked == 0):
					result.append(i)
				else:
					break
			for i in range(px-1,-1,-1):
				if (self.map[i][py].blocked == 0):
					result.append(i)
				else:
					break
		if type == 2:
			result = [py]
			for i in range(py+1,10,1):
				if (self.map[px][i].blocked == 0):
					result.append(i)
				else:
					break
			for i in range(py-1,-1,-1):
				if (self.map[py][i].blocked == 0):
					result.append(i)
				else:
					break
		print result
		return result

	def normalize(self,mx,my):
		x = (mx - bios_x) / 50
		y = (my - bios_y) / 50
		return x,y

	def win(self):
		return

if __name__ == '__main__':
	ui = UI()
	ui.mainloop()