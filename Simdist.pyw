# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 16:59:44 2015

@author: pedro.correia
"""

from __future__ import division          # This is python 2.7 so I always use this to avoid problems in divisions
import numpy as np                       # Numpy numerical library
from scipy.interpolate import interp1d   # Scipy interpolation function (the purpose of this desktop App)

import sys                               # System library
from PyQt4 import QtGui,QtCore,Qt        # PyQt4/PySide (depending on implementation) is the GUI library
import libs.cerena_file_utils as cfile   # This is a CERENA made library to deal with files.

import os                                # I need to do some file management, that's why I'm importing os library
from os import listdir                   # Actually I'm just going to use the names directly instead from os
from os.path import isfile, join         # Same here

#import pyqtgraph.examples
#pyqtgraph.examples.run()                # I was just seeing how pyqtgraph works with this (that's why it's commented for the release)
import pyqtgraph as pg                   # This is the library I'm going to use for plots

def load_style(spath='Stylesheet/stylesheet.xml'):
    """
    Loading function for stylesheet of the software.
    The function loads the entire file into a single string.
    The stylesheet determines the color of all widgets in the
    software. It's xml (maybe css) code. QT knows how to handle
    it.
    """
    fid = open(spath)       # Open file into a variable (just the file, not the information within it).
    l = fid.readlines()     # Reads all information inside the file to a list of strings.
    fid.close()             # Closes the file
    s = ''                  # Creates an empty string variable.
    for i in l: s=s+i       # Tranforms the list of strings into the above string variable (so all text is now a string).
    return s                # Returns a string with all the file information.

class Simdist(QtGui.QMainWindow):
    """
    The software name is Simdist. I've created an identifying icon
    for it (CERENA) and I'm thinking it should have a 2D viewer and a toolbar
    for quick operations and parameters
    """
    def __init__(self):
        super(Simdist, self).__init__()
        
        self.initUI()   # The first function I call is the one that's going to build all necessary widgets.
        
    def initUI(self):
        """
        This function sets the necessary variables and widgets for the software to function.
        """
        self.data_flag = False   # Flag for user imported data
        self.data = None         # Variable for user imported data
        self.internal = None     # Variable for software imported data
        self.new_data = None     # Variable for interpolated data
        
        self.internal_plot = None       # Variable for software imported data plot
        self.internal_plot_flag = False # Flag for software imported data plot
        self.data_plot = None       # Variable for user imported data plot
        self.inter_plot = None      # Variable for interpolated data
        self.data_plot_flag = False # Flag for user imported data plot
        
        self.topmenu()  # This function will build a topmenu into this application (see topmenu function).
        self.toolbar()  # This function will build a toolbar into this application (see toolbar function).
        self.viewer()   # This function will build a 2D viewer embed in the software (see viewer function).
        
    def __update_distribution_database__(self):
        """
        Function to check which data is available to be used for transformation.
        It adds the name of the files into a combobox on the interface of this app.
        """
        onlyfiles = [ f for f in listdir('Base') if isfile(join('Base',f)) ]  # Quick recipe I got for getting all files (names) within a folder (thanks pycruft: http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python)
        for i in onlyfiles:              # So for every file name I'm going to add an item to the combobox in toolbar.
            self.baseInput.addItem(i)    # I think I could used addItems but I'm on the run (no time to test).

    def __get_compare_distribution__(self):
        """
        This function loads the requested internal data and plots it.
        """
        self.internal = np.loadtxt('Base/'+str(self.baseInput.currentText()))  # Open requested distribution file.
        if not self.internal_plot_flag:   # If it does not have any internal data plot:
            self.internal_plot = self.my_viewer.plot(self.internal[:,0],self.internal[:,1],pen='r')    # Plot requested data.        
            self.internal_plot_flag = True  # And changes the internal data plot flag to True
        else:    # If a internal data plot already exists than...
            self.my_viewer.removeItem(self.internal_plot)  # Removes the previous
            self.internal_plot = self.my_viewer.plot(self.internal[:,0],self.internal[:,1],pen='r')    # And Plots new requested data.
            
    def __get_user_distribution__(self):
        """
        This function uses user imported data with column chosen in the toolbar SpinBox
        to plot the file information and the ready made interpolation for the new function.
        """
        if self.data_flag: # This will only work if user has imported data
            if not self.data_plot_flag:      # If no previous user data exists
                per_data = np.percentile(self.data[:,self.colInput.value()-1],range(0,101))  # calculates new set
                
                f1  = interp1d(per_data,np.arange(0,101))  # Interpolation function from original set to percentile values.
                f2  = interp1d(self.internal[:,0],self.internal[:,1])   # Interpolation from internal data
                new_per  = f1(self.data[:,self.colInput.value()-1])   # calculating a new percentile set
                self.new_data =  f2(new_per) # transforming those new percentile values into a completely new distribution.
                
                per_data2 = np.percentile(self.new_data,range(0,101))                              # Calculating new set from interpolation to plot
                self.data_plot = self.my_viewer.plot(np.arange(0,101),per_data,pen='b')      # and plots it with blue line
                self.inter_plot = self.my_viewer.plot(np.arange(0,101),per_data2,pen='y')    # (plots interpolated set also)
                self.data_plot_flag = True                                                   # setting its flag to true
            else:
                self.my_viewer.removeItem(self.data_plot)                                    # Otherwise remove previous user data plot
                self.my_viewer.removeItem(self.inter_plot)                                    # Otherwise remove previous user data plot
                
                per_data = np.percentile(self.data[:,self.colInput.value()-1],range(0,101))  # re-calculates new set

                f1  = interp1d(per_data,np.arange(0,101))  # Interpolation function from original set to percentile values.
                f2  = interp1d(self.internal[:,0],self.internal[:,1])   # Interpolation from internal data
                new_per  = f1(self.data[:,self.colInput.value()-1])   # calculating a new percentile set
                self.new_data =  f2(new_per) # transforming those new percentile values into a completely new distribution.                
                
                per_data2 = np.percentile(self.new_data,range(0,101))                              # Calculating new set from interpolation to plot
                self.data_plot = self.my_viewer.plot(np.arange(0,101),per_data,pen='b')      # and plots it
                self.inter_plot = self.my_viewer.plot(np.arange(0,101),per_data2,pen='y')    # (plots interpolated set also)
        
    def on_event_import(self):
        """
        Event function that open a FileDialog and if request is accepted loads
        a file into the software.
        """
        dialog = QtGui.QFileDialog(self)                               # Opens a file dialog
        dialog.setWindowTitle('Import Point-data')                     # Give a title to it
        dialog.setFileMode(QtGui.QFileDialog.ExistingFile)             # Method for the file dialog (I'm not sure of all implications but seems good)
        dialog.setStyleSheet(load_style('Stylesheet/stylesheet.xml'))  # Make sure the XML style is the same
        if dialog.exec_() == QtGui.QDialog.Accepted:                   # If selected file is accepted
            filename = dialog.selectedFiles()[0]                       # Get name of the file
            self.data = cfile.load_data(filename)                      # And opens the file using internal library
            self.colInput.setMaximum(self.data.shape[1])               # Setting the maximum for the spinbox of the column
            self.data_flag = True                                      # This is just a quick flag since other functions need to know if data has been imported.
            self.__get_user_distribution__()                           # On import imediatly calls this function
            
    def on_event_export(self):
        """
        Event function that opens a FileDialog to save results from the
        software.
        """
        if self.data_flag:  # Only lets user save anything if any data was loaded.
            dialog = QtGui.QFileDialog(self)                               # Opens a file dialog
            dialog.setWindowTitle('Import Point-data')                     # Give a title to it
            dialog.setFileMode(QtGui.QFileDialog.AnyFile)             # Method for the file dialog (I'm not sure of all implications but seems good)
            dialog.setStyleSheet(load_style('Stylesheet/stylesheet.xml'))  # Make sure the XML style is the same
            if dialog.exec_() == QtGui.QDialog.Accepted:                   # If selected file is accepted
                filename = dialog.selectedFiles()[0]                       # Get name of the file
                np.savetxt(str(filename),np.hstack((self.data,self.new_data[:,np.newaxis])),fmt='%15.3f') # Saves data for chosen directory

    def viewer(self):
        """
        This function builds a 2D viewer using pyqtgraph.
        """
        self.my_viewer = pg.PlotWidget()           # Creating my plot widget
        self.setCentralWidget(self.my_viewer)      # Embeding it in this app.
        self.__get_compare_distribution__()        # Plotting initial data
    
    def topmenu(self):
        """
        This funcion builds the top menu for this application.
        I'm putting it here to separate it from the rest of the widgets.
        """
        importAction = QtGui.QAction(QtGui.QIcon('ART/topmenu/import.png'), '&Import data', self)  # QTGUI function to create topmenu item.   
        importAction.setShortcut('Ctrl+I')                                                         # Set the shortcut
        importAction.setStatusTip('Import data')                                                   # Set the tooltip (mouse-over information)
        importAction.triggered.connect(self.on_event_import)                                       # Set the event on click
        exportAction = QtGui.QAction(QtGui.QIcon('ART/topmenu/export.png'), '&Save results', self) # QTGUI function to create topmenu item.   
        exportAction.setShortcut('Ctrl+S')                                                         # Set the shortcut
        exportAction.setStatusTip('Save results')                                                  # Set the tooltip (mouse-over information)
        importAction.triggered.connect(self.on_event_export)                                       # Set the event on click
        exitAction = QtGui.QAction(QtGui.QIcon('ART/topmenu/quit.png'), '&Exit', self)             # QTGUI function to create topmenu item.  
        exitAction.setShortcut('Ctrl+Q')                                                           # Set the shortcut
        exitAction.setStatusTip('Exit application')                                                # Set the tooltip (mouse-over information)
        exitAction.triggered.connect(self.on_event_quit)                                           # Set the event on click
        
        self.statusBar()                       # After all items are created I just call for a statusbar (bottom space where information appears).
        menubar = self.menuBar()               # I create the menu bar (the place where items are going to be put)
        fileMenu = menubar.addMenu('&File')    # In the menu bar a "File" option appears.
        fileMenu.addAction(importAction)       # Inside the "File" option I put my created items.
        fileMenu.addAction(exportAction)
        fileMenu.addAction(exitAction)
            
    def toolbar(self):
        """
        This funcion builds the toolbar menu for this application.
        I'm putting it here to separate it from the rest of the widgets.
        """
        self.input_toolbar = self.addToolBar('Data Input')         # Here I'm adding a toolbar space (with a name).
        self.input_toolbar.setIconSize(QtCore.QSize(32,32))        # I set the expected Icon (button) size.
        self.input_toolbar.setOrientation(QtCore.Qt.Horizontal)    # Set it's orientation (button orientation not toolbar).
        
        importInput = QtGui.QAction(QtGui.QIcon('ART/toolbar/import.png'), 'Import data', self)  # Create an item for the toolbar.
        importInput.setShortcut('Ctrl+P')                                                        # Set a shortcut for it.
        importInput.triggered.connect(self.on_event_import)                                      # Create an event.
        self.input_toolbar.addAction(importInput)                                                # I put the created item in the toolbar.
        
        dataInput = QtGui.QAction(QtGui.QIcon('ART/toolbar/export.png'), 'Save results', self)  # Create an item for the toolbar.
        dataInput.setShortcut('Ctrl+P')                                                         # Set a shortcut for it.
        dataInput.triggered.connect(self.on_event_export)                                       # Create an event.
        self.input_toolbar.addAction(dataInput)                                                 # I put the created item in the toolbar.
        
        self.input_toolbar.addSeparator()                  # Adding separator to avoid widgets and icons to be glued
        
        self.baseInput = baseInput = QtGui.QComboBox(self) # I'm doing a ComboBox (chose option widget) for the user to select the distribution to use for the transformation.
        self.__update_distribution_database__()            # This function will add items to the combobox
        self.input_toolbar.addWidget(self.baseInput)       # And know I put the combobox in the toolbar.
        self.baseInput.currentIndexChanged['QString'].connect(self.__get_compare_distribution__)  # Event function to plot a red line for internal database set
        
        self.input_toolbar.addSeparator()                  # Adding separator to avoid widgets and icons to be glued    
        
        self.colInput = colInput = QtGui.QSpinBox(self)    # I'm doing a SpinBox (chose number widget) to put in the toolbar (since there may be more that 1 col in input data).
        self.colInput.setRange(1,100)                      # Give a reasonable limit for the number of columns.       
        self.input_toolbar.addWidget(self.colInput)        # And put the SpinBox inside the toolbar.
        self.colInput.valueChanged.connect(self.__get_user_distribution__)  # Event function to plot a red line for user data set
        
    def launchme(self):
        """
        This funcion launches the application with some parameters.
        One of those is maximize to full size of screen. I also give
        the frame title here (Simdist).
        """
        qr = self.frameGeometry()                                 # Here I'm getting geometry of this frame (QMainWindow).
        cp = QtGui.QDesktopWidget().availableGeometry().center()  # Get the center of the screen
        qr.moveCenter(cp)                                         # Move Frame to the center of the screen.
        self.move(qr.topLeft())                                   # Make sure it's centered (I think).
        self.setWindowTitle('Simdist')                            # Set title for this frame.
        self.setFixedSize(400,400)                                # Set fixed size for this frame (so you can't change it later).
        #self.showMaximized()                                     # Maximizing the frame option (I commented since it's not important for this software).
        self.show()                                               # Make sure you're showing it (until know it's invisible).
        
    def on_event_quit(self):
        """
        Small function to ask the user if it really wants to quit
        the application.
        """
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)    # Build a Message Box dialog.
        if reply == QtGui.QMessageBox.Yes:
            QtGui.qApp.quit()                              # If reply is yes (maybe "ok"..., I'm not sure) than exit app.
    
def main():
    app = QtGui.QApplication(sys.argv)                           # Create the application.
    app.setWindowIcon(QtGui.QIcon('ART/cerena.png'))             # Here I set the logo.
    mv = Simdist()                                               # Call the application main window.
    mv.setStyleSheet(load_style('Stylesheet/stylesheet.xml'))    # Provide it a style.
    mv.launchme()                                                # call launchme() internal function that deals with some app specifics (and actually shows the app).
    sys.exit(app.exec_())                                        # I think this is the main loop. But I'm not sure.
    
if __name__ == '__main__':
    main() # If this is being executed (by oposition to be imported) than run "main" function