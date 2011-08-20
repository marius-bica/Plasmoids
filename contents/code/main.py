# -*- coding: utf-8 -*-
import subprocess
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyQt4 import QtCore

class Vnstat(plasmascript.Applet):
	def __init__(self,parent,args=None):
		plasmascript.Applet.__init__(self,parent)

	def init(self):
		self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
		self.label = Plasma.Label(self.applet)
		self.label.setText("Init")
		self.layout.addItem(self.label)
		self.applet.setLayout(self.layout)
		self.resize(90, 20)
		
		self.timer = QtCore.QTimer()
		self.timer.setInterval(900000)
		self.timer.start()
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updateLabel)
		
		self.updateLabel()

	def updateLabel(self):
		color = 'white'
		p = subprocess.Popen("vnstat --oneline", shell=True, stdout=subprocess.PIPE)
		stats = p.communicate()
		frags = stats[0].split(';')
		
		style = 'color:#000;font-family:Ubuntu;font-size:10px;font-weight:bold'
		self.label.setText('<span style="' + style + '">' + frags[3] + "</span>")
		

def CreateApplet(parent):
	return Vnstat(parent)