# -*- coding: utf-8 -*-
import subprocess
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyQt4 import QtCore

class RamUsage(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

    def init(self):
        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
        self.label = Plasma.Label(self.applet)
        self.label.setText("Init")
        self.layout.addItem(self.label)
        self.applet.setLayout(self.layout)
        self.resize(160, 20)
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(5000)
        self.timer.start()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updateLabel)
        
        self.updateLabel()

    def updateLabel(self):
        color = 'white'
        p = subprocess.Popen("vmstat | tail -n1 | awk '{print $3,$4,$5,$6}'", shell=True, stdout=subprocess.PIPE)
        stats = p.communicate()
        frags = stats[0].split(' ')
        free = int(math.floor(int(frags[1])/1024))
        swap = int(math.floor(int(frags[0])/1024))
        buffers = int(math.floor(int(frags[2])/1024))
        cache = int(math.floor(int(frags[3])/1024))
        total = free + cache + buffers
        
        style = 'color:#fff;font-family:Ubuntu;font-size:10px;font-weight:normal;width:140px;'
        totalStyle = ''
        if total <= 500:
            totalStyle = ' style="color:#fff;font-weight:bold;background-color:#ff0000;"'
        labelStyle = ' style="font-weight:bold;color:#4F555A;"'        
    
        text  = '<div style="' + style + '">'
        text += '<table>'
        text += '<tr><td width="5%"><span' + labelStyle + '>F</span></td><td align="right">' + str(free) + ' MB</td><td width="5%"><span' + labelStyle + '>C</span></td><td align="right">' + str(cache) + ' MB</td></tr>'
        text += '<tr><td width="5%"><span' + labelStyle + '>B</span></td><td align="right">' + str(buffers) + ' MB</td><td width="5%"><span' + labelStyle + '>S</span></td><td align="right">' + str(swap) + ' MB</td></tr>'
        text += '<tr><td width="10%"><span' + labelStyle + '>F+C</span></td><td align="right">' + str(free + cache) + ' MB</td><td width="5%"><span' + labelStyle + '>T</span></td><td align="right"><span' + totalStyle + '>' + str(total) + ' MB</span></td></tr>'
        text += '</table>'
        text += '</div>'
        self.label.setText(text)
                

def CreateApplet(parent):
        return RamUsage(parent)