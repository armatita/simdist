# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 21:55:02 2015

@author: Pedro Correia
"""

from __future__ import division
import numpy as np
from PyQt4 import QtGui,QtCore
import cerena_file_utils as cfile

def load_style(spath='Stylesheet/stylesheet.xml'):
    """
    Loading function for stylesheet of the software.
    The function loads the entire file into a single string.
    The stylesheet determines the color of all widgets in the
    software. It's xml (maybe css) code. QT know how to handle
    it.
    """
    fid = open(spath)
    l = fid.readlines()
    fid.close()
    s = ''
    for i in l: s=s+i
    return s
    
class PointData(QtGui.QWidget):
    """
    Import point-data parameters frame.
    """
    def __init__(self, parent = None,filename = None):
        super(PointData, self).__init__(parent,QtCore.Qt.WindowStaysOnTopHint)
        self.filename = filename
        self.setWindowTitle('Import point-data')
        self.setStyleSheet(load_style('Stylesheet/stylesheet.xml'))
        self.setFixedSize(400, 350)
        
        self.point_parameters()
        self.null_parameters()
        self.preview_box()
        
        btn1 = QtGui.QPushButton('Import', self)
        btn1.clicked.connect(self.on_event_import)
        btn1.resize(100,40)
        btn1.move(50, 300)
        
        btn2 = QtGui.QPushButton('Cancel', self)
        btn2.clicked.connect(self.on_event_close)
        btn2.resize(100,40)
        btn2.move(250, 300)
        
    def on_event_import(self):
        pass
    
    def on_event_close(self):
        self.close()
        
    def preview_box(self):
        c=0
        s=''
        with open(self.filename) as openfileobject:
            for line in openfileobject:
                s=s+line
                c=c+1
                if c>99: break
        qle = QtGui.QPlainTextEdit(self)
        qle.move(10,150)
        qle.setFixedSize(380,140)
        qle.setPlainText(s)
        
    def null_parameters(self):
        g=QtGui.QGroupBox('Null and File',self)
        g.setFixedSize(90,140)
        g.move(305,5)
        l=QtGui.QLabel('Null:',self)
        l.move(310,50)
        l=QtGui.QLabel('Header:',self)
        l.move(310,80)
        self.null = QtGui.QDoubleSpinBox(self)
        self.null.setRange(-999999,999999)
        self.null.move(335,47)
        self.null.setFixedSize(50,20)
        self.null.setValue(-99)
        self.header = QtGui.QSpinBox(self)
        self.header.setRange(0,100)
        self.header.move(350,77)
        self.header.setFixedSize(35,20)
        
    def point_parameters(self):
        g=QtGui.QGroupBox('Point specifics',self)
        g.setFixedSize(290,140)
        g.move(10,5)
        l=QtGui.QLabel('X column:',self)
        l.move(20,50)
        l=QtGui.QLabel('Y column:',self)
        l.move(20,80)
        l=QtGui.QLabel('Z column:',self)
        l.move(20,110)
        self.node1 = QtGui.QSpinBox(self)
        self.node1.setRange(1,10000)
        self.node1.move(90,47)
        self.node1.setFixedSize(70,20)
        self.node1.setValue(1)
        self.node2 = QtGui.QSpinBox(self)
        self.node2.setRange(1,10000)
        self.node2.move(90,77)
        self.node2.setFixedSize(70,20)
        self.node2.setValue(2)
        self.node3 = QtGui.QSpinBox(self)
        self.node3.setRange(0,10000)
        self.node3.move(90,107)
        self.node3.setFixedSize(70,20)
        self.node3.setValue(3)
        
    def mesh_parameters(self):
        g=QtGui.QGroupBox('Mesh specifics',self)
        g.setFixedSize(290,140)
        g.move(10,5)
        l=QtGui.QLabel('X(i):',self)
        l.move(20,50)
        l=QtGui.QLabel('Y(j):',self)
        l.move(20,80)
        l=QtGui.QLabel('Z(k):',self)
        l.move(20,110)
        l=QtGui.QLabel('Nodes',self)
        l.move(60,20)
        l=QtGui.QLabel('Size',self)
        l.move(140,20)
        l=QtGui.QLabel('First',self)
        l.move(220,20)
        self.node1 = QtGui.QSpinBox(self)
        self.node1.setRange(1,10000)
        self.node1.move(60,47)
        self.node1.setFixedSize(70,20)
        self.node2 = QtGui.QSpinBox(self)
        self.node2.setRange(1,10000)
        self.node2.move(60,77)
        self.node2.setFixedSize(70,20)
        self.node3 = QtGui.QSpinBox(self)
        self.node3.setRange(1,10000)
        self.node3.move(60,107)
        self.node3.setFixedSize(70,20)
        
        self.size1 = QtGui.QDoubleSpinBox(self)
        self.size1.setRange(1,1000000)
        self.size1.move(140,47)
        self.size1.setFixedSize(70,20)
        self.size2 = QtGui.QDoubleSpinBox(self)
        self.size2.setRange(1,1000000)
        self.size2.move(140,77)
        self.size2.setFixedSize(70,20)
        self.size3 = QtGui.QDoubleSpinBox(self)
        self.size3.setRange(1,1000000)
        self.size3.move(140,107)
        self.size3.setFixedSize(70,20)
        
        self.first1 = QtGui.QDoubleSpinBox(self)
        self.first1.setRange(0,1000000)
        self.first1.move(220,47)
        self.first1.setFixedSize(70,20)
        self.first2 = QtGui.QDoubleSpinBox(self)
        self.first2.setRange(0,1000000)
        self.first2.move(220,77)
        self.first2.setFixedSize(70,20)
        self.first3 = QtGui.QDoubleSpinBox(self)
        self.first3.setRange(0,1000000)
        self.first3.move(220,107)
        self.first3.setFixedSize(70,20)
        

