# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 15:59:14 2018

@author: Ilias
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import frame3d as model
import numpy as np
import pandas as pd
import analysis3Dframe as analyze
import os
thereisopenproject = False
ADDSELFLOADS = True
MAINWINDOW = None

back = 'rgb(218, 218, 218)'
tabs = 'rgb(240, 240, 240)'
lighttabs = tabs
letters = 'rgb(25,10,10)'
menubarselection = 'rgb(255,0,0)'
gradstart = 'rgb(149, 151, 163)'
gradient = 'stop:0 rgb(194, 204, 204), stop:1 rgb(164, 174, 174)'
detaildark =  'rgb(67,76,88)'
detaillight = tabs

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        width_unit = QtWidgets.QDesktopWidget().availableGeometry().size().width()//100 #13px
        height_unit = QtWidgets.QDesktopWidget().availableGeometry().size().height()//100 #7px
        self.projectname = None
        onlyFloat = QFloatValidator()
        onlyPosFloat = QPosFloatValidator()
#------>fonts
        font1 = QtGui.QFont()
        font1.setFamily("Arial")
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setUnderline(True)
        font1.setWeight(75)
        font2 = QtGui.QFont()
        font2.setFamily("Arial")
        font2.setPointSize(9)
        font2.setUnderline(True)
        font2.setWeight(50)
        font3 = QtGui.QFont()
        font3.setFamily("Arial")
        font3.setPointSize(9)
        font3.setWeight(50)
        font4 = QtGui.QFont()
        font4.setFamily("Arial")
        
#------>stylesheets
        mainwindowstyle = "background-color: "+back+";border-color: "+back+";"
#        tabstyle = "QTabBar::tab:selected {color:rgb(234, 238, 0);background-color: "+detaillight+";}QTabWidget::pane {border: 0px;}QTabBar::tab {background-color: "+back+";}QTabWidget>QWidget>QWidget{background-color: qlineargradient(spread:pad, x1:0.222, y1:1, x2:0.812, y2:0, "+ gradient +");}color: "+letters+";"
        tabstyle = "QTabBar::tab:selected {background-color: "+detaillight+";} QTabWidget::pane {border: 0px;} QTabBar::tab {background-color: "+back+";} QTabWidget>QWidget>QWidget{background-color: "+tabs+";} color: "+letters+";"
        menubarstyle = """
        QMenuBar {background-color: rgb(134, 144, 144);
           color: rgb(244, 251, 251);}
        QMenuBar::item {background-color: rgb(134, 144, 144);
            color: rgb(244, 251, 251);}
        QMenuBar::item::selected {background-color: rgb(67,76,88);}
        QMenu {background-color: rgb(134, 144, 144);
            color: rgb(244, 251, 251);}
        QMenu::item::selected {background-color: rgb(67,76,88);}"""
        toolbarstyle = "background-color: "+tabs+";border-color: rgb(107, 116, 128);"
        framestyle = "background-color: "+tabs+";"
        graphicstyle = "background-color: qlineargradient(spread:pad, x1:0.222, y1:1, x2:0.812, y2:0, "+ gradient +");"
        statusbarstyle = "background-color: rgb(107, 116, 128);border: 1px solid rgb(107, 116, 128);\n"
        treestyle = "color: "+letters+";"
        combostyle = "background-color: rgb(254, 254, 254);"
        lineeditstyle = "background-color: rgb(254, 254, 254);"
        leftliststyle = "background-color: "+tabs+";border-color: rgb(204, 204, 204);"
#------>genikes diastaseis
        min_tree_width = width_unit*14.5
        min_graph_width = width_unit*50
        min_tabs_width = width_unit*30
        iconsize = int(width_unit*1.6)
        tabtreeSize = width_unit*8
#------>xarakthristika main window        
        self.setWindowIcon(QtGui.QIcon("Pyrforos.ico"))
        if self.projectname:
            self.setWindowTitle(self.projectname)
        else:
            self.setWindowTitle(" ")
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setStyleSheet(mainwindowstyle)
#------>menubar        
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setStyleSheet(menubarstyle)
        self.menubar.setGeometry(QtCore.QRect(0, 0, width_unit*100, height_unit*3))
        self.menuFile = QtWidgets.QMenu("File",self.menubar)
#        self.menuEdit = QtWidgets.QMenu("Edit",self.menubar)
#        self.menuHelp = QtWidgets.QMenu("Help",self.menubar)
        self.setMenuBar(self.menubar) 
        self.actionNew = QtWidgets.QAction("New File",self)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addSeparator()
        self.actionOpen = QtWidgets.QAction("Open",self)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.actionSave = QtWidgets.QAction("Save",self)
        self.menuFile.addAction(self.actionSave)
        self.actionSaveAs = QtWidgets.QAction("Save as...",self)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.actionExit = QtWidgets.QAction("Exit",self)
        self.menuFile.addAction(self.actionExit)
#        self.actionPreferences = QtWidgets.QMenu("Preferences",self.menuEdit)
#        self.actionIncludeSelfLoads = QtWidgets.QAction("Include self loads",self)
#        self.actionDontIncludeSelfLoads = QtWidgets.QAction("Exclude self loads",self)
#        self.actionPreferences.addAction(self.actionIncludeSelfLoads)
#        self.actionPreferences.addAction(self.actionDontIncludeSelfLoads)
#        self.menuEdit.addAction(self.actionPreferences.menuAction())
#        self.actionPreferences = QtWidgets.QAction("Preferences",self)
#        self.menuEdit.addAction(self.actionPreferences)
        self.menubar.addAction(self.menuFile.menuAction())
#        self.menubar.addAction(self.menuEdit.menuAction())        
#        self.menubar.addAction(self.menuHelp.menuAction())
#------>toolbar 1
        tb = self.addToolBar("")
        tb.setMovable(False)
        tb.setStyleSheet(toolbarstyle)
        tb.setIconSize(QtCore.QSize(iconsize,iconsize))#20*20
        new_file = QtWidgets.QAction(QtGui.QIcon("icons\\new.png"),"New File",self)
        tb.addAction(new_file)
        open_file = QtWidgets.QAction(QtGui.QIcon("icons\\openfolder.png"),"Open File",self)
        tb.addAction(open_file)
        tb.addSeparator()
        self.save_file = QtWidgets.QAction(QtGui.QIcon("icons\\save.png"),"Save",self)
#        save_file.setShortcut("Ctrl+S")
        tb.addAction(self.save_file)
        tb.addSeparator()
#        print_file = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\Ilias\\icons\\print.png"),"Print",self)
#        tb.addAction(print_file)
#        undo = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\Ilias\\icons\\undo.png"),"Undo Action",self)
#        tb.addAction(undo)
#        redo = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\Ilias\\icons\\redo.png"),"Redo Action",self)
#        tb.addAction(redo)
        self.analysis = QtWidgets.QAction("ANALYSIS",self)
        self.viewresults = QtWidgets.QAction("VIEW RESULTS",self)
        tb.addAction(self.analysis)
        tb.addAction(self.viewresults)
        
#------>toolbar 2 
#        tb2 = self.addToolBar("")
#        tb2.setMovable(False)
#        tb2.setStyleSheet(toolbarstyle)
#        tb2.setIconSize(QtCore.QSize(iconsize,iconsize))
#        win = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\Ilias\\icons\\win.png"),"Cacscade",self)
#        tb2.addAction(win)
#        win1 = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\Ilias\\icons\\win1.png"),"Column",self)
#        tb2.addAction(win1)
#        win2 = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\Ilias\\icons\\win2.png"),"Stack",self)
#        tb2.addAction(win2)
#        win3 = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\Ilias\\pyproj\\icons\\win3.png"),"Tile",self)
#        tb2.addAction(win3)
        
#------>toolbar 3 
#        tb3 = self.addToolBar("")
#        tb3.setMovable(False)
#        tb3.setStyleSheet(toolbarstyle)
#        tb3.setIconSize(QtCore.QSize(iconsize,iconsize))
#        win = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\Ilias\\pyproj\\icons\\sections1.png"),"Cacscade",self)
#        tb3.addAction(win)
#        win1 = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\Ilias\\pyproj\\icons\\member1.png"),"Column",self)
#        tb3.addAction(win1)
#        win2 = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\Ilias\\pyproj\\icons\\support4.png"),"Stack",self)
#        tb3.addAction(win2)
#        win3 = QtWidgets.QAction(QtGui.QIcon("C:\\Users\\Ilias\\pyproj\\icons\\support5.png"),"Tile",self)
#        tb3.addAction(win3)
#------>set central widget
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
#------>gridlayout
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        m = int(width_unit/3+1)
        self.gridLayout.setHorizontalSpacing(m)
        self.gridLayout.setVerticalSpacing(m)
        self.gridLayout.setContentsMargins(m,m,m,m)
#------>frameAndTree        
        self.frameleft = QtWidgets.QFrame(self.centralwidget)
        self.frameleft.setMinimumSize(QtCore.QSize(min_tree_width, 0))
        self.frameleft.setStyleSheet(framestyle)
        self.mainTree = QtWidgets.QTreeWidget(self.frameleft)
        self.mainTree.setMinimumSize(QtCore.QSize(min_tree_width, 0))
        self.mainTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.mainTree.setStyleSheet(treestyle)
        self.mainTree.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mainTree.header().setVisible(False)
#        self.mainTree.horizontalScrollBar().setEnabled(True);
#        self.mainTree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
#        self.mainTree.header().setStretchLastSection(True)
        self.mainTree.setColumnWidth(0, 500)
        self.mainTree.raise_()
        
        
#------>list info box
        self.listWidget = QtWidgets.QListWidget(self.frameleft)
        self.listWidget.setStyleSheet(leftliststyle)
        self.listWidget.setFrameShape(QtWidgets.QFrame.Panel)
        self.listWidget.setLineWidth(1)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
#------>layouts
        self.verticalLeft = QtWidgets.QVBoxLayout(self.frameleft)
        self.verticalLeft.setContentsMargins(3, 3, 3, 3)
        self.verticalLeft.addWidget(self.mainTree)
        self.verticalLeft.addWidget(self.listWidget)
        self.verticalLeft.setStretch(0, 65)
        self.verticalLeft.setStretch(1, 35)
        self.gridLayout.addWidget(self.frameleft, 0, 0, 3, 1)
#------>graphicsView
#        self.viewer = QtWidgets.QGraphicsView(self.centralwidget)
        self.viewer = StructureViewer(self.centralwidget)
        
        self.viewer.setMinimumSize(QtCore.QSize(min_graph_width, 0))
        self.viewer.setStyleSheet(graphicstyle)
        self.viewer.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.viewer.setLineWidth(0)
        self.gridLayout.addWidget(self.viewer, 0, 1, 2, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 19, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 0, 1)
        self.viewerframe = QtWidgets.QFrame(self.centralwidget)
        self.viewerframe.setMaximumHeight(100)
        self.gridLayout.addWidget(self.viewerframe, 2, 1, 1, 1)
        self.btndefault = QtWidgets.QPushButton('Default view',self.viewerframe)
        self.btnxyview = QtWidgets.QPushButton('XY view',self.viewerframe)
        self.btnxzview = QtWidgets.QPushButton('XZ view',self.viewerframe)
        self.btnyzview = QtWidgets.QPushButton('YZ view',self.viewerframe)
        gridviewerframe = QtWidgets.QGridLayout(self.viewerframe)
        gridviewerframe.addWidget(self.btndefault, 0, 0, 1, 1)
        gridviewerframe.addWidget(self.btnxyview, 0, 1, 1, 1)
        gridviewerframe.addWidget(self.btnxzview, 0, 2, 1, 1)
        gridviewerframe.addWidget(self.btnyzview, 0, 3, 1, 1)
        for i in range(3):
            gridviewerframe.setRowStretch(i,1)
        
#------>tabs
        self.frameright = QtWidgets.QFrame(self.centralwidget)
        self.frameright.setMinimumSize(QtCore.QSize(min_tabs_width, 0))
        self.frameright.setStyleSheet(framestyle)
        self.frameright.setLineWidth(0)
        self.verticalRight = QtWidgets.QVBoxLayout(self.frameright)
        self.verticalRight.setContentsMargins(0, 0, 0, 0)
        self.verticalRight.setSpacing(0)
#------>top tabs
        self.tab_top = QtWidgets.QTabWidget(self.frameright)
        self.tab_top.setStyleSheet(tabstyle)
#------START OF SECTIONS-------------------------------------------------------

        self.tabSections = QtWidgets.QWidget()
        self.tab_top.addTab(self.tabSections, "Sections")
        self.label_Groups = QtWidgets.QLabel("Groups",self.tabSections)
        self.grouptree = QtWidgets.QTreeWidget(self.tabSections)
        self.grouptree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.grouptree.setHeaderHidden(True)
        self.grouptree.setMinimumSize(QtCore.QSize(tabtreeSize, 0))
        self.grouptree.setMaximumSize(QtCore.QSize(tabtreeSize, 100000))
#        self.grouptree.header().setStretchLastSection(False)
#        self.grouptree.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.grouptree.setStyleSheet(treestyle)
        self.grouptree.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_Sections = QtWidgets.QLabel("Sections",self.tabSections)
        self.frame1 = QtWidgets.QFrame(self.tabSections)
        self.frame3 = QtWidgets.QFrame(self.tabSections)
        self.frame4 = QtWidgets.QFrame(self.tabSections)
        self.gridSections = QtWidgets.QGridLayout(self.tabSections)
        self.gridSections.addWidget(self.label_Groups, 0, 0, 1, 1)
        self.gridSections.addWidget(self.grouptree, 1, 0, 3, 1)
        self.gridSections.addWidget(self.label_Sections, 0, 1, 1, 1)
        self.gridSections.addWidget(self.frame1, 1, 1, 1, 1)
        self.gridSections.addWidget(self.frame3, 2, 1, 1, 1)
        self.gridSections.addWidget(self.frame4, 3, 1, 1, 1)
#------>way of section inserting
        self.sectionType=QtWidgets.QButtonGroup()
        self.sectionType.setExclusive(True)
        self.firstSection=QtWidgets.QRadioButton("Standard Structural Steel",self.frame1)
        self.firstSection.setChecked(True)
        self.secondSection=QtWidgets.QRadioButton("Cross - section Values",self.frame3)
        for sectionway in [self.firstSection, self.secondSection]:
            self.sectionType.addButton(sectionway)
#------>type of standard section
        self.sectionSize=QtWidgets.QButtonGroup()
        self.sectionSize.setExclusive(True)
        self.rbIPE = QtWidgets.QRadioButton("IPE",self.frame1)
        self.rbHE = QtWidgets.QRadioButton("HE",self.frame1)
        self.rbIPN = QtWidgets.QRadioButton("IPN",self.frame1)
        self.rbHL = QtWidgets.QRadioButton("HL",self.frame1)
        self.rbHD = QtWidgets.QRadioButton("HD",self.frame1)
        self.rbHP = QtWidgets.QRadioButton("HP",self.frame1)
        self.rbUPE = QtWidgets.QRadioButton("UPE",self.frame1)
        self.rbUPN = QtWidgets.QRadioButton("UPN",self.frame1)
        self.rbU = QtWidgets.QRadioButton("U",self.frame1)
        self.sectiontypes = [self.rbIPE, self.rbHE, self.rbIPN, self.rbHL, self.rbHD, self.rbHP, self.rbUPE, self.rbUPN, self.rbU]
        for sectiontype in self.sectiontypes:
            self.sectionSize.addButton(sectiontype)
        self.comboSections = QtWidgets.QComboBox(self.frame1)
        self.comboSections.setStyleSheet(combostyle)
        self.comboSections.setMinimumSize(QtCore.QSize(width_unit*8, 0))
        
                
        self.label_E1 = QtWidgets.QLabel("Ε:",self.frame1)
        self.label_v1 = QtWidgets.QLabel("v:",self.frame1)
        self.label_G1 = QtWidgets.QLabel("G:",self.frame1)
        self.lineE1 = QtWidgets.QLineEdit(self.frame1)
        self.lineE1.setPlaceholderText("KPa")
        self.linev1 = QtWidgets.QLineEdit(self.frame1)
        self.linev1.setPlaceholderText("only if no G")
        self.lineG1 = QtWidgets.QLineEdit(self.frame1)
        self.lineG1.setPlaceholderText("KPa") 

        self.label_E = QtWidgets.QLabel("E:",self.frame3)
        self.label_G = QtWidgets.QLabel("G:",self.frame3)
        self.label_A = QtWidgets.QLabel("A:",self.frame3)
        self.label_J = QtWidgets.QLabel("J:",self.frame3)
        self.label_Iy = QtWidgets.QLabel("Iy:",self.frame3)
        self.label_Iz = QtWidgets.QLabel("Iz:",self.frame3)
        self.label_W = QtWidgets.QLabel("W:",self.frame3)
        self.label_v = QtWidgets.QLabel("v:",self.frame3)
        self.lineE = QtWidgets.QLineEdit(self.frame3)
        self.lineG = QtWidgets.QLineEdit(self.frame3)
        self.lineA = QtWidgets.QLineEdit(self.frame3)
        self.lineJ = QtWidgets.QLineEdit(self.frame3)
        self.lineIy = QtWidgets.QLineEdit(self.frame3)
        self.lineIz = QtWidgets.QLineEdit(self.frame3)
        self.lineW = QtWidgets.QLineEdit(self.frame3)
        self.linev = QtWidgets.QLineEdit(self.frame3)
        self.lineE.setPlaceholderText("KPa")
        self.lineG.setPlaceholderText("KPa")
        self.lineA.setPlaceholderText("m2")
        self.lineJ.setPlaceholderText("x axis")
        self.lineIy.setPlaceholderText("Major axis")
        self.lineIz.setPlaceholderText("Minor axis")
        self.lineW.setPlaceholderText("kg/m")
        self.linev.setPlaceholderText("only if no G")
        for item in [self.lineE1, self.linev1, self.lineG1, self.lineE, self.lineG, self.lineA, self.lineJ, self.lineIy, self.lineIz, self.lineW, self.linev]:
            item.setStyleSheet(lineeditstyle)
            item.setMinimumSize(QtCore.QSize(width_unit*3, 0))
            item.setValidator(onlyPosFloat)
        for item in [self.label_E1, self.label_v1, self.label_G1, self.label_E, self.label_G, self.label_A, self.label_J, self.label_Iy, self.label_Iz, self.label_W, self.label_v]:
            item.setMinimumSize(QtCore.QSize(width_unit*2, 0))

            
        self.gridframe1 = QtWidgets.QGridLayout(self.frame1)
        self.gridframe1.addWidget(self.firstSection, 0, 0, 1, 4)
        self.gridframe1.addWidget(self.rbIPE, 1, 0, 1, 1)
        self.gridframe1.addWidget(self.rbHE, 2, 0, 1, 1)
        self.gridframe1.addWidget(self.rbIPN, 3, 0, 1, 1)
        self.gridframe1.addWidget(self.rbHL, 1, 1, 1, 1)
        self.gridframe1.addWidget(self.rbHD, 2, 1, 1, 1)
        self.gridframe1.addWidget(self.rbHP, 3, 1, 1, 1)
        self.gridframe1.addWidget(self.rbUPE, 1, 2, 1, 1)
        self.gridframe1.addWidget(self.rbUPN, 2, 2, 1, 1)
        self.gridframe1.addWidget(self.rbU, 3, 2, 1, 1)
        self.gridframe1.addWidget(self.comboSections, 1, 5, 2, 2)
        self.gridframe1.addWidget(self.label_E1, 4, 0, 2, 1)
        self.gridframe1.addWidget(self.lineE1, 4, 1, 2, 1)
        self.gridframe1.addWidget(self.label_v1, 4, 2, 2, 1)
        self.gridframe1.addWidget(self.linev1, 4,3, 2, 1)
        self.gridframe1.addWidget(self.label_G1, 4, 4, 2, 1)
        self.gridframe1.addWidget(self.lineG1, 4, 5, 2, 1)
        self.gridframe3 = QtWidgets.QGridLayout(self.frame3)
        self.gridframe3.addWidget(self.secondSection, 0, 0, 1, 3)
        self.gridframe3.addWidget(self.label_E, 1, 0, 1, 1)
        self.gridframe3.addWidget(self.label_G, 2, 0, 1, 1)
        self.gridframe3.addWidget(self.label_A, 3, 0, 1, 1)
        self.gridframe3.addWidget(self.label_J, 1, 2, 1, 1)
        self.gridframe3.addWidget(self.label_Iy, 2, 2, 1, 1)
        self.gridframe3.addWidget(self.label_Iz, 3, 2, 1, 1)
        self.gridframe3.addWidget(self.label_W, 1, 4, 1, 1)
        self.gridframe3.addWidget(self.label_v, 2, 4, 1, 1)
        self.gridframe3.addWidget(self.lineE, 1, 1, 1, 1)
        self.gridframe3.addWidget(self.lineG, 2, 1, 1, 1)
        self.gridframe3.addWidget(self.lineA, 3, 1, 1, 1)
        self.gridframe3.addWidget(self.lineJ, 1, 3, 1, 1)
        self.gridframe3.addWidget(self.lineIy, 2, 3, 1, 1)
        self.gridframe3.addWidget(self.lineIz, 3, 3, 1, 1)
        self.gridframe3.addWidget(self.lineW, 1, 5, 1, 1)
        self.gridframe3.addWidget(self.linev, 2, 5, 1, 1)
        
        self.btnNewGroup = QtWidgets.QPushButton("Add Group", self.frame4)
        self.btnSaveChangGroup = QtWidgets.QPushButton("Modify", self.frame4)
        self.btnDeleteGroup = QtWidgets.QPushButton("Delete", self.frame4)
        self.gridframe4 = QtWidgets.QGridLayout(self.frame4)
        self.gridframe4.addWidget(self.btnNewGroup, 0, 0, 1, 1)
        self.gridframe4.addWidget(self.btnSaveChangGroup, 0, 1, 1, 1)
        self.gridframe4.addWidget(self.btnDeleteGroup, 0, 2, 1, 1)
        
        
        for line in [self.lineA, self.lineE1, self.linev1, self.lineG1, self.lineE,self.lineG, self.lineJ,self.lineIy, self.lineIz,self.linev, self.lineW]:
            line.textEdited.connect(self.groupEdited)
#            line.textEdited.connect(lambda:(self.btnNewGroup.setEnabled(True)))
#            line.textEdited.connect(lambda:(self.btnSaveChangGroup.setEnabled(False)))
#            line.textEdited.connect(lambda:(self.btnDeleteGroup.setEnabled(False)))
        for rbutton in [self.rbIPE, self.rbHE, self.rbIPN, self.rbHL, self.rbHD,self.rbHP, self.rbUPE, self.rbUPN, self.rbU]:
            rbutton.toggled.connect(self.groupEdited)
#            rbutton.toggled.connect(lambda:(self.btnNewGroup.setEnabled(True)))
#            rbutton.toggled.connect(lambda:(self.btnSaveChangGroup.setEnabled(False)))
#            rbutton.toggled.connect(lambda:(self.btnDeleteGroup.setEnabled(False)))


#------START OF MEMBERS--------------------------------------------------------
        self.tabMembers = QtWidgets.QWidget()
        self.tab_top.addTab(self.tabMembers, "Members")
        self.frame5 = QtWidgets.QFrame(self.tabMembers)
        self.frame6 = QtWidgets.QFrame(self.tabMembers)
        self.frame7 = QtWidgets.QFrame(self.tabMembers)
        label_Elements = QtWidgets.QLabel("Elements",self.tabMembers)
        label_Position = QtWidgets.QLabel("Position",self.tabMembers)
        label_Loads = QtWidgets.QLabel("Loads",self.tabMembers)
        label_Groups = QtWidgets.QLabel("Groups",self.tabMembers)
        
        self.memberstree = QtWidgets.QTreeWidget(self.tabMembers)
        self.memberstree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.memberGrouptree = QtWidgets.QTreeWidget(self.frame6)
        self.memberGrouptree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        for tree in [self.memberstree, self.memberGrouptree]:
            tree.setHeaderHidden(True)
            tree.setStyleSheet(treestyle)
            tree.setFrameShape(QtWidgets.QFrame.Panel)
        self.loadList = QtWidgets.QListWidget(self.tabMembers)
        self.loadList.setStyleSheet(leftliststyle)
        self.loadList.setFrameShape(QtWidgets.QFrame.Panel)
        self.gridMembers = QtWidgets.QGridLayout(self.tabMembers)
        self.gridMembers.addWidget(label_Elements, 0, 0, 1, 1)
        self.gridMembers.addWidget(self.memberstree, 1, 0, 4, 1)
        self.gridMembers.addWidget(label_Position, 0, 1, 1, 1)
        self.gridMembers.addWidget(self.frame5, 1, 1, 1, 1)
        self.gridMembers.addWidget(label_Groups, 0, 2, 1, 1)
        self.gridMembers.addWidget(self.loadList, 3, 1, 1, 1)
        self.gridMembers.addWidget(label_Loads, 2, 1, 1, 1)
        self.gridMembers.addWidget(self.frame6, 1, 2, 3, 1)
        self.gridMembers.addWidget(self.frame7, 4, 1, 1, 2)
        self.gridMembers.setColumnStretch(0,1)
        self.gridMembers.setColumnStretch(1,2.5)
        self.gridMembers.setColumnStretch(2,1)
        label_Start = QtWidgets.QLabel("Start:", self.frame5)
        label_End = QtWidgets.QLabel("End:", self.frame5)
        label_Nodes = QtWidgets.QLabel("Nodes", self.frame5)
        label_Coordinates = QtWidgets.QLabel("Coordinates", self.frame5)
        label_theta = QtWidgets.QLabel("Theta angle", self.frame5)
        self.lineStart = QtWidgets.QLineEdit(self.frame5)
        self.lineStart.setPlaceholderText("x,y,z,meters")
        self.comboStart = QtWidgets.QComboBox(self.frame5)
        self.lineEnd = QtWidgets.QLineEdit(self.frame5)
        self.lineEnd.setPlaceholderText("x,y,z,meters")
        self.comboEnd = QtWidgets.QComboBox(self.frame5)
        self.lineTheta = QtWidgets.QLineEdit(self.frame5)
        self.lineTheta.setPlaceholderText("rads")
        self.lineTheta.setStyleSheet(lineeditstyle)
        self.lineTheta.setMinimumSize(QtCore.QSize(width_unit*3, 0))
        self.lineTheta.setValidator(onlyFloat)
        for item in [self.lineStart, self.lineEnd, self.comboStart, self.comboEnd,self.lineTheta]:
            item.setStyleSheet(combostyle)
        self.gridFrame5 = QtWidgets.QGridLayout(self.frame5)
        self.gridFrame5.addWidget(label_Start, 1, 0, 1, 1)
        self.gridFrame5.addWidget(label_End, 2, 0, 1, 1)
        self.gridFrame5.addWidget(label_Nodes, 0, 2, 1, 1)
        self.gridFrame5.addWidget(label_Coordinates, 0, 1, 1, 1)
        self.gridFrame5.addWidget(label_theta, 3, 0, 1, 1)
        self.gridFrame5.addWidget(self.lineStart, 1, 1, 1, 1)
        self.gridFrame5.addWidget(self.comboStart, 1, 2, 1, 1)
        self.gridFrame5.addWidget(self.lineEnd, 2, 1, 1, 1)
        self.gridFrame5.addWidget(self.comboEnd, 2, 2, 1, 1)
        self.gridFrame5.addWidget(self.lineTheta, 3, 1, 1, 1)
        self.gridFrame5.setColumnStretch(0,1)
        self.gridFrame5.setColumnStretch(1,2)
        self.gridFrame5.setColumnStretch(2,2)
        self.btnNewMember = QtWidgets.QPushButton("Add member", self.frame7)
        self.btnSaveChangMember = QtWidgets.QPushButton("Save changes", self.frame7)
        self.btnDeleteMember = QtWidgets.QPushButton("Delete", self.frame7)
        self.gridframe7 = QtWidgets.QGridLayout(self.frame7)
        self.gridframe7.addWidget(self.btnNewMember, 0, 0, 1, 1)
        self.gridframe7.addWidget(self.btnSaveChangMember, 0, 1, 1, 1)
        self.gridframe7.addWidget(self.btnDeleteMember, 0, 2, 1, 1)
                   

#------START OF SUPPORTS-------------------------------------------------------
        self.tabSupports = QtWidgets.QWidget()
        self.tab_top.addTab(self.tabSupports, "Supports")
        self.supportstree = QtWidgets.QTreeWidget(self.tabSupports)
        self.supportstree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.supportstree.setHeaderHidden(True)
#        self.supportstree.header().setStretchLastSection(False)
#        self.supportstree.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.supportstree.setStyleSheet(treestyle)
        self.supportstree.setFrameShape(QtWidgets.QFrame.Panel)

        self.frame8 = QtWidgets.QFrame(self.tabSupports)
        self.frame9 = QtWidgets.QFrame(self.tabSupports)
        self.frame9_1 = QtWidgets.QFrame(self.tabSupports)
        self.tabSupportDetails = QtWidgets.QTabWidget(self.tabSupports)
        self.tabSupportDetails.setStyleSheet(tabstyle)
        self.tab_sup_rotation = QtWidgets.QWidget()
        self.tabSupportDetails.addTab(self.tab_sup_rotation, "Rotation angles")
        self.tab_stiffness = QtWidgets.QWidget()
        self.tabSupportDetails.addTab(self.tab_stiffness, "Support stiffness")

        self.comboSupNodes = QtWidgets.QComboBox(self.frame8)
        self.comboSupNodes.setStyleSheet(combostyle)
        self.comboSupNodes.setMinimumSize(QtCore.QSize(width_unit*8, 0))

        label_Supports = QtWidgets.QLabel("Supported Nodes",self.tabSupports)
        label_Node = QtWidgets.QLabel("Nodes",self.tabSupports)
        label_Degrees = QtWidgets.QLabel("Degrees of freedom",self.tabSupports)
        
        self.sup_x = QtWidgets.QRadioButton("x",self.frame9)
        self.sup_y = QtWidgets.QRadioButton("y",self.frame9)
        self.sup_z = QtWidgets.QRadioButton("z",self.frame9)
        self.sup_rotx = QtWidgets.QRadioButton("θx",self.frame9)
        self.sup_roty = QtWidgets.QRadioButton("θy",self.frame9)
        self.sup_rotz = QtWidgets.QRadioButton("θz",self.frame9)
        for s in [self.sup_x, self.sup_y, self.sup_z, self.sup_rotx, self.sup_roty, self.sup_rotz]:
            s.setAutoExclusive(False)
        self.gridframe9 = QtWidgets.QGridLayout(self.frame9)
        self.gridframe9.addWidget(self.sup_x, 0, 0, 1, 1)
        self.gridframe9.addWidget(self.sup_y, 1, 0, 1, 1)
        self.gridframe9.addWidget(self.sup_z, 2, 0, 1, 1)
        self.gridframe9.addWidget(self.sup_rotx, 0, 1, 1, 1)
        self.gridframe9.addWidget(self.sup_roty, 1, 1, 1, 1)
        self.gridframe9.addWidget(self.sup_rotz, 2, 1, 1, 1)
        self.gridSupports = QtWidgets.QGridLayout(self.tabSupports)
        self.gridSupports.addWidget(label_Supports, 0, 0, 1, 1)
        self.gridSupports.addWidget(self.supportstree, 1, 0, 5, 1)
        self.gridSupports.addWidget(label_Node, 0, 1, 1, 1)
        self.gridSupports.addWidget(label_Degrees, 0, 2, 1, 2)
        self.gridSupports.addWidget(self.frame8, 1, 1, 2, 1)
        self.gridSupports.addWidget(self.frame9, 1, 2, 2, 2)
        self.gridSupports.addWidget(self.tabSupportDetails, 3, 1, 2, 2)
        self.gridSupports.addWidget(self.frame9_1, 5, 1, 1, 2)
        self.gridSupports.setColumnStretch(0,1)
        self.gridSupports.setColumnStretch(1,1)
        self.gridSupports.setColumnStretch(2,2.5)
        self.gridSupports.setRowStretch(0,1)
        for row in range(1,6):
            self.gridSupports.setRowStretch(row,3)
        self.btnNewSupport = QtWidgets.QPushButton("Add Support", self.frame9_1)
        self.btnSaveChangSupport = QtWidgets.QPushButton("Save changes", self.frame9_1)
        self.btnDeleteSupport = QtWidgets.QPushButton("Delete", self.frame9_1)
        self.gridframe9_1 = QtWidgets.QGridLayout(self.frame9_1)
        self.gridframe9_1.addWidget(self.btnNewSupport, 0, 0, 1, 1)
        self.gridframe9_1.addWidget(self.btnSaveChangSupport, 0, 1, 1, 1)
        self.gridframe9_1.addWidget(self.btnDeleteSupport, 0, 2, 1, 1)
        

        self.frame10 = QtWidgets.QFrame(self.tab_sup_rotation)
        label_rotation_angles = QtWidgets.QLabel("Enter the angles per\n axis of the support",self.frame10)
        self.frame11 = QtWidgets.QFrame(self.tab_sup_rotation)        
        gridtab_sup_rotation = QtWidgets.QGridLayout(self.tab_sup_rotation)
        gridtab_sup_rotation.addWidget(self.frame10, 0, 0, 1, 1)
        gridtab_sup_rotation.addWidget(self.frame11, 0, 1, 2, 1)
        self.rot_x = QtWidgets.QLineEdit(self.frame11)
        self.rot_y = QtWidgets.QLineEdit(self.frame11)
        self.rot_z = QtWidgets.QLineEdit(self.frame11)
        self.rot_x.setPlaceholderText("rad")
        self.rot_y.setPlaceholderText("rad")
        self.rot_z.setPlaceholderText("rad")
        label_axis_x = QtWidgets.QLabel("   Axis x:",self.frame11)
        label_axis_y = QtWidgets.QLabel("   Axis y:",self.frame11)
        label_axis_z = QtWidgets.QLabel("   Axis z:",self.frame11)
        
        gridframe11 = QtWidgets.QGridLayout(self.frame11)
        gridframe11.addWidget(self.rot_x, 0, 1, 1, 1)
        gridframe11.addWidget(self.rot_y, 1, 1, 1, 1)
        gridframe11.addWidget(self.rot_z, 2, 1, 1, 1)
        gridframe11.addWidget(label_axis_x, 0, 0, 1, 1)
        gridframe11.addWidget(label_axis_y, 1, 0, 1, 1)
        gridframe11.addWidget(label_axis_z, 2, 0, 1, 1)
        for item in [self.rot_x, self.rot_y, self.rot_z]:
            item.setStyleSheet(lineeditstyle)
            item.setMinimumSize(QtCore.QSize(width_unit*3, 0))
            item.setValidator(onlyFloat)
        gridtab_sup_rotation.setColumnStretch(0,1)
        gridtab_sup_rotation.setColumnStretch(1,2)
        gridframe11.setColumnStretch(0,1)
        gridframe11.setColumnStretch(1,1)
        gridframe11.setColumnStretch(2,1)
                    
        self.frame12 = QtWidgets.QFrame(self.tab_stiffness)
        label_stiffnesses = QtWidgets.QLabel("Enter the values of\nthe stiffness for\neach degree of\nfreedom",self.frame12)
        self.frame13 = QtWidgets.QFrame(self.tab_stiffness)
        gridtab_sup_stiffness = QtWidgets.QGridLayout(self.tab_stiffness)
        gridtab_sup_stiffness.addWidget(self.frame12, 0, 0, 2, 1)
        gridtab_sup_stiffness.addWidget(self.frame13, 0, 1, 2, 1)
        self.stiff_x = QtWidgets.QLineEdit(self.frame13)
        self.stiff_y = QtWidgets.QLineEdit(self.frame13)
        self.stiff_z = QtWidgets.QLineEdit(self.frame13)
        self.stiff_rotx = QtWidgets.QLineEdit(self.frame13)
        self.stiff_roty = QtWidgets.QLineEdit(self.frame13)
        self.stiff_rotz = QtWidgets.QLineEdit(self.frame13)
        self.stiff_x.setPlaceholderText("KN/m")
        self.stiff_y.setPlaceholderText("KN/m")
        self.stiff_z.setPlaceholderText("KN/m")
        self.stiff_rotx.setPlaceholderText("KNm/rad")
        self.stiff_roty.setPlaceholderText("KNm/rad")
        self.stiff_rotz.setPlaceholderText("KNm/rad")
        label_stiff_x = QtWidgets.QLabel("    x:",self.frame13)
        label_stiff_y = QtWidgets.QLabel("    y:",self.frame13)
        label_stiff_z = QtWidgets.QLabel("    z:",self.frame13)
        label_stiff_rotx = QtWidgets.QLabel("    Rot x:",self.frame13)
        label_stiff_roty = QtWidgets.QLabel("    Rot y:",self.frame13)
        label_stiff_rotz = QtWidgets.QLabel("    Rot z:",self.frame13)
        gridframe13 = QtWidgets.QGridLayout(self.frame13)
        gridframe13.addWidget(self.stiff_x, 0, 1, 1, 1)
        gridframe13.addWidget(self.stiff_y, 1, 1, 1, 1)
        gridframe13.addWidget(self.stiff_z, 2, 1, 1, 1)
        gridframe13.addWidget(self.stiff_rotx, 0, 3, 1, 1)
        gridframe13.addWidget(self.stiff_roty, 1, 3, 1, 1)
        gridframe13.addWidget(self.stiff_rotz, 2, 3, 1, 1)
        gridframe13.addWidget(label_stiff_x, 0, 0, 1, 1)
        gridframe13.addWidget(label_stiff_y, 1, 0, 1, 1)
        gridframe13.addWidget(label_stiff_z, 2, 0, 1, 1)
        gridframe13.addWidget(label_stiff_rotx, 0, 2, 1, 1)
        gridframe13.addWidget(label_stiff_roty, 1, 2, 1, 1)
        gridframe13.addWidget(label_stiff_rotz, 2, 2, 1, 1)
        for item in [self.stiff_x, self.stiff_y, self.stiff_z, self.stiff_rotx, self.stiff_roty, self.stiff_rotz]:
            item.setStyleSheet(lineeditstyle)
            item.setMinimumSize(QtCore.QSize(width_unit*3, 0))
            item.setValidator(onlyPosFloat)
        gridtab_sup_stiffness.setColumnStretch(0,1)
        gridtab_sup_stiffness.setColumnStretch(1,2)
        gridframe13.setColumnStretch(0,1)
        gridframe13.setColumnStretch(1,1)
        gridframe13.setColumnStretch(2,1)
        gridframe13.setColumnStretch(3,1)
        
#------START OF DISPLACEMENTS--------------------------------------------------
        self.tabDisps = QtWidgets.QWidget()
        self.tab_top.addTab(self.tabDisps, "Displacements")
        self.dispstree = QtWidgets.QTreeWidget(self.tabDisps)
        self.dispstree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.dispstree.setHeaderHidden(True)
#        self.dispstree.header().setStretchLastSection(False)
#        self.dispstree.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        label_Disps = QtWidgets.QLabel("Supported Nodes",self.tabDisps)
        self.dispstree.setStyleSheet(treestyle)
        self.dispstree.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame29 = QtWidgets.QFrame(self.tabDisps)
        label_Node_disp = QtWidgets.QLabel("Nodes",self.tabDisps)
        self.comboDispNodes = QtWidgets.QComboBox(self.frame29)
        self.comboDispNodes.setStyleSheet(combostyle)
        self.comboDispNodes.setMinimumSize(QtCore.QSize(width_unit*8, 0))
        self.frame29_1 = QtWidgets.QFrame(self.tabDisps)
#        self.tabSupportDetails.addTab(self.tabDisps, "Displacements")
        self.frame14 = QtWidgets.QFrame(self.tabDisps)
        label_displacements = QtWidgets.QLabel("Enter the values of\nthe displacement for\neach degree of\nfreedom",self.frame14)
        self.frame15 = QtWidgets.QFrame(self.tabDisps)
#        gridtab_sup_disps = QtWidgets.QGridLayout(self.tabDisps)
#        gridtab_sup_disps.addWidget(self.frame14, 0, 0, 2, 1)
#        gridtab_sup_disps.addWidget(self.frame15, 0, 1, 2, 1)
        self.disp_x = QtWidgets.QLineEdit(self.frame15)
        self.disp_y = QtWidgets.QLineEdit(self.frame15)
        self.disp_z = QtWidgets.QLineEdit(self.frame15)
        self.disp_rotx = QtWidgets.QLineEdit(self.frame15)
        self.disp_roty = QtWidgets.QLineEdit(self.frame15)
        self.disp_rotz = QtWidgets.QLineEdit(self.frame15)
        self.disp_x.setPlaceholderText("m")
        self.disp_y.setPlaceholderText("m")
        self.disp_z.setPlaceholderText("m")
        self.disp_rotx.setPlaceholderText("rad")
        self.disp_roty.setPlaceholderText("rad")
        self.disp_rotz.setPlaceholderText("rad")
        label_disp_x = QtWidgets.QLabel("    x:",self.frame15)
        label_disp_y = QtWidgets.QLabel("    y:",self.frame15)
        label_disp_z = QtWidgets.QLabel("    z:",self.frame15)
        label_disp_rotx = QtWidgets.QLabel("    Rot x:",self.frame15)
        label_disp_roty = QtWidgets.QLabel("    Rot y:",self.frame15)
        label_disp_rotz = QtWidgets.QLabel("    Rot z:",self.frame15)
        gridDisps = QtWidgets.QGridLayout(self.tabDisps)
        gridDisps.addWidget(label_Disps,0,0,1,1)
        gridDisps.addWidget(label_Node_disp,0,1,1,1)
        gridDisps.addWidget(self.dispstree,1,0,4,1)
        gridDisps.addWidget(self.frame29,1,1,1,2)
        gridDisps.addWidget(self.frame14,2,1,2,1)
        gridDisps.addWidget(self.frame15,2,2,2,1)
        gridDisps.addWidget(self.frame29_1,4,1,1,2)
        j=0
        for i in [1,3,3,3,3]:
            gridDisps.setRowStretch(j,i)
            j+=1
        j=0
        for i in [1,1,2]:
            gridDisps.setColumnStretch(j,i)
            j+=1
        gridframe15 = QtWidgets.QGridLayout(self.frame15)
        gridframe15.addWidget(self.disp_x, 0, 1, 1, 1)
        gridframe15.addWidget(self.disp_y, 1, 1, 1, 1)
        gridframe15.addWidget(self.disp_z, 2, 1, 1, 1)
        gridframe15.addWidget(self.disp_rotx, 0, 3, 1, 1)
        gridframe15.addWidget(self.disp_roty, 1, 3, 1, 1)
        gridframe15.addWidget(self.disp_rotz, 2, 3, 1, 1)
        gridframe15.addWidget(label_disp_x, 0, 0, 1, 1)
        gridframe15.addWidget(label_disp_y, 1, 0, 1, 1)
        gridframe15.addWidget(label_disp_z, 2, 0, 1, 1)
        gridframe15.addWidget(label_disp_rotx, 0, 2, 1, 1)
        gridframe15.addWidget(label_disp_roty, 1, 2, 1, 1)
        gridframe15.addWidget(label_disp_rotz, 2, 2, 1, 1)
        for i in range(4):
            gridframe15.setColumnStretch(i,1)
        gridframe29 = QtWidgets.QGridLayout(self.frame29)
        gridframe29.addWidget(self.comboDispNodes,1,0,1,1)
        for i in range(4):
            gridframe29.setRowStretch(i,1)
        for i in range(3):
            gridframe29.setColumnStretch(i,1)
        for item in [self.disp_x, self.disp_y, self.disp_z, self.disp_rotx, self.disp_roty, self.disp_rotz]:
            item.setStyleSheet(lineeditstyle)
            item.setMinimumSize(QtCore.QSize(width_unit*3, 0))
            item.setValidator(onlyFloat)
        self.btnNewDisplacement = QtWidgets.QPushButton("Add displacement", self.frame29_1)
        self.btnSaveChangDisp = QtWidgets.QPushButton("Save changes", self.frame29_1)
        self.btnDeleteDisp = QtWidgets.QPushButton("Delete", self.frame29_1)
        self.gridframe29_1 = QtWidgets.QGridLayout(self.frame29_1)
        self.gridframe29_1.addWidget(self.btnNewDisplacement, 0, 0, 1, 1)
        self.gridframe29_1.addWidget(self.btnSaveChangDisp, 0, 1, 1, 1)
        self.gridframe29_1.addWidget(self.btnDeleteDisp, 0, 2, 1, 1)
#------START OF RELEASES-------------------------------------------------------
        self.tabRels = QtWidgets.QWidget()
        self.tab_top.addTab(self.tabRels, "Node Releases")
        self.relstree = QtWidgets.QTreeWidget(self.tabRels)
        self.relstree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.relstree.setHeaderHidden(True)
#        self.relstree.header().setStretchLastSection(False)
#        self.relstree.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        label_Rels = QtWidgets.QLabel("Node Releases",self.tabRels)
        self.relstree.setStyleSheet(treestyle)
        self.relstree.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame30 = QtWidgets.QFrame(self.tabRels)
        label_Node_rel = QtWidgets.QLabel("Elements",self.frame30)
        self.comboRelMembers = QtWidgets.QComboBox(self.frame30)
        self.comboRelMembers.setStyleSheet(combostyle)
        self.comboRelMembers.setMinimumSize(QtCore.QSize(width_unit*8, 0))
        self.frame30_1 = QtWidgets.QFrame(self.tabRels)
        self.frame31 = QtWidgets.QFrame(self.tabRels)
        label_releases = QtWidgets.QLabel("Enter the values of\nthe displacement for\neach degree of\nfreedom",self.frame31)
        self.frame32 = QtWidgets.QFrame(self.tabRels)
        label_startnode = QtWidgets.QLabel("Start Node",self.frame32)
        self.rel_x = QtWidgets.QLineEdit(self.frame32)
        self.rel_y = QtWidgets.QLineEdit(self.frame32)
        self.rel_z = QtWidgets.QLineEdit(self.frame32)
        self.rel_rotx = QtWidgets.QLineEdit(self.frame32)
        self.rel_roty = QtWidgets.QLineEdit(self.frame32)
        self.rel_rotz = QtWidgets.QLineEdit(self.frame32)
        self.rel_x.setPlaceholderText("rad")
        self.rel_y.setPlaceholderText("rad")
        self.rel_z.setPlaceholderText("rad")
        self.rel_rotx.setPlaceholderText("rad")
        self.rel_roty.setPlaceholderText("rad")
        self.rel_rotz.setPlaceholderText("rad")
        label_rel_x = QtWidgets.QLabel("    x:",self.frame32)
        label_rel_y = QtWidgets.QLabel("    y:",self.frame32)
        label_rel_z = QtWidgets.QLabel("    z:",self.frame32)
        label_rel_rotx = QtWidgets.QLabel("    Rot x:",self.frame32)
        label_rel_roty = QtWidgets.QLabel("    Rot y:",self.frame32)
        label_rel_rotz = QtWidgets.QLabel("    Rot z:",self.frame32)
        label_stopnode = QtWidgets.QLabel("End Node",self.frame32)
        self.rel_x2 = QtWidgets.QLineEdit(self.frame32)
        self.rel_y2 = QtWidgets.QLineEdit(self.frame32)
        self.rel_z2 = QtWidgets.QLineEdit(self.frame32)
        self.rel_rotx2 = QtWidgets.QLineEdit(self.frame32)
        self.rel_roty2 = QtWidgets.QLineEdit(self.frame32)
        self.rel_rotz2 = QtWidgets.QLineEdit(self.frame32)
        self.rel_x2.setPlaceholderText("rad")
        self.rel_y2.setPlaceholderText("rad")
        self.rel_z2.setPlaceholderText("rad")
        self.rel_rotx2.setPlaceholderText("rad")
        self.rel_roty2.setPlaceholderText("rad")
        self.rel_rotz2.setPlaceholderText("rad")
        label_rel_x2 = QtWidgets.QLabel("    x:",self.frame32)
        label_rel_y2 = QtWidgets.QLabel("    y:",self.frame32)
        label_rel_z2 = QtWidgets.QLabel("    z:",self.frame32)
        label_rel_rotx2 = QtWidgets.QLabel("    Rot x:",self.frame32)
        label_rel_roty2 = QtWidgets.QLabel("    Rot y:",self.frame32)
        label_rel_rotz2 = QtWidgets.QLabel("    Rot z:",self.frame32)
        gridRels = QtWidgets.QGridLayout(self.tabRels)
        gridRels.addWidget(label_Rels,0,0,1,1)
        gridRels.addWidget(label_Node_rel,0,1,1,1)
        gridRels.addWidget(self.relstree,1,0,4,1)
        gridRels.addWidget(self.frame30,1,1,1,1)
        gridRels.addWidget(self.frame31,2,1,2,1)
        gridRels.addWidget(self.frame32,0,2,4,1)
        gridRels.addWidget(self.frame30_1,4,1,1,2)
        j=0
        for i in [1,3,3,3,3]:
            gridRels.setRowStretch(j,i)
            j+=1
        j=0
        for i in [1,1,2]:
            gridRels.setColumnStretch(j,i)
            j+=1
        gridframe32 = QtWidgets.QGridLayout(self.frame32)
        gridframe32.addWidget(label_startnode, 0, 0, 1, 1)
        gridframe32.addWidget(self.rel_x, 1, 1, 1, 1)
        gridframe32.addWidget(self.rel_y, 2, 1, 1, 1)
        gridframe32.addWidget(self.rel_z, 3, 1, 1, 1)
        gridframe32.addWidget(self.rel_rotx, 1, 3, 1, 1)
        gridframe32.addWidget(self.rel_roty, 2, 3, 1, 1)
        gridframe32.addWidget(self.rel_rotz, 3, 3, 1, 1)
        gridframe32.addWidget(label_rel_x, 1, 0, 1, 1)
        gridframe32.addWidget(label_rel_y, 2, 0, 1, 1)
        gridframe32.addWidget(label_rel_z, 3, 0, 1, 1)
        gridframe32.addWidget(label_rel_rotx, 1, 2, 1, 1)
        gridframe32.addWidget(label_rel_roty, 2, 2, 1, 1)
        gridframe32.addWidget(label_rel_rotz, 3, 2, 1, 1)
        gridframe32.addWidget(label_stopnode, 4, 0, 1, 1)
        gridframe32.addWidget(self.rel_x2, 5, 1, 1, 1)
        gridframe32.addWidget(self.rel_y2, 6, 1, 1, 1)
        gridframe32.addWidget(self.rel_z2, 7, 1, 1, 1)
        gridframe32.addWidget(self.rel_rotx2, 5, 3, 1, 1)
        gridframe32.addWidget(self.rel_roty2, 6, 3, 1, 1)
        gridframe32.addWidget(self.rel_rotz2, 7, 3, 1, 1)
        gridframe32.addWidget(label_rel_x2, 5, 0, 1, 1)
        gridframe32.addWidget(label_rel_y2, 6, 0, 1, 1)
        gridframe32.addWidget(label_rel_z2, 7, 0, 1, 1)
        gridframe32.addWidget(label_rel_rotx2, 5, 2, 1, 1)
        gridframe32.addWidget(label_rel_roty2, 6, 2, 1, 1)
        gridframe32.addWidget(label_rel_rotz2, 7, 2, 1, 1)
        for i in range(4):
            gridframe32.setColumnStretch(i,1)
        for item in [self.rel_x, self.rel_y, self.rel_z, self.rel_rotx, self.rel_roty, self.rel_rotz,self.rel_x2, self.rel_y2, self.rel_z2, self.rel_rotx2, self.rel_roty2, self.rel_rotz2]:
            item.setStyleSheet(lineeditstyle)
            item.setMinimumSize(QtCore.QSize(width_unit*3, 0))
            item.setValidator(onlyFloat)
        self.btnNewRelease = QtWidgets.QPushButton("Add Release", self.frame30_1)
        self.btnSaveChangRel = QtWidgets.QPushButton("Save changes", self.frame30_1)
        self.btnDeleteRel = QtWidgets.QPushButton("Delete", self.frame30_1)
        self.gridframe29_1 = QtWidgets.QGridLayout(self.frame30_1)
        self.gridframe29_1.addWidget(self.btnNewRelease, 0, 0, 1, 1)
        self.gridframe29_1.addWidget(self.btnSaveChangRel, 0, 1, 1, 1)
        self.gridframe29_1.addWidget(self.btnDeleteRel, 0, 2, 1, 1)
#------START OF RIGID NODES----------------------------------------------------
        self.tabRigs = QtWidgets.QWidget()
        self.tab_top.addTab(self.tabRigs, "Rigid Nodes")
        self.rigstree = QtWidgets.QTreeWidget(self.tabRigs)
        self.rigstree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.rigstree.setHeaderHidden(True)
#        self.rigstree.header().setStretchLastSection(False)
#        self.rigstree.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        label_Rigs = QtWidgets.QLabel("Node Releases",self.tabRigs)
        self.rigstree.setStyleSheet(treestyle)
        self.rigstree.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame33 = QtWidgets.QFrame(self.tabRigs)
        self.frame34 = QtWidgets.QFrame(self.tabRigs)
        self.frame35 = QtWidgets.QFrame(self.tabRigs)
        self.frame35_1 = QtWidgets.QFrame(self.tabRigs)
        label_Elem_rig = QtWidgets.QLabel("Elements",self.frame33)
        self.comboRigMembers = QtWidgets.QComboBox(self.frame33)
        self.comboRigMembers.setStyleSheet(combostyle)
        self.comboRigMembers.setMinimumSize(QtCore.QSize(width_unit*8, 0))
        label_rig_start = QtWidgets.QLabel("Start:",self.frame34)
        label_rig_dxs = QtWidgets.QLabel("Dx:",self.frame34)
        label_rig_dys = QtWidgets.QLabel("Dy:",self.frame34)
        label_rig_dzs = QtWidgets.QLabel("Dz:",self.frame34)
        label_rig_end = QtWidgets.QLabel("End:",self.frame35)
        label_rig_dxe = QtWidgets.QLabel("Dx:",self.frame35)
        label_rig_dye = QtWidgets.QLabel("Dy:",self.frame35)
        label_rig_dze = QtWidgets.QLabel("Dz:",self.frame35)
        self.rig_dxs = QtWidgets.QLineEdit(self.frame34)
        self.rig_dys = QtWidgets.QLineEdit(self.frame34)
        self.rig_dzs = QtWidgets.QLineEdit(self.frame34)
        self.rig_dxe = QtWidgets.QLineEdit(self.frame35)
        self.rig_dye = QtWidgets.QLineEdit(self.frame35)
        self.rig_dze = QtWidgets.QLineEdit(self.frame35)
        for item in [self.rig_dxs, self.rig_dys, self.rig_dzs, self.rig_dxe, self.rig_dye, self.rig_dze]:
            item.setStyleSheet(lineeditstyle)
            item.setMinimumSize(QtCore.QSize(width_unit*3, 0))
            item.setValidator(onlyFloat)
        gridframe34 = QtWidgets.QGridLayout(self.frame34)
        gridframe34.addWidget(label_rig_start, 0, 0, 1, 1)
        gridframe34.addWidget(label_rig_dxs, 1, 0, 1, 1)
        gridframe34.addWidget(label_rig_dys, 2, 0, 1, 1)
        gridframe34.addWidget(label_rig_dzs, 3, 0, 1, 1)
        gridframe34.addWidget(self.rig_dxs, 1, 1, 1, 1)
        gridframe34.addWidget(self.rig_dys, 2, 1, 1, 1)
        gridframe34.addWidget(self.rig_dzs, 3, 1, 1, 1)
        gridframe35 = QtWidgets.QGridLayout(self.frame35)
        gridframe35.addWidget(label_rig_end, 0, 0, 1, 1)
        gridframe35.addWidget(label_rig_dxe, 1, 0, 1, 1)
        gridframe35.addWidget(label_rig_dye, 2, 0, 1, 1)
        gridframe35.addWidget(label_rig_dze, 3, 0, 1, 1)
        gridframe35.addWidget(self.rig_dxe, 1, 1, 1, 1)
        gridframe35.addWidget(self.rig_dye, 2, 1, 1, 1)
        gridframe35.addWidget(self.rig_dze, 3, 1, 1, 1)
        for grid in [gridframe34, gridframe35]:
            for i in range(2):
                grid.setColumnStretch(i,1)
        gridRigs = QtWidgets.QGridLayout(self.tabRigs)
        gridRigs.addWidget(label_Rigs,0,0,1,1)
        gridRigs.addWidget(label_Elem_rig,0,1,1,1)
        gridRigs.addWidget(self.rigstree,1,0,2,1)
        gridRigs.addWidget(self.frame33,1,1,1,1)
        gridRigs.addWidget(self.frame34,1,2,1,1)
        gridRigs.addWidget(self.frame35,1,3,1,1)
        gridRigs.addWidget(self.frame35_1,2,1,1,3)
        j=0
        for i in [1,10,2]:
            gridRigs.setRowStretch(j,i)
            j+=1
        j=0
        for i in [1,1,1,1]:
            gridRigs.setColumnStretch(j,i)
            j+=1
        self.btnNewRig = QtWidgets.QPushButton("Add", self.frame30_1)
        self.btnSaveChangRig = QtWidgets.QPushButton("Save changes", self.frame30_1)
        self.btnDeleteRig = QtWidgets.QPushButton("Delete", self.frame30_1)
        self.gridframe35_1 = QtWidgets.QGridLayout(self.frame35_1)
        self.gridframe35_1.addWidget(self.btnNewRig, 0, 0, 1, 1)
        self.gridframe35_1.addWidget(self.btnSaveChangRig, 0, 1, 1, 1)
        self.gridframe35_1.addWidget(self.btnDeleteRig, 0, 2, 1, 1)
#------>bottom tabs
#------>nodal loads
        self.bottomframe = QtWidgets.QFrame(self.frameright)
        self.tab_bottom = QtWidgets.QTabWidget(self.bottomframe)
        self.tab_bottom.setStyleSheet(tabstyle)
#        self.tab_bottom.currentChanged.connect(self.current_tab_changed)
        self.tab_NodalLoads = QtWidgets.QWidget()
        self.tab_bottom.addTab(self.tab_NodalLoads, "Nodal Loads")
        self.tab_MemberLoads = QtWidgets.QWidget()
        self.tab_bottom.addTab(self.tab_MemberLoads, "Member Loads")
#        self.loadGroupList = QtWidgets.QListWidget()#tha exei me kathe epilogh melous tin arxi -telos kai fortia
#        self.loadGroupList.addItems(model.Beam.LoadGroups)#na to allajw
        horizontalbottom = QtWidgets.QHBoxLayout(self.bottomframe)
        horizontalbottom.setContentsMargins(0, 0, 0, 0)
        horizontalbottom.setSpacing(0)
        horizontalbottom.addWidget(self.tab_bottom)
#        horizontalbottom.addWidget(self.loadGroupList)
        horizontalbottom.setStretch(0, 3)
        horizontalbottom.setStretch(1, 1) 
        self.frame16 = QtWidgets.QFrame(self.tab_NodalLoads)
        self.frame17 = QtWidgets.QFrame(self.tab_NodalLoads)
        self.frame18 = QtWidgets.QFrame(self.tab_NodalLoads)
        self.frame19 = QtWidgets.QFrame(self.tab_NodalLoads)
        self.frame20 = QtWidgets.QFrame(self.tab_NodalLoads)
        gridtab_NodalLoads = QtWidgets.QGridLayout(self.tab_NodalLoads)
        gridtab_NodalLoads.addWidget(self.frame16, 0, 0, 1, 1)
        gridtab_NodalLoads.addWidget(self.frame17, 0, 1, 1, 1)
        gridtab_NodalLoads.addWidget(self.frame18, 1, 0, 1, 1)
        gridtab_NodalLoads.addWidget(self.frame19, 1, 1, 1, 1)
        gridtab_NodalLoads.addWidget(self.frame20, 2, 0, 2, 2)
        gridtab_NodalLoads.setColumnStretch(0,3)
        gridtab_NodalLoads.setColumnStretch(1,2)
#        gridtab_NodalLoads.setRowStretch(0,1)
#        gridtab_NodalLoads.setRowStretch(1,1)
#        gridtab_NodalLoads.setRowStretch(2,2)
        vertical_loadaNode = QtWidgets.QVBoxLayout(self.frame16)
        vertical_nodalLoads = QtWidgets.QVBoxLayout(self.frame18)
        vertical_loadGroups = QtWidgets.QVBoxLayout(self.frame19)
        gridframe20 = QtWidgets.QGridLayout(self.frame20)
        label_LoadselectNode = QtWidgets.QLabel("Select a node:",self.frame16)
        self.combo_loadNodes = QtWidgets.QComboBox(self.frame16)
        self.combo_loadNodes.setMaximumSize(QtCore.QSize(70,20))  
        vertical_loadaNode.addWidget(label_LoadselectNode)
        vertical_loadaNode.addWidget(self.combo_loadNodes)
        self.radio_force = QtWidgets.QRadioButton('Force', self.frame18)
        self.radio_moment = QtWidgets.QRadioButton('Moment', self.frame18)
        vertical_nodalLoads.addWidget(self.radio_force)
        vertical_nodalLoads.addWidget(self.radio_moment)
        label_LoadGroup = QtWidgets.QLabel("Load Group:",self.frame19)
        self.combo_loadGroups = QtWidgets.QComboBox(self.frame19)
        self.combo_loadGroups.setMaximumSize(QtCore.QSize(70,20)) 
        vertical_loadGroups.addWidget(label_LoadGroup)
        vertical_loadGroups.addWidget(self.combo_loadGroups)
        label_Loadvectorcomponents = QtWidgets.QLabel("Enter load vector components:",self.frame20)
        label_loadX = QtWidgets.QLabel("X :",self.frame20)
        label_loadY = QtWidgets.QLabel("Y :",self.frame20)
        label_loadZ = QtWidgets.QLabel("Z :",self.frame20)
        self.load_x = QtWidgets.QLineEdit(self.frame20)
        self.load_x.setPlaceholderText("KN")
        self.load_y = QtWidgets.QLineEdit(self.frame20)
        self.load_y.setPlaceholderText("KN")
        self.load_z = QtWidgets.QLineEdit(self.frame20)
        self.load_z.setPlaceholderText("KN")
        self.btnAddNodalLoad = QtWidgets.QPushButton("Add Load", self.frame20)
        gridframe20.addWidget(label_Loadvectorcomponents,0,0,1,8)
        gridframe20.addWidget(label_loadX,1,0,1,1)
        gridframe20.addWidget(self.load_x,1,1,1,1)
        gridframe20.addWidget(label_loadY,1,2,1,1)
        gridframe20.addWidget(self.load_y,1,3,1,1)
        gridframe20.addWidget(label_loadZ,1,4,1,1)
        gridframe20.addWidget(self.load_z,1,5,1,1)
        gridframe20.addWidget(self.btnAddNodalLoad,1,7,1,1)
        for item in [self.combo_loadNodes, self.combo_loadGroups]:
            item.setStyleSheet(combostyle)
        for item in [self.load_x, self.load_y, self.load_z]:
            item.setStyleSheet(lineeditstyle)
            item.setMinimumSize(QtCore.QSize(width_unit*3, 0))
            item.setValidator(onlyFloat)
#----->member loads
        self.frame21 = QtWidgets.QFrame(self.tab_MemberLoads)
        self.frame22 = QtWidgets.QFrame(self.tab_MemberLoads)
        self.frame23 = QtWidgets.QFrame(self.tab_MemberLoads)
        self.frame24 = QtWidgets.QFrame(self.tab_MemberLoads)
        self.frame25 = QtWidgets.QFrame(self.tab_MemberLoads)
        self.frame26 = QtWidgets.QFrame(self.tab_MemberLoads)
        self.frame27 = QtWidgets.QFrame(self.tab_MemberLoads)
        self.frame28 = QtWidgets.QFrame(self.tab_MemberLoads)
        for item in [self.frame25, self.frame26, self.frame27, self.frame28]:
            item.hide()
        gridtab_MemberLoads = QtWidgets.QGridLayout(self.tab_MemberLoads)
        gridtab_MemberLoads.addWidget(self.frame21, 0, 0, 1, 1)
        gridtab_MemberLoads.addWidget(self.frame22, 0, 1, 1, 1)
        gridtab_MemberLoads.addWidget(self.frame23, 1, 0, 1, 1)
        gridtab_MemberLoads.addWidget(self.frame24, 1, 1, 1, 1)
        gridtab_MemberLoads.addWidget(self.frame25, 2, 0, 2, 2)
        gridtab_MemberLoads.addWidget(self.frame26, 2, 0, 2, 2)
        gridtab_MemberLoads.addWidget(self.frame27, 2, 0, 2, 2)
        gridtab_MemberLoads.addWidget(self.frame28, 2, 0, 2, 2)
        gridtab_MemberLoads.setColumnStretch(0,3)
        gridtab_MemberLoads.setColumnStretch(1,2)
#        gridtab_MemberLoads.setRowStretch(0,1)
#        gridtab_MemberLoads.setRowStretch(1,1)
#        gridtab_MemberLoads.setRowStretch(2,2)
        vertical_loadaMember = QtWidgets.QVBoxLayout(self.frame21)
        vertical_load_types = QtWidgets.QVBoxLayout(self.frame22)
        vertical_memberLoads = QtWidgets.QVBoxLayout(self.frame23)
        vertical_loadGroups_2 = QtWidgets.QVBoxLayout(self.frame24)
        
        label_LoadselectType = QtWidgets.QLabel("Select a load type:",self.frame22)
        self.combo_loadTypes = QtWidgets.QComboBox(self.frame22)
        self.combo_loadTypes.setMaximumSize(QtCore.QSize(140,20))  
        vertical_load_types.addWidget(label_LoadselectType)
        vertical_load_types.addWidget(self.combo_loadTypes)
        
        label_LoadselectMember = QtWidgets.QLabel("Select a member:",self.frame21)
        self.combo_loadMembers = QtWidgets.QComboBox(self.frame21)
        self.combo_loadMembers.setMaximumSize(QtCore.QSize(70,20))  
        vertical_loadaMember.addWidget(label_LoadselectMember)
        vertical_loadaMember.addWidget(self.combo_loadMembers)
        self.radio_force_2 = QtWidgets.QRadioButton('Force', self.frame23)
        self.radio_moment_2 = QtWidgets.QRadioButton('Moment', self.frame23)
        vertical_memberLoads.addWidget(self.radio_force_2)
        vertical_memberLoads.addWidget(self.radio_moment_2)
        label_LoadGroup_2 = QtWidgets.QLabel("Load Group:",self.frame24)
        self.combo_loadGroups_2 = QtWidgets.QComboBox(self.frame24)
        self.combo_loadGroups_2.setMaximumSize(QtCore.QSize(70,20)) 
        
        vertical_loadGroups_2.addWidget(label_LoadGroup_2)
        vertical_loadGroups_2.addWidget(self.combo_loadGroups_2)
        for item in [self.combo_loadTypes, self.combo_loadMembers, self.combo_loadGroups_2]:
            item.setStyleSheet(combostyle)

#------>point load
        gridframe25 = QtWidgets.QGridLayout(self.frame25)
        label_Loadvectorcomponents_2 = QtWidgets.QLabel("Enter load vector components:",self.frame25)
        label_loadX_2 = QtWidgets.QLabel("X :",self.frame25)
        label_loadY_2 = QtWidgets.QLabel("Y :",self.frame25)
        label_loadZ_2 = QtWidgets.QLabel("Z :",self.frame25)
        label_a_2 = QtWidgets.QLabel("a =",self.frame25)
        self.dist_a_2 = QtWidgets.QLineEdit('0', self.frame25)
        self.dist_a_2.setToolTip('Distance from start of member')
        self.load_x_2 = QtWidgets.QLineEdit(self.frame25)
        self.load_x_2.setPlaceholderText("KN")
        self.load_y_2 = QtWidgets.QLineEdit(self.frame25)
        self.load_y_2.setPlaceholderText("KN")
        self.load_z_2 = QtWidgets.QLineEdit(self.frame25)
        self.load_z_2.setPlaceholderText("KN")
        self.btnAddPointLoad = QtWidgets.QPushButton("Add Load", self.frame25)
        gridframe25.addWidget(label_a_2,0,0,1,1)
        gridframe25.addWidget(self.dist_a_2,0,1,1,1)
        gridframe25.addWidget(label_Loadvectorcomponents_2,1,0,1,8)
        gridframe25.addWidget(label_loadX_2,2,0,1,1)
        gridframe25.addWidget(self.load_x_2,2,1,1,1)
        gridframe25.addWidget(label_loadY_2,2,2,1,1)
        gridframe25.addWidget(self.load_y_2,2,3,1,1)
        gridframe25.addWidget(label_loadZ_2,2,4,1,1)
        gridframe25.addWidget(self.load_z_2,2,5,1,1)
        gridframe25.addWidget(self.btnAddPointLoad,2,7,1,1)
        
        for item in [self.dist_a_2, self.load_x_2, self.load_y_2, self.load_z_2]:
            item.setStyleSheet(lineeditstyle)
            item.setMinimumSize(QtCore.QSize(width_unit*3, 0))
            item.setValidator(onlyFloat)
        self.dist_a_2.setValidator(onlyPosFloat)

#------>uniform load

        gridframe26 = QtWidgets.QGridLayout(self.frame26)
        label_partialload_3 = QtWidgets.QLabel("Partial load:",self.frame26)
        label_a_3 = QtWidgets.QLabel("a =",self.frame26)
        label_b_3 = QtWidgets.QLabel("b =",self.frame26)
        label_Loadvectorcomponents_3 = QtWidgets.QLabel("Enter load vector components:",self.frame26)
        label_loadX_3 = QtWidgets.QLabel("X :",self.frame26)
        label_loadY_3 = QtWidgets.QLabel("Y :",self.frame26)
        label_loadZ_3 = QtWidgets.QLabel("Z :",self.frame26)
        self.dist_a_3 = QtWidgets.QLineEdit('0',self.frame26)
        self.dist_a_3.setToolTip('Distance from start of member to start of load')
        self.dist_b_3 = QtWidgets.QLineEdit('0',self.frame26)
        self.dist_b_3.setToolTip('Distance from end of load to end of member')
        self.load_x_3 = QtWidgets.QLineEdit(self.frame26)
        self.load_x_3.setPlaceholderText("KN")
        self.load_y_3 = QtWidgets.QLineEdit(self.frame26)
        self.load_y_3.setPlaceholderText("KN")
        self.load_z_3 = QtWidgets.QLineEdit(self.frame26)
        self.load_z_3.setPlaceholderText("KN")
        self.btnAddUniformLoad = QtWidgets.QPushButton("Add Load", self.frame26)
        gridframe26.addWidget(label_partialload_3,0,0,1,8)
        gridframe26.addWidget(label_a_3,1,0,1,1)
        gridframe26.addWidget(self.dist_a_3,1,1,1,1)
        gridframe26.addWidget(label_b_3,1,2,1,1)
        gridframe26.addWidget(self.dist_b_3,1,3,1,1)
        gridframe26.addWidget(self.btnAddUniformLoad,1,7,1,1)
        gridframe26.addWidget(label_Loadvectorcomponents_3,2,0,1,8)
        gridframe26.addWidget(label_loadX_3,3,0,1,1)
        gridframe26.addWidget(self.load_x_3,3,1,1,1)
        gridframe26.addWidget(label_loadY_3,3,2,1,1)
        gridframe26.addWidget(self.load_y_3,3,3,1,1)
        gridframe26.addWidget(label_loadZ_3,3,6,1,1)
        gridframe26.addWidget(self.load_z_3,3,7,1,1)
        for item in [self.dist_a_3, self.dist_b_3, self.load_x_3, self.load_y_3, self.load_z_3]:
            item.setStyleSheet(lineeditstyle)
            item.setMinimumSize(QtCore.QSize(width_unit*3, 0))
            item.setValidator(onlyFloat)
        for item in [self.dist_a_3, self.dist_b_3]:
            item.setValidator(onlyPosFloat)
        
#------>triangular load

        gridframe27 = QtWidgets.QGridLayout(self.frame27)
        label_partialload_4 = QtWidgets.QLabel("Partial load:",self.frame27)
        label_a_4 = QtWidgets.QLabel("a =",self.frame27)
        label_b_4 = QtWidgets.QLabel("b =",self.frame27)
        
        label_Loadvectorcomponents_4 = QtWidgets.QLabel("Enter load vector components:",self.frame27)
        label_loadX_4_1 = QtWidgets.QLabel("X :",self.frame27)
        label_loadY_4_1 = QtWidgets.QLabel("Y :",self.frame27)
        label_loadZ_4_1 = QtWidgets.QLabel("Z :",self.frame27)
        self.dist_a_4 = QtWidgets.QLineEdit('0',self.frame27)
        self.dist_a_4.setToolTip('Distance from start of member to start of load')
        self.dist_b_4 = QtWidgets.QLineEdit('0',self.frame27)
        self.dist_b_4.setToolTip('Distance from end of load to end of member')
        self.btnAddTriangularLoad = QtWidgets.QPushButton("Add Load", self.frame27)
        self.load_x_4_1 = QtWidgets.QLineEdit(self.frame27)
        self.load_x_4_1.setPlaceholderText("KN")
        self.load_y_4_1 = QtWidgets.QLineEdit(self.frame27)
        self.load_y_4_1.setPlaceholderText("KN")
        self.load_z_4_1 = QtWidgets.QLineEdit(self.frame27)
        self.load_z_4_1.setPlaceholderText("KN")
        
        label_loadX_4_2 = QtWidgets.QLabel("X :",self.frame27)
        label_loadY_4_2 = QtWidgets.QLabel("Y :",self.frame27)
        label_loadZ_4_2 = QtWidgets.QLabel("Z :",self.frame27)
        self.load_x_4_2 = QtWidgets.QLineEdit(self.frame27)
        self.load_x_4_2.setPlaceholderText("KN")
        self.load_y_4_2 = QtWidgets.QLineEdit(self.frame27)
        self.load_y_4_2.setPlaceholderText("KN")
        self.load_z_4_2 = QtWidgets.QLineEdit(self.frame27)
        self.load_z_4_2.setPlaceholderText("KN")
        gridframe27.addWidget(label_partialload_4,0,0,1,6)
        gridframe27.addWidget(label_a_4,1,0,1,1)
        gridframe27.addWidget(self.dist_a_4,1,1,1,1)
        gridframe27.addWidget(label_b_4,1,2,1,1)
        gridframe27.addWidget(self.dist_b_4,1,3,1,1)
        gridframe27.addWidget(self.btnAddTriangularLoad,1,5,1,2)
        gridframe27.addWidget(label_Loadvectorcomponents_4,2,0,1,6)
        gridframe27.addWidget(label_loadX_4_1,3,0,1,1)
        gridframe27.addWidget(label_loadY_4_1,3,2,1,1)
        gridframe27.addWidget(label_loadZ_4_1,3,4,1,1)
        gridframe27.addWidget(self.load_x_4_1,3,1,1,1)
        gridframe27.addWidget(self.load_y_4_1,3,3,1,1)
        gridframe27.addWidget(self.load_z_4_1,3,5,1,1)
        gridframe27.addWidget(label_loadX_4_2,4,0,1,1)
        gridframe27.addWidget(label_loadY_4_2,4,2,1,1)
        gridframe27.addWidget(label_loadZ_4_2,4,4,1,1)
        gridframe27.addWidget(self.load_x_4_2,4,1,1,1)
        gridframe27.addWidget(self.load_y_4_2,4,3,1,1)
        gridframe27.addWidget(self.load_z_4_2,4,5,1,1)
        for item in [self.dist_a_4, self.dist_b_4,self.load_x_4_1, self.load_y_4_1, self.load_z_4_1, self.load_x_4_2, self.load_y_4_2, self.load_z_4_2]:
            item.setStyleSheet(lineeditstyle)
            item.setMinimumSize(QtCore.QSize(width_unit*3, 0))
            item.setValidator(onlyFloat)
        for item in [self.dist_a_4, self.dist_b_4]:
            item.setValidator(onlyPosFloat)

#------>trapezoidal load
        gridframe28 = QtWidgets.QGridLayout(self.frame28)
        label_partialload_5 = QtWidgets.QLabel("Partial load:",self.frame28)
        label_a_5 = QtWidgets.QLabel("a =",self.frame28)
        label_b_5 = QtWidgets.QLabel("b =",self.frame28)
        
        label_Loadvectorcomponents_5 = QtWidgets.QLabel("Enter load vector components:",self.frame28)
        label_loadX_5_1 = QtWidgets.QLabel("X :",self.frame28)
        label_loadY_5_1 = QtWidgets.QLabel("Y :",self.frame28)
        label_loadZ_5_1 = QtWidgets.QLabel("Z :",self.frame28)
        self.dist_a_5 = QtWidgets.QLineEdit('0',self.frame28)
        self.dist_a_5.setToolTip('Distance from start of member to start of load')
        self.dist_b_5 = QtWidgets.QLineEdit('0',self.frame28)
        self.dist_b_5.setToolTip('Distance from end of load to end of member')
        self.btnAddTrapezoidalLoad = QtWidgets.QPushButton("Add Load", self.frame28)
        self.load_x_5_1 = QtWidgets.QLineEdit(self.frame28)
        self.load_x_5_1.setPlaceholderText("KN")
        self.load_y_5_1 = QtWidgets.QLineEdit(self.frame28)
        self.load_y_5_1.setPlaceholderText("KN")
        self.load_z_5_1 = QtWidgets.QLineEdit(self.frame28)
        self.load_z_5_1.setPlaceholderText("KN")
        
        label_loadX_5_2 = QtWidgets.QLabel("X :",self.frame28)
        label_loadY_5_2 = QtWidgets.QLabel("Y :",self.frame28)
        label_loadZ_5_2 = QtWidgets.QLabel("Z :",self.frame28)
        self.load_x_5_2 = QtWidgets.QLineEdit(self.frame28)
        self.load_x_5_2.setPlaceholderText("KN")
        self.load_y_5_2 = QtWidgets.QLineEdit(self.frame28)
        self.load_y_5_2.setPlaceholderText("KN")
        self.load_z_5_2 = QtWidgets.QLineEdit(self.frame28)
        self.load_z_5_2.setPlaceholderText("KN")
        gridframe28.addWidget(label_partialload_5,0,0,1,6)
        gridframe28.addWidget(label_a_5,1,0,1,1)
        gridframe28.addWidget(self.dist_a_5,1,1,1,1)
        gridframe28.addWidget(label_b_5,1,2,1,1)
        gridframe28.addWidget(self.dist_b_5,1,3,1,1)
        gridframe28.addWidget(self.btnAddTrapezoidalLoad,1,5,1,2)
        gridframe28.addWidget(label_Loadvectorcomponents_5,2,0,1,6)
        gridframe28.addWidget(label_loadX_5_1,3,0,1,1)
        gridframe28.addWidget(label_loadY_5_1,3,2,1,1)
        gridframe28.addWidget(label_loadZ_5_1,3,4,1,1)
        gridframe28.addWidget(self.load_x_5_1,3,1,1,1)
        gridframe28.addWidget(self.load_y_5_1,3,3,1,1)
        gridframe28.addWidget(self.load_z_5_1,3,5,1,1)
        gridframe28.addWidget(label_loadX_5_2,4,0,1,1)
        gridframe28.addWidget(label_loadY_5_2,4,2,1,1)
        gridframe28.addWidget(label_loadZ_5_2,4,4,1,1)
        gridframe28.addWidget(self.load_x_5_2,4,1,1,1)
        gridframe28.addWidget(self.load_y_5_2,4,3,1,1)
        gridframe28.addWidget(self.load_z_5_2,4,5,1,1)
        for item in [self.dist_a_5, self.dist_b_5,self.load_x_5_1, self.load_y_5_1, self.load_z_5_1, self.load_x_5_2, self.load_y_5_2, self.load_z_5_2]:
            item.setStyleSheet(lineeditstyle)
            item.setMinimumSize(QtCore.QSize(width_unit*3, 0))
            item.setValidator(onlyFloat)
        for item in [self.dist_a_5, self.dist_b_5]:
            item.setValidator(onlyPosFloat)#FONTS
#TREES
        self.grouptree.setFont(font3)
        for tree in [self.memberstree, self.memberGrouptree]:
            tree.setFont(font3)
        self.supportstree.setFont(font3)
        self.dispstree.setFont(font3)
        self.relstree.setFont(font3)
        self.rigstree.setFont(font3)
#COMBOS
        self.comboSections.setFont(font3)
        self.comboSupNodes.setFont(font3)
        self.comboDispNodes.setFont(font3)            
        self.comboRelMembers.setFont(font3)
        self.comboRigMembers.setFont(font3)
        for item in [self.combo_loadTypes, self.combo_loadMembers, self.combo_loadGroups_2]:
            item.setFont(font3)
        for item in [self.combo_loadNodes, self.combo_loadGroups]:
            item.setFont(font3)
#LARGELABELS font1
        self.label_Groups.setFont(font1)
        self.label_Sections.setFont(font1)
        for label in [label_Elements, label_Position, label_Loads, label_Groups]:
            label.setFont(font1)
        for label in [label_Supports, label_Node, label_Degrees]:
            label.setFont(font1)
        for label in [label_Disps, label_Node_disp, label_Elem_rig, label_Rigs, label_Node_rel, label_Rels]:
            label.setFont(font1)
#MEDIUMLABELS font2
        label_LoadGroup.setFont(font2)
        label_LoadselectNode.setFont(font2)
        label_Start.setFont(font2)
        label_Nodes.setFont(font2)
        label_End.setFont(font2)
        label_Coordinates.setFont(font2)
        label_theta.setFont(font2)
        label_LoadselectMember.setFont(font2)
        label_LoadGroup_2.setFont(font2)  
        for item in [label_Loadvectorcomponents_2]:
            item.setFont(font2) 
        for item in [label_partialload_3]:
            item.setFont(font2)          
        for item in [label_partialload_4, label_Loadvectorcomponents_4]:
            item.setFont(font2)   
        for item in [label_partialload_5]:
            item.setFont(font2)             
        for item in [label_Loadvectorcomponents]:
            item.setFont(font2)  
        for item in [label_startnode, label_stopnode]:
            item.setFont(font2) 
        for item in [label_rig_start, label_rig_end]:
            item.setFont(font2)
#SMALLLABELS font3
        for item in [self.label_E1, self.label_v1, self.label_G1, self.label_E, self.label_G, self.label_A, self.label_J, self.label_Iy, self.label_Iz, self.label_W, self.label_v]:
            item.setFont(font3)   
        for item in [label_disp_x, label_disp_y, label_disp_z, label_disp_rotx, label_disp_roty, label_disp_rotz]:
            item.setFont(font3)
        for item in [label_rel_x, label_rel_y, label_rel_z, label_rel_rotx, label_rel_roty, label_rel_rotz, label_rel_x2, label_rel_y2, label_rel_z2, label_rel_rotx2, label_rel_roty2, label_rel_rotz2]:
            item.setFont(font3)
        for item in [label_rig_dxs, label_rig_dys, label_rig_dzs, label_rig_dxe, label_rig_dye,label_rig_dze]:
            item.setFont(font3)
        for item in [label_loadX, label_loadY, label_loadZ]:
            item.setFont(font3)
        for item in [label_loadX_2, label_loadY_2, label_loadZ_2]:
            item.setFont(font3)
        for item in [label_a_5, label_b_5,  label_loadX_5_1, label_loadY_5_1, label_loadZ_5_1,label_loadX_5_2, label_loadY_5_2, label_loadZ_5_2]:
            item.setFont(font3)
        for item in [label_a_4, label_b_4, label_loadX_4_1, label_loadY_4_1, label_loadZ_4_1,label_loadX_4_2, label_loadY_4_2, label_loadZ_4_2]:
            item.setFont(font3)
        for item in [label_a_3, label_b_3, label_loadX_3, label_loadY_3, label_loadZ_3]:
            item.setFont(font3)
        for item in [label_axis_x, label_axis_y, label_axis_z]:
            item.setFont(font3)
        for item in [label_stiff_x, label_stiff_y, label_stiff_z, label_stiff_rotx, label_stiff_roty, label_stiff_rotz]:
            item.setFont(font3)
#tinyLABELS font4
        for item in [label_displacements, label_releases, label_stiffnesses, label_rotation_angles]:
            item.setFont(font4)
#LINES
        for item in [self.lineE1, self.linev1, self.lineG1, self.lineE, self.lineG, self.lineA, self.lineJ, self.lineIy, self.lineIz, self.lineW, self.linev]:
            item.setFont(font4)    
        self.lineTheta.setFont(font4)
        for item in [self.disp_x, self.disp_y, self.disp_z, self.disp_rotx, self.disp_roty, self.disp_rotz]:
            item.setFont(font4)            
        for item in [self.rel_x, self.rel_y, self.rel_z, self.rel_rotx, self.rel_roty, self.rel_rotz,self.rel_x2, self.rel_y2, self.rel_z2, self.rel_rotx2, self.rel_roty2, self.rel_rotz2]:
            item.setFont(font4)
        for item in [self.lineStart, self.lineEnd, self.comboStart, self.comboEnd,self.lineTheta]:
            item.setFont(font4)
        for item in [self.rig_dxs, self.rig_dys, self.rig_dzs, self.rig_dxe, self.rig_dye, self.rig_dze]:
            item.setFont(font4)
        for item in [self.load_x, self.load_y, self.load_z]:
            item.setFont(font4)
        for item in [self.dist_a_2, self.load_x_2, self.load_y_2, self.load_z_2]:
            item.setFont(font4)
        for item in [self.dist_a_3, self.dist_b_3, self.load_x_3, self.load_y_3, self.load_z_3]:
            item.setFont(font4)
        for item in [self.dist_a_4, self.dist_b_4, self.load_x_4_1, self.load_y_4_1, self.load_z_4_1, self.load_x_4_2, self.load_y_4_2, self.load_z_4_2]:
            item.setFont(font4)        
        for item in [self.dist_a_5, self.dist_b_5, self.load_x_5_1, self.load_y_5_1, self.load_z_5_1, self.load_x_5_2, self.load_y_5_2, self.load_z_5_2]:
            item.setFont(font4)
        for item in [self.stiff_x, self.stiff_y, self.stiff_z, self.stiff_rotx, self.stiff_roty, self.stiff_rotz]:
            item.setFont(font4)
        for item in [self.rot_x, self.rot_y, self.rot_z]:
            item.setFont(font4)
#BUTTONS
        for item in [self.btnNewMember, self.btnSaveChangMember, self.btnDeleteMember]:
            item.setFont(font3)     
        for item in [self.btnNewGroup, self.btnSaveChangGroup, self.btnDeleteGroup]:
            item.setFont(font3)
        for item in [self.btnNewSupport, self.btnSaveChangSupport, self.btnDeleteSupport]:
            item.setFont(font3)
        for item in [self.btnNewDisplacement, self.btnSaveChangDisp, self.btnDeleteDisp]:
            item.setFont(font3)
        for item in [self.btnNewRelease, self.btnSaveChangRel, self.btnDeleteRel]:
            item.setFont(font3)   
        for item in [self.btnNewRig, self.btnSaveChangRig, self.btnDeleteRig]:
            item.setFont(font3)
#VARIOUS
        self.listWidget.setFont(font4)
        for sectionway in [self.firstSection, self.secondSection]:
            sectionway.setFont(font2)
        for sectiontype in self.sectiontypes:
            sectiontype.setFont(font3)
        self.loadList.setFont(font3)
#------>various layouts
        self.verticalRight.addWidget(self.tab_top)
        self.verticalRight.addWidget(self.bottomframe)
        self.verticalRight.setStretch(0, 5)
        self.verticalRight.setStretch(1, 5) 
        self.gridLayout.addWidget(self.frameright, 0, 2, 3, 1)
#------>statusbar
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setStyleSheet(statusbarstyle)
        self.setStatusBar(self.statusbar)
#------>main actions
#        self.center() #otan ayto syndyazetai me to "gridframe20.addWidget(label_Loadanglecomponents,2,0,1,8)" gia kapoio logo den kentrarei to parathyro 
        self.actionExit.triggered.connect(self.close)
        self.mainTree.customContextMenuRequested.connect(self.openMainMenu)
        self.mainTree.itemClicked.connect(self.mainTreeClicked)
        self.actionNew.triggered.connect(self.createNewProject)
        new_file.triggered.connect(self.createNewProject)
        self.actionOpen.triggered.connect(self.openFileNameDialog)
        open_file.triggered.connect(self.openFileNameDialog)
        self.actionSave.triggered.connect(self.saveAsIs)
#        self.actionIncludeSelfLoads.triggered.connect(lambda:(self.manageSelfLoads(True)))
#        self.actionDontIncludeSelfLoads.triggered.connect(lambda:(self.manageSelfLoads(False)))   
        self.save_file.triggered.connect(self.saveAsIs)
        self.actionSaveAs.triggered.connect(self.saveFileDialog)
        self.analysis.triggered.connect(self.analysisWin)
        self.viewresults.triggered.connect(self.viewresultsWin)
#------>viewer actions
        self.btndefault.clicked.connect(lambda:(self.drawStructure()))
        self.btnxyview.clicked.connect(lambda:(self.drawStructure(view='XY')))
        self.btnxzview.clicked.connect(lambda:(self.drawStructure(view='XZ')))
        self.btnyzview.clicked.connect(lambda:(self.drawStructure(view='YZ')))

#------>actions for section tab
        self.grouptree.itemClicked.connect(self.groupClicked)
        self.grouptree.customContextMenuRequested.connect(self.openGroupMenu)
        for sectionway in [self.firstSection, self.secondSection]:
            sectionway.clicked.connect(lambda:(self.loadSectionWays()))
        self.firstSection.clicked.connect(lambda:(self.clearHalfSectionTab(self.firstSection)))
        self.secondSection.clicked.connect(lambda:(self.clearHalfSectionTab(self.secondSection)))
        for sectiontype in self.sectiontypes:
            sectiontype.clicked.connect(lambda:(self.loadSectionSizes()))
        self.IPE = pd.read_csv('IPE.csv', sep=",")
        self.IPN = pd.read_csv('IPN.csv', sep=",")
        self.HE = pd.read_csv('HE.csv', sep=",")
        self.HL = pd.read_csv('HL.csv', sep=",")
        self.HD = pd.read_csv('HD.csv', sep=",")
        self.HP = pd.read_csv('HP.csv', sep=",")
        self.UPE = pd.read_csv('UPE.csv', sep=",")
        self.UPN = pd.read_csv('UPN.csv', sep=",")
        self.U = pd.read_csv('U.csv', sep=",")
        self.btnNewGroup.clicked.connect(self.getGroupvalue)
        self.btnSaveChangGroup.clicked.connect(self.saveGroupChanges)
        self.btnDeleteGroup.clicked.connect(self.deleteGroup)
        self.btnNewGroup.setEnabled(True)
        self.btnSaveChangGroup.setEnabled(False)
        self.btnDeleteGroup.setEnabled(False)
#------>members actions
        self.memberstree.itemClicked.connect(self.elementClicked)
        self.memberstree.customContextMenuRequested.connect(self.openMemberMenu)
        self.memberGrouptree.itemClicked.connect(self.membergroupClicked)
        self.memberGrouptree.customContextMenuRequested.connect(self.openMemberGroupMenu)
        nodelist = [' '] + list(model.Beam.Nodes.keys())
        self.comboStart.addItems(nodelist)
        self.comboEnd.addItems(nodelist)
        self.lineStart.textEdited.connect(lambda:(self.comboStart.setCurrentIndex(0)))
        self.lineEnd.textEdited.connect(lambda:(self.comboEnd.setCurrentIndex(0)))
        for line in [self.lineStart, self.lineEnd]:
            line.textEdited.connect(lambda:(self.btnNewMember.setEnabled(True)))
            line.textEdited.connect(lambda:(self.btnNewMember.setAutoDefault(True)))
        self.comboStart.currentTextChanged.connect(lambda:(self.lineStart.clear()))
        self.comboEnd.currentTextChanged.connect(lambda:(self.lineEnd.clear()))
        for btn in [self.comboStart, self.comboEnd]:
            btn.currentTextChanged.connect(lambda:(self.btnNewMember.setEnabled(True)))
        self.btnNewMember.clicked.connect(lambda:(self.addElement()))
        self.btnSaveChangMember.clicked.connect(lambda:(self.saveMemberChanges()))
        self.btnDeleteMember.clicked.connect(lambda:(self.delElement()))
        self.btnNewMember.setEnabled(False)
        self.btnSaveChangMember.setEnabled(False)
        self.btnDeleteMember.setEnabled(False)
#------>supports actions
        self.supportstree.itemClicked.connect(self.supportClicked)
#        self.supportstree.customContextMenuRequested.connect(self.openSupportsMenu)
        self.btnNewSupport.clicked.connect(self.getSupportValue)
        self.btnSaveChangSupport.clicked.connect(self.saveSupportChanges)
        self.btnDeleteSupport.clicked.connect(lambda:(self.deleteSupport()))
        self.btnNewSupport.setEnabled(True)
        self.btnSaveChangSupport.setEnabled(False)
        self.btnDeleteSupport.setEnabled(False)
#------>displacements actions
        self.dispstree.itemClicked.connect(self.displacementClicked)
#        self.dispstree.customContextMenuRequested.connect(self.openDispMenu)
        self.btnNewDisplacement.clicked.connect(self.getDispValues)
        self.btnSaveChangDisp.clicked.connect(self.saveDispValues)
        self.btnDeleteDisp.clicked.connect(lambda:(self.deleteDisplacement()))
        self.btnNewDisplacement.setEnabled(True)
        self.btnSaveChangDisp.setEnabled(False)
        self.btnDeleteDisp.setEnabled(False)
#------>releases actions
        self.relstree.itemClicked.connect(self.releaseClicked)
#        self.dispstree.customContextMenuRequested.connect(self.openDispMenu)
        self.btnNewRelease.clicked.connect(self.getRelValues)
        self.btnSaveChangRel.clicked.connect(self.saveRelValues)
        self.btnDeleteRel.clicked.connect(lambda:(self.deleteRelease()))
        self.btnNewRelease.setEnabled(True)
        self.btnSaveChangRel.setEnabled(False)
        self.btnDeleteRel.setEnabled(False)
#------>rigid nodes actions
        self.rigstree.itemClicked.connect(self.rigidClicked)
#        self.dispstree.customContextMenuRequested.connect(self.openDispMenu)
        self.btnNewRig.clicked.connect(self.getRigValues)
        self.btnSaveChangRig.clicked.connect(self.saveRigValues)
        self.btnDeleteRig.clicked.connect(lambda:(self.deleteRig()))
        self.btnNewRig.setEnabled(True)
        self.btnSaveChangRig.setEnabled(False)
        self.btnDeleteRig.setEnabled(False)  
        
#----->bottom tab actions
        self.combo_loadTypes.addItem('')
        self.combo_loadTypes.addItem(QtGui.QIcon("pointload.png"), "Point Load")
        self.combo_loadTypes.addItem(QtGui.QIcon("uniformload.png"), "Uniform Load")
        self.combo_loadTypes.addItem(QtGui.QIcon("triangularload.png"), "Triangular Load")
        self.combo_loadTypes.addItem(QtGui.QIcon("trapezoidalload.png"), "Trapezoidal Load")
        self.combo_loadTypes.currentTextChanged.connect(self.on_combobox_changed)
        self.btnAddNodalLoad.clicked.connect(self.addNodalLoad)
        self.btnAddPointLoad.clicked.connect(self.addPointLoad)
        self.btnAddUniformLoad.clicked.connect(self.addUniformLoad)
        self.btnAddTriangularLoad.clicked.connect(self.addTriangularLoad)
        self.btnAddTrapezoidalLoad.clicked.connect(self.addTrapezoidalLoad)
        
        nodal_ll = frozenset({self.load_x, self.load_y, self.load_z})
        point_ll = frozenset({self.load_x_2, self.load_y_2, self.load_z_2})
        unif_ll = frozenset({self.load_x_3, self.load_y_3, self.load_z_3})
        triang_ll = frozenset({self.load_x_4_1, self.load_y_4_1, self.load_z_4_1,self.load_x_4_2, self.load_y_4_2, self.load_z_4_2})
        trap_ll = frozenset({self.load_x_5_1, self.load_y_5_1, self.load_z_5_1,self.load_x_5_2, self.load_y_5_2, self.load_z_5_2})
        all_lines = set({nodal_ll, point_ll, unif_ll, triang_ll, trap_ll})
        
        for lineset in all_lines:
            new_all_lines = all_lines-{lineset}
            for line in lineset:
                for clearset in new_all_lines:
                    for clearline in clearset:
                        line.textEdited.connect(clearline.clear)
        self.deactivateUI()
        self.installEventFilter(self) #eventFilter

    def drawStructure(self, view='default'):
        self.resetView()
        if view=='default':
            self.viewer.drawStructure()
        if view=='XY':
            self.viewer.drawStructure(view)
        if view=='XZ':
            self.viewer.drawStructure(view)
        if view=='YZ':
            self.viewer.drawStructure(view)


    def analysisWin(self):
        self.analysisWindow = AnalysisWindow(self.projectname)
        self.analysisWindow.show()

    def viewresultsWin(self):
        self.resultsWindow = ViewResultsWindow(self.projectname)
        self.resultsWindow.show()



    def mainTreeClicked(self,item,column):
        self.listWidget.clear()
        text = item.text(0)
        if item.parent():
            if item.parent().text(0)=='Nodes':#it is a node
                for i,c in enumerate(text):
                    if c==':':
                        node=text[:i]
                        break
                coords = str(model.Beam.Nodes[node])
                support = str(model.Beam.NodalSupports[node])
                item1 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item1)
                item1.setText("Coordinates: {}".format(coords))
                if node in model.Beam.Displacements.keys():
                    disps = str(model.Beam.Displacements[node])
                    item4 = QtWidgets.QListWidgetItem()
                    self.listWidget.addItem(item4)
                    item4.setText("Displacements: {}".format(str(disps)))
                item2 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item2)
                item2.setText("Loads:")
                thereareloads = False
                for i,rep in enumerate(list(model.Beam.Loads['node'])):
                    if rep==node:
                        loads = model.Beam.Loads.loc[(model.Beam.Loads.node==node), 'loadsstart']
                        item3 = QtWidgets.QListWidgetItem()
                        self.listWidget.addItem(item3)
                        item3.setText("      {}".format(str(loads[i]))) #ayto thelei kati giati etsi den tha mou vgalei ola ta epikomvia tou idiou komvou
                        thereareloads = True
                if thereareloads==False:
                    item3 = QtWidgets.QListWidgetItem()
                    self.listWidget.addItem(item3)
                    item3.setText("      None")
            if item.parent().text(0)=='Supports':
                for i,c in enumerate(text):
                    if c==',':
                        node=text[:i]
                        break
                support = str(model.Beam.NodalSupports[node])
                item1 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item1)
                item1.setText("Node: {}".format(node))
                item2 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item2)
                item2.setText("     {}".format(support)) 
                if node in model.Beam.ElasticNode.keys():
                    stiff = str(model.Beam.ElasticNode[node])
                    item3 = QtWidgets.QListWidgetItem()
                    self.listWidget.addItem(item3)
                    item3.setText("Stiffness values: {}".format(str(stiff)))
                if node in model.Beam.Displacements.keys():
                    disps = str(model.Beam.Displacements[node])
                    item4 = QtWidgets.QListWidgetItem()
                    self.listWidget.addItem(item4)
                    item4.setText("Displacements: {}".format(str(disps)))        
            if item.parent().text(0)=='Members':
                for i,c in enumerate(text):
                    if c==',':
                        member=text[:i]
                        break
                startnode = model.Beam.Beams[member].start_node
                stopnode = model.Beam.Beams[member].stop_node
                group = model.Beam.Beams[member].group
                theta = model.Beam.Beams[member].theta
                release = model.Beam.Beams[member].release
                item1 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item1)
                item1.setText("Start node: {}".format(startnode)) 
                item2 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item2)
                item2.setText("Stop node: {}".format(stopnode)) 
                item3 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item3)
                item3.setText("Group: {}".format(group)) 
                item4 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item4)
                item4.setText("Local x axis angle: {}".format(str(theta))) 
                item5 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item5)
                reltxt = str(release) if release!=None else 'None'
                item5.setText("Releases: {}".format(reltxt)) 
            if item.parent().text(0)=='Section Groups':
                group = text
                groupvalues = model.Beam.Groups[text]
                specvals = [groupvalues[0][i] for i in range(len(groupvalues[0]))]
                crosstype = groupvalues[1]
                specdict = dict(zip(['E','A','v','G','J','Iy','Iz','w'],specvals))
                item1 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item1)
                item1.setText("Name: {}".format(group))
                for key, value in specdict.items():
                    item2 = QtWidgets.QListWidgetItem()
                    self.listWidget.addItem(item2)
                    item2.setText("{}: {}".format(key,value))
                item3 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item3)
                item3.setText('Type: {}'.format(crosstype))
            if item.parent().text(0)=='Displacements':
                for i,c in enumerate(text):
                    if c==',':
                        node=text[:i]
                        break
                disps = model.Beam.Displacements[node]
                item1 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item1)
                item1.setText("Node: {}".format(node))
                item2 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item2)
                item2.setText("     {}".format(disps))
                
                
            if item.parent().text(0)=='Releases':
                for i,c in enumerate(text):
                    if c==',':
                        el=text[:i]
                        break
                rels = model.Beam.Beams[el].release
                stext = 'Starting node' if rels[0][0]==1 else ''
                etext = 'Ending node' if rels[0][1]==1 else ''
                item1 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item1)
                item1.setText("Release at: {} {}".format(stext,etext))
                item2 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item2)
                item2.setText("Freedoms released: {}".format(rels[1]))
                item3 = QtWidgets.QListWidgetItem()
                self.listWidget.addItem(item3)
                item3.setText("Angles of releases: {}".format(rels[2]))
            
            if item.parent().text(0)=='Rigid Nodes':
                for i,c in enumerate(text):
                    if c==',':
                        el=text[:i]
                        break
                rigs = model.Beam.RigidNode[el]
                if any(r!=0 for r in rigs[0]):
                    item1 = QtWidgets.QListWidgetItem()
                    self.listWidget.addItem(item1)
                    item1.setText("Rigid node at starting node\nwith values: {}".format(rigs[0]))
                if any(r!=0 for r in rigs[0]):
                    item2 = QtWidgets.QListWidgetItem()
                    self.listWidget.addItem(item2)
                    item2.setText("Rigid node at ending node\nwith values: {}".format(rigs[1]))
#


    def groupClicked(self,item):
        if item.text(0)=='New':
            self.clearSectionTab()
        else:
            name = item.text(0)
            group = model.Beam.Groups[name]
            self.showGroupSpecs(group)
            self.btnNewGroup.setEnabled(False)
            self.btnSaveChangGroup.setEnabled(True)
            self.btnDeleteGroup.setEnabled(True)


    def showGroupSpecs(self,group):
        secDict = {'IPE':self.rbIPE, 'HE':self.rbHE, 'IPN':self.rbIPN, 'HL':self.rbHL, 'HD':self.rbHD, 'HP':self.rbHP, 'UPE':self.rbUPE, 'UPN':self.rbUPN, 'U':self.rbU}
        self.sectionSize.setExclusive(False)
        for rb in secDict.values():
            rb.setChecked(False)
        sec = group[1].split(' ')
        if sec[0] in secDict.keys():
            secDict[sec[0]].setChecked(True)
            self.firstSection.setChecked(True)
        else:
            self.secondSection.setChecked(True)
        self.sectionSize.setExclusive(True)        
        self.lineA.setText(str(group[0][1]))
        self.lineE1.setText(str(group[0][0]))
        self.lineE.setText(str(group[0][0]))
        self.lineG.setText(str(group[0][3]))
        self.lineJ.setText(str(group[0][4]))
        self.lineIy.setText(str(group[0][5]))
        self.lineIz.setText(str(group[0][6]))
        self.linev.setText(str(group[0][2]))
        self.lineW.setText(str(group[0][7]))
        self.linev1.setText(str(group[0][2]))
        self.lineG1.setText(str(group[0][3]))
            
            
    def elementClicked(self,item):
        self.loadList.clear()
        if item.text(0)=='New':
            self.clearMemberTab()
        else:
            name = item.text(0)
            if name[:2]=='el':
                beam = model.Beam.Beams[name]
                self.comboStart.setCurrentText(beam.start_node)
                self.comboEnd.setCurrentText(beam.stop_node)
                self.lineStart.setText(str(beam.start))
                self.lineEnd.setText(str(beam.stop))
                if self.lineTheta!=0:
                    self.lineTheta.setText(str(beam.theta))
                loads = model.Beam.Loads[model.Beam.Loads.self_load=='NO'].reset_index(drop=True)
                func = {'FE':'even', 'PE':'even', 'FT':'triangular', 'PT':'triangular', 'FR':'trapezoidal', 'PR':'trapezoidal', 'Po':'point', 'M':'moment'}
                if name in list(loads.member):
                    memberslist = loads.loc[(loads.member==name), ['function', 'group']]
                    memberslist = memberslist.reset_index(drop=True)
                    text=[]
                    for i in range(len(memberslist)):
                        t = '{} load ({}) {}'.format(func[loads.function[i]],loads.group[i], loads.vector[i])
                        text.append(t)
                        self.loadList.addItems(text)
                self.btnNewMember.setEnabled(False)
                self.btnSaveChangMember.setEnabled(True)
                self.btnDeleteMember.setEnabled(True)

            
    def membergroupClicked(self, item):
#        self.elementList.clear()
        group = item.text(0)
        text=[]
        beams = model.Beam.Beams
        for name, beam in beams.items():
            if group == beam.group:
                text.append(name)
#        self.elementList.addItems(text)
        self.btnNewMember.setEnabled(True)
        self.btnSaveChangMember.setEnabled(True)
        self.btnDeleteMember.setEnabled(False)


    def supportClicked(self,item):
        self.clearSupportTab()
        name = item.text(0)
        if name=='New':
            self.comboSupNodes.setEnabled(True)
            self.btnNewSupport.setEnabled(True)
            self.btnSaveChangSupport.setEnabled(False)
            self.btnDeleteSupport.setEnabled(False)
            self.clearSupportTab()
        else:
            self.btnNewSupport.setEnabled(False)
            self.btnSaveChangSupport.setEnabled(True)
            self.btnDeleteSupport.setEnabled(True)
            self.comboSupNodes.setEnabled(False)
            self.comboSupNodes.setCurrentText(name)
            sups = [self.sup_x, self.sup_y, self.sup_z, self.sup_rotx, self.sup_roty, self.sup_rotz]
            for i, sup in enumerate(model.Beam.NodalSupports[name]):
                if sup==1 or sup==2:
                    sups[i].setChecked(True)
            angles = [self.rot_x, self.rot_y,self.rot_z]   
            if name in model.Beam.RotatedSupports.keys():
                for i, angle in enumerate(model.Beam.RotatedSupports[name]):
                    angles[i].setText(str(angle))
            stiffs = [self.stiff_x, self.stiff_y, self.stiff_z, self.stiff_rotx, self.stiff_roty, self.stiff_rotz]            
            if name in model.Beam.ElasticNode.keys():
                for i, stiff in enumerate(model.Beam.ElasticNode[name]):
                    if model.Beam.NodalSupports[name][i]==2:
                        stiffs[i].setText(str(stiff))


    def displacementClicked(self,item):
        name = item.text(0)
        if name=='New':
            self.comboDispNodes.setEnabled(True)
            self.btnNewDisplacement.setEnabled(True)
            self.btnSaveChangDisp.setEnabled(False)
            self.btnDeleteDisp.setEnabled(False)
            self.clearDispTab()
        else:
            self.btnNewDisplacement.setEnabled(False)
            self.btnSaveChangDisp.setEnabled(True)
            self.btnDeleteDisp.setEnabled(True)
            self.comboDispNodes.setEnabled(False)
            self.comboDispNodes.setCurrentText(name)
            disps = [self.disp_x, self.disp_y, self.disp_z, self.disp_rotx, self.disp_roty, self.disp_rotz]
            if name in model.Beam.Displacements.keys():
                for i, disp in enumerate(model.Beam.Displacements[name]):
                    disps[i].setText(str(disp))


    def releaseClicked(self,item):
        name = item.text(0)
        if name=='New':
            self.comboRelMembers.setEnabled(True)
            self.btnNewRelease.setEnabled(True)
            self.btnSaveChangRel.setEnabled(False)
            self.btnDeleteRel.setEnabled(False)
            self.clearRelTab()
        else:
            for i,c in enumerate(name):
                if c==',':
                    name=name[:i]
                    break
            self.btnNewRelease.setEnabled(False)
            self.btnSaveChangRel.setEnabled(True)
            self.btnDeleteRel.setEnabled(True)
            self.comboRelMembers.setEnabled(False)
            self.comboRelMembers.setCurrentText(name)
            rels = [self.rel_x, self.rel_y, self.rel_z, self.rel_rotx, self.rel_roty, self.rel_rotz,self.rel_x2, self.rel_y2, self.rel_z2, self.rel_rotx2, self.rel_roty2, self.rel_rotz2]
            releases = model.Beam.Beams[name].release[1]
            releasevals = model.Beam.Beams[name].release[2]
            for i, rel in enumerate(rels):
                if releases[i] == 1:
                    rel.setText(str(releasevals[i]))
                else:
                    rel.setText('')


    def rigidClicked(self, item):
        name = item.text(0)
        if name=='New':
            self.comboRigMembers.setEnabled(True)
            self.btnNewRig.setEnabled(True)
            self.btnSaveChangRig.setEnabled(False)
            self.btnDeleteRig.setEnabled(False)
            self.clearRigTab()
        else:
            self.btnNewRig.setEnabled(False)
            self.btnSaveChangRig.setEnabled(True)
            self.btnDeleteRig.setEnabled(True)
            self.comboRigMembers.setEnabled(False)
            self.comboRigMembers.setCurrentText(name)
            rigs = [self.rig_dxs, self.rig_dys, self.rig_dzs, self.rig_dxe, self.rig_dye, self.rig_dze]
            rigidstart = model.Beam.RigidNode[name][0]
            rigidstop = model.Beam.RigidNode[name][1]
            allrigs =rigidstart + rigidstop
            for i, rig in enumerate(rigs):
                rig.setText(str(allrigs[i]))



    def openMainMenu(self, position):
        item = self.mainTree.itemAt(position)
        if item==None or item.parent()==None:
            return
        name = item.text(0)
        menu = QtWidgets.QMenu()
        if name == 'Nodes':
            addnode = QtWidgets.QAction("Add Node",self)
            menu.addAction(addnode)
        if item.parent().text(0) == 'Nodes':
            for i,c in enumerate(name):
                if c==':':
                    node=name[:i]
                    break
            deletenode = QtWidgets.QAction("Delete Node",self)
            menu.addAction(deletenode)
            deletenode.triggered.connect(lambda:(self.deleteNode(node)))
        if name == 'Supports':
            addsupport = QtWidgets.QAction("Add support",self)
            menu.addAction(addsupport)
            addsupport.triggered.connect(lambda:(self.tab_top.setCurrentIndex(2)))
        if item.parent().text(0) == 'Supports':
            for i,c in enumerate(name):
                if c==',':
                    node=name[:i]
                    break
            deletesupport = QtWidgets.QAction("Delete support",self)
            menu.addAction(deletesupport)
            deletesupport.triggered.connect(lambda:(self.deleteSupport(node)))
        if name == 'Members':
            addmember = QtWidgets.QAction("Add member",self)
            menu.addAction(addmember)
            addmember.triggered.connect(lambda:(self.tab_top.setCurrentIndex(1)))
        if item.parent().text(0) == 'Members':
            for i,c in enumerate(name):
                if c==',':
                    el=name[:i]
                    break
            deletemember = QtWidgets.QAction("Delete member",self)
            menu.addAction(deletemember)
            deletemember.triggered.connect(lambda:(self.delElement(el)))
        if name == 'Section Groups':
            editsections = QtWidgets.QAction("Edit sections",self)
            menu.addAction(editsections)
            editsections.triggered.connect(lambda:(self.tab_top.setCurrentIndex(0)))
        
        
        if name == 'Displacements':
            adddisplace = QtWidgets.QAction("Add displacement",self)
            menu.addAction(adddisplace)
            adddisplace.triggered.connect(lambda:(self.tab_top.setCurrentIndex(3)))
        if item.parent().text(0) == 'Displacements':
            for i,c in enumerate(name):
                if c==',':
                    node=name[:i]
                    break
            deletedisp = QtWidgets.QAction("Delete displacement",self)
            menu.addAction(deletedisp)
            deletedisp.triggered.connect(lambda:(self.deleteDisplacement(node)))
        
        if name == 'Releases':
            addrelease = QtWidgets.QAction("Add release",self)
            menu.addAction(addrelease)
            addrelease.triggered.connect(lambda:(self.tab_top.setCurrentIndex(4)))
        if item.parent().text(0) == 'Releases':
            for i,c in enumerate(name):
                if c==',':
                    el=name[:i]
                    break
            deleterel = QtWidgets.QAction("Delete release",self)
            menu.addAction(deleterel)
            deleterel.triggered.connect(lambda:(self.deleteRelease(el)))
        
        if name == 'Rigid Nodes':
            addrigid = QtWidgets.QAction("Add support",self)
            menu.addAction(addrigid)
            addrigid.triggered.connect(lambda:(self.tab_top.setCurrentIndex(5)))
        if item.parent().text(0) == 'Rigid Nodes':
            for i,c in enumerate(name):
                if c==',':
                    el=name[:i]
                    break
            deleterig = QtWidgets.QAction("Delete rigid node",self)
            menu.addAction(deleterig)
            deleterig.triggered.connect(lambda:(self.deleteRig(el)))

        
        if item.parent().text(0) == 'Nodal Loads':
            for i,c in enumerate(name):
                if c==',':
                    node=name[:i]
                    j=i
                    break
            vector = name[j+2:]
            deleteload = QtWidgets.QAction("Delete",self)
            menu.addAction(deleteload)
            deleteload.triggered.connect(lambda:(self.deleteNodalLoad(node, vector)))
            
        if item.parent().text(0) == 'Beam Loads':
            for i,c in enumerate(name):
                if c==',':
                    el=name[:i]
                    j=i
                    break
            func = {'Nodal load':'Nodal load','evenly distributed':'FE','triangular':'FT', 'trapezoidal':'FR', 'point':'Po', 'moment':'M'}
            function = func[name[j+1:]]
            vector = item.child(0)
            deleteload = QtWidgets.QAction("Delete",self)
            menu.addAction(deleteload)
            deleteload.triggered.connect(lambda:(self.deleteMemberLoad(el, function, vector)))    
        menu.exec_(self.mainTree.viewport().mapToGlobal(position))



    def openMemberMenu(self, position):
        item = self.memberstree.itemAt(position)
        if item:
            name = item.text(0)
            if name=='New':
                return
            menu = QtWidgets.QMenu()
            deletemember = QtWidgets.QAction("Delete member",self)
            menu.addAction(deletemember)
            modify = QtWidgets.QAction("Change group",self)
            menu.addAction(modify)
            deletemember.triggered.connect(lambda:(self.delElement(name)))
            menu.exec_(self.memberstree.viewport().mapToGlobal(position))  
        else:
            return

    def openGroupMenu(self, position):#<-----dokimastika gia right click menu
        if self.grouptree.itemAt(position):
            item = self.grouptree.itemAt(position)
            name = item.text(0)
            if name=='New':
                return
            selected_groups = self.grouptree.selectedItems()
            menu = QtWidgets.QMenu()
            deletegroup = QtWidgets.QAction("Delete",self)
            menu.addAction(deletegroup)
            deletegroup.triggered.connect(lambda:(self.deleteGroup(selected_groups)))
            menu.exec_(self.grouptree.viewport().mapToGlobal(position))
        else:
            return
        
    def openMemberGroupMenu(self, position):#<-----dokimastika gia right click menu
        if self.memberGrouptree.itemAt(position):
            item = self.memberGrouptree.itemAt(position)
            name = item.text(0)
            if name=='New':
                return
            selected_groups = self.memberGrouptree.selectedItems()
            menu = QtWidgets.QMenu()
            deletegroup = QtWidgets.QAction("Delete",self)
            menu.addAction(deletegroup)
            deletegroup.triggered.connect(lambda:(self.deleteGroup(selected_groups)))
            menu.exec_(self.memberGrouptree.viewport().mapToGlobal(position))
        else:
            return


    def openDispMenu(self):
        pass

    def openSupportsMenu(self):
        pass
#----------   END OF DEMO FUNCTIONS  -------------------------------------


#-----------  START OF MEMBERS FUNCTIONS  -----------------------------------
    def addElement(self, name=None):
        '''Check the validity of inserted data in element window, add the new
        member and update all widgets and data structures'''
        global ADDSELFLOADS
        textstart,textstop = self.createStartStop()
        numstart = self.lineStart.text()
        numstop = self.lineEnd.text()
        theta = float(self.lineTheta.text()) if self.lineTheta.text()!='' else 0
        group = self.memberGrouptree.currentItem().text(0) if self.memberGrouptree.currentItem()!=None else 'Default'
        textcoords=[]
        numstartcoords=[]
        numstopcoords=[]
        try:
            if textstart==' ':
                rawlist=[]
                for i,c in enumerate(numstart):
                    if c!=',':
                        rawlist.append(c)
                    else:
                        textcoords.append(''.join(rawlist))
                        rawlist=[]
                textcoords.append(''.join(rawlist))
                rawlist=[]
                for i in textcoords:
                    coord = float(i)
                    numstartcoords.append(coord)
                start = numstartcoords
            else:
                start=textstart
            textcoords=[]
            if textstop==' ':
                rawlist=[]
                for i,c in enumerate(numstop):
                    if c!=',':
                        rawlist.append(c)
                    else:
                        textcoords.append(''.join(rawlist))
                        rawlist=[]
                textcoords.append(''.join(rawlist))
                rawlist=[]
                for i in textcoords:
                    coord = float(i)
                    numstopcoords.append(coord)
                stop = numstopcoords
            else:
                stop=textstop
            if name==None:
                name = model.beamNextName()            
            if not self.startStopIsSame(name, start, stop):
                for key,value in model.Beam.Beams.items():
                    if self.thereIsSameBeam(value, start, stop)==True:
                        self.singleEvent('Warning', 'There is already a member       \n with these coordinates               ')
                        return                        
                if len(model.Beam.Groups.keys())>=1:
                    model.addElement(name,start,stop,theta=theta,group=group)
                else:
                    self.singleEvent('Warning', 'Please create a group before adding any member.')
                    return
            else:
                self.singleEvent('Warning', 'Start and End nodes cannot be the same')
                return
        except (RuntimeError, TypeError, NameError, ZeroDivisionError, ValueError):
            self.singleEvent('Warning', 'Please check the validity of the inserted coordinates')
            return
        beam = model.Beam.Beams[name]
        if ADDSELFLOADS==True:
            self.addSelfLoad(name,beam)
        self.generateMembersTree()
        self.generateProjectTree()
        self.fillTabWidgets()
        self.resetView()
        self.addUpdateViewer(name,beam)


    def createStartStop(self):
        self.textstart = self.comboStart.currentText()
        self.textstop = self.comboEnd.currentText()
        return self.textstart, self.textstop


    def startStopIsSame(self,name, start, stop):
        if type(start)==str:
            if type(stop)==str:
                if start==stop:
                    return True
            else:
                if list(model.Beam.Nodes[start])==stop:
                    return True
        else:
            if type(stop)==str:
                if start==list(model.Beam.Nodes[stop]):
                    return True
            else:
                if start==stop:
                    return True
        return False


    def thereIsSameBeam(self,value, start, stop):
        if (((value.start_node==start or list(value.start)==start) and (value.stop_node==stop or list(value.stop)==stop)) or 
            ((value.start_node==stop or list(value.start)==stop) and (value.stop_node==start or list(value.stop)==start))):
            return True 


    def saveMemberChanges(self):
        selected_beams = self.memberstree.selectedItems()
        for item in selected_beams:
            el = item.text(0)
            beam = model.Beam.Beams[el]
            theta = float(self.lineTheta.text()) if self.lineTheta.text()!='' else 0
            group = self.memberGrouptree.currentItem().text(0) if self.memberGrouptree.currentItem()!=None else beam.group
            beam.groupVals(group)
            beam.initValues(theta)
        self.generateMembersTree()
        self.generateProjectTree()


    def delElement(self, *name):
        if not name:
            selected_beams = self.memberstree.selectedItems()
            for item in selected_beams:
                name = item.text(0)
                beam = model.Beam.Beams[name]
                model.deleteBeam(name)
                self.delSelfLoad(name,beam)
                self.viewer.deleteBeam(name)
            self.clearMemberTab()
            self.generateAllTrees()
        else:
            name = name[0]
            beam = model.Beam.Beams[name]
            model.deleteBeam(name)
            self.delSelfLoad(name,beam)
            self.viewer.deleteBeam(name)
            self.clearMemberTab()
            self.generateAllTrees()

    def deleteNode(self, node):
        model.deleteNode(node)
        self.resetView()
        self.addUpdateViewer()
        self.generateAllTrees()


#----------   END OF MEMBERS FUNCTIONS  ---------------------------------------

#---------   START OF SECTION FUNCTIONS  --------------------------------------

    def loadSectionSizes(self):
        if self.rbIPE.isChecked():
            self.comboSections.clear()
            self.comboSections.addItems(self.IPE['Section name'])#EDW NA MPEI ALLO ARXEIO
        if self.rbHE.isChecked():
            self.comboSections.clear()
            self.comboSections.addItems(self.HE['Section name'])
        if self.rbIPN.isChecked():
            self.comboSections.clear()
            self.comboSections.addItems(self.IPN['Section name'])
        if self.rbHL.isChecked():
            self.comboSections.clear()
            self.comboSections.addItems(self.HL['Section name'])
        if self.rbHD.isChecked():
            self.comboSections.clear()
            self.comboSections.addItems(self.HD['Section name'])
        if self.rbHP.isChecked():
            self.comboSections.clear()
            self.comboSections.addItems(self.HP['Section name'])
        if self.rbUPE.isChecked():
            self.comboSections.clear()
            self.comboSections.addItems(self.UPE['Section name'])
        if self.rbUPN.isChecked():
            self.comboSections.clear()
            self.comboSections.addItems(self.UPN['Section name'])
        if self.rbU.isChecked():
            self.comboSections.clear()
            self.comboSections.addItems(self.U['Section name'])


    def createGroup(self):
        if self.firstSection.isChecked():
            section = self.comboSections.currentText()
            E1 = self.lineE1.text()
            v1 = self.linev1.text() if self.linev1.text()!='' else '0'
            G1 = self.lineG1.text() if self.lineG1.text()!='' else '0'
            if G1=='0' and v1=='0':
                self.singleEvent('Warning', 'Please insert either G or v.')
                return
            return section, E1, v1, G1
        elif self.secondSection.isChecked():
            A = self.lineA.text()
            E = self.lineE.text()
            G = self.lineG.text() if self.lineG.text()!='' else '0'
            J = self.lineJ.text()
            Iy = self.lineIy.text()
            Iz = self.lineIz.text()
            v = self.linev.text() if self.linev.text()!='' else '0'
            w = self.lineW.text() if self.linev.text()!='' else '0'
            if G=='0' and v=='0':
                self.singleEvent('Warning', 'Please insert either G or v.')
                return
            return E,A,v,G,J,Iy,Iz,w
        else:
            self.singleEvent('Warning', 'Please choose the way you\'d like to insert a section .')
            return


    def getGroupvalue(self):
        data = self.checkGroupvalue()
        if data != None:
            groupname, specs, sectiontype = data
        else:
            return
        model.Beam.Groups[groupname]=[specs,sectiontype]
        self.clearSectionTab()
        self.generateSectionsTree()
        self.generateProjectTree()


    def changeGroupValue(self, group):
        data = self.checkGroupvalue(gn=group)
        if data != None:
            groupname, specs, sectiontype = data
        else:
            return
        model.Beam.Groups[groupname]=[specs,sectiontype]


    def groupEdited(self):
        item = self.grouptree.currentItem()
        if item==None:
            return
        group = item.text(0)
        if group=='New':
            self.btnDeleteGroup.setEnabled(False)
            self.btnNewGroup.setEnabled(True)
            self.btnSaveChangGroup.setEnabled(False)
        else:
            self.btnDeleteGroup.setEnabled(True)
            self.btnNewGroup.setEnabled(False)
            self.btnSaveChangGroup.setEnabled(True)


    def checkGroupvalue(self, gn=None):
        specs = self.createGroup()
        if len(specs)==4:
            if specs[0]=='' or specs[1]=='':
                self.singleEvent('', 'Please insert all values correctly.')
                return
#            elif (specs[2]=='' and specs[3]=='') or (specs[2]!='' and specs[3]!=''):
#                self.singleEvent('', 'Please insert either G or v.')
#                return
            else:
                if gn==None:
                    text, ok = QtWidgets.QInputDialog.getText(self, 'New Group', 'Enter a name for the new group of elements')
                    if ok and text:
                        for buttonname in self.sectiontypes:
                            if buttonname.isChecked():
                                t=buttonname.text()
                        groupname = text
                        if groupname in model.Beam.Groups.keys():
                            self.singleEvent('', 'This name already exists')
                            return
                        sectiontype = specs[0]
                        values = self.deriveSectionValues(t,sectiontype,specs[1],specs[3],specs[2])
                    elif not ok:
                        return
                    else:
                        self.singleEvent('', 'Please enter a valid group name')
                        return
                else:
                    groupname = gn
                    for buttonname in self.sectiontypes:
                            if buttonname.isChecked():
                                t=buttonname.text()
                    sectiontype = specs[0]
                    values = self.deriveSectionValues(t,sectiontype,specs[1],specs[3],specs[2])
        elif len(specs)==8:
            if specs[0]=='' or specs[1]=='' or specs[4]=='' or specs[5]=='' or specs[6]=='' or specs[7]=='':
                self.singleEvent('Warning', 'Please insert all values correctly.')
                return
            else:
                if gn==None:
                    text, ok = QtWidgets.QInputDialog.getText(self, 'New Group', 'Enter a name for the new group of elements')
                    if ok and text:
                        groupname = text
                        if groupname in model.Beam.Groups.keys():
                            self.singleEvent('', 'This name already exists')
                            return
#                        values = specs
                        values = []
                        for text in specs:
                            values.append(float(text))
                        sectiontype = 'Custom'
                    elif not ok:
                        return
                    else:
                        self.singleEvent('', 'Please enter a valid group name')
                        return
                else:
                    groupname = gn
                    values=[]
                    for text in specs:
                        values.append(float(text))
                    sectiontype = 'Custom'
        return groupname, list(values), sectiontype #here the specs have to be calculated for all the above and then return


    def deriveSectionValues(self,t,sectiontype,E,G,v):
        file = '{}.csv'.format(t)
        data = pd.read_csv(file, sep=",")
        data = data.set_index('Section name')
        A = float(data.at[sectiontype,'A'])
        J = float(data.at[sectiontype,'lt'])
        Iy = float(data.at[sectiontype,'ly'])
        Iz = float(data.at[sectiontype,'lz'])
        g=9.8066500286389
        w = g*float(data.at[sectiontype,'G'])
        E = float(E)
        v = float(v) if v!='' else 0
        G = float(G) if G!='' else E/(2+2*v)
        return E,A,v,G,J,Iy,Iz,w


    def deleteGroup(self, selected_groups):
        reply = self.dChoiceEvent('','Are you sure you want to delete the selected groups?')
        if reply==QtWidgets.QMessageBox.Ok:
            if not selected_groups:
                selected_groups = self.grouptree.selectedItems()
                for groupname in selected_groups:
                    if groupname.text(0)=='Default':
                        self.singleEvent('', 'Default group cannot be deleted')
                    else:
                        del model.Beam.Groups[groupname.text(0)]
                        for beam in model.Beam.Beams.keys():
                            if model.Beam.Beams[beam].group==groupname.text(0):
                                model.Beam.Beams[beam].group='Default'
                self.clearSectionTab()
                self.generateSectionsTree()
                self.generateProjectTree()
            else:
                for groupname in selected_groups:
                    if groupname.text(0)=='Default':
                        self.singleEvent('', 'Default group cannot be deleted')
                    else:
                        del model.Beam.Groups[groupname.text(0)]
                        for beam in model.Beam.Beams.keys():
                            if model.Beam.Beams[beam].group==groupname.text(0):
                                model.Beam.Beams[beam].group='Default'
                self.clearSectionTab()
                self.generateSectionsTree()
                self.generateProjectTree()


    def saveGroupChanges(self):
        reply = self.dChoiceEvent('','Are you sure you want to save changes for selected groups?')
        if reply==QtWidgets.QMessageBox.Ok:
            selected_groups = self.grouptree.selectedItems()
            for groupname in selected_groups:
                self.changeGroupValue(groupname.text(0))
        else:
            return
        
#--------   END OF SECTION FUNCTIONS  -----------------------------------------

#--------   START OF SUPPORT FUNCTIONS  ---------------------------------------

    def getSupportValue(self):
        if self.checkSupportValues() != None:
            node, sups, rots, stiffs = self.checkSupportValues()
            if any(r!=0 for r in rots):
                model.Beam.RotatedSupports[node] = rots
            if any(s!=0 for s in stiffs):
                model.Beam.ElasticNode[node] = stiffs
                for i,stiff in enumerate(stiffs):
                    if stiff!=0:
                        sups[i]=2
            model.Beam.NodalSupports[node] = sups        
            self.generateProjectTree()
            self.generateSupportsTree()
            self.addUpdateViewer()
            self.clearSupportTab()


    def saveSupportChanges(self):
        reply = self.dChoiceEvent('','Are you sure you want to save changes for selected support?')
        if reply==QtWidgets.QMessageBox.Ok:
            self.getSupportValue()
        else:
            return


    def checkSupportValues(self):
        node, sups, rots, stiffs, checkstiffs = self.getInitSupportValues()
        if node==' ':
            self.singleEvent('', 'No node has been chosen')
            return
        if all(sup==0 for sup in sups):
            self.singleEvent('', 'There has to be checked at least one degree of freedom.')
            return
        if checkstiffs!=[0,0,0,0,0,0]:
            for i, stiff in enumerate(checkstiffs):
                if stiff!=0 and sups[i]==0:
                    self.singleEvent('', 'Stiffness value is valid only for supported degrees.')
                    return
        normrots=[]
        for angle in rots:
            normrots.append(angle%(2*np.pi))
        return node, sups, rots, stiffs


    def getInitSupportValues(self):
        node = self.comboSupNodes.currentText()
        
        sups = []
        for rbutton in [self.sup_x, self.sup_y, self.sup_z, self.sup_rotx, self.sup_roty, self.sup_rotz]:
            if rbutton.isChecked():
                sups.append(1)
            else:
                sups.append(0)
        rots = []
        for angle in [self.rot_x, self.rot_y,self.rot_z]:
            a = angle.text()
            if a=='':
                rots.append(0)
            else:
                rots.append(float(a))
        stiffs = []
        checkstiffs = []
        for stiff in [self.stiff_x, self.stiff_y, self.stiff_z, self.stiff_rotx, self.stiff_roty, self.stiff_rotz]:
            t = stiff.text()
            if t == '':
                stiffs.append(0)
                checkstiffs.append(0)
            else:
                stiffs.append(float(t))
                checkstiffs.append(1)
        return node, sups, rots, stiffs, checkstiffs


    def deleteSupport(self, *args):
        reply = self.dChoiceEvent('','Are you sure you want to delete the selected supports?')
        if reply==QtWidgets.QMessageBox.Ok:
            if len(args)==1:
                node=args[0]
                model.Beam.NodalSupports[node] = [0,0,0,0,0,0]
                if node in model.Beam.RotatedSupports.keys():
                    del model.Beam.RotatedSupports[node]
                if node in model.Beam.Displacements.keys():    
                    del model.Beam.Displacements[node]
                if node in model.Beam.ElasticNode.keys():
                    del model.Beam.ElasticNode[node]
                self.generateProjectTree()
                self.generateDispTree()
                self.generateSupportsTree()
                self.clearSupportTab()
                self.addUpdateViewer()
            else:
                selected_sups = self.supportstree.selectedItems()
                for supportname in selected_sups:
                    node = supportname.text(0)
                    model.Beam.NodalSupports[node] = [0,0,0,0,0,0]
                    if node in model.Beam.RotatedSupports.keys():
                        del model.Beam.RotatedSupports[node]
                    if node in model.Beam.Displacements.keys():    
                        del model.Beam.Displacements[node]
                    if node in model.Beam.ElasticNode.keys():
                        del model.Beam.ElasticNode[node]
                    self.generateProjectTree()
                    self.generateDispTree()
                    self.generateSupportsTree()
                    self.clearSupportTab()
                    self.addUpdateViewer()
        else:
            return


#--------   END OF SUPPORT FUNCTIONS  -----------------------------------------
#--------   START OF DISPLACEMENT FUNCTIONS  ----------------------------------

    def getDispValues(self):
        node = self.comboDispNodes.currentText()
        disps = []
        for disp in [self.disp_x, self.disp_y, self.disp_z, self.disp_rotx, self.disp_roty, self.disp_rotz]:
            d = disp.text()
            if d=='':
                disps.append(0)
            else:
                disps.append(float(d))
        if any(d!=0 for d in disps):
            model.Beam.Displacements[node] = disps
            self.generateProjectTree()
            self.generateDispTree()
            self.clearDispTab()

    def saveDispValues(self):
        reply = self.dChoiceEvent('','Are you sure you want to save changes?')
        if reply==QtWidgets.QMessageBox.Ok:
            self.getDispValues()
        else:
            return


    def deleteDisplacement(self, *args):
        reply = self.dChoiceEvent('','Are you sure you want to delete the selected displacement?')
        if reply==QtWidgets.QMessageBox.Ok:
            if len(args)==1:
                del model.Beam.Displacements[args[0]]
                self.generateProjectTree()
                self.generateDispTree()
                self.clearDispTab()
            else:
                selected_disps = self.dispstree.selectedItems()
                for dispname in selected_disps:
                    node = dispname.text(0)
                    del model.Beam.Displacements[node]
                    self.generateProjectTree()
                    self.generateDispTree()
                    self.clearDispTab()
        else:
            return
   
#--------   END OF DISPLACEMENT FUNCTIONS  ------------------------------------
#--------   START OF RELEASES FUNCTIONS  ----------------------------------

    def getRelValues(self):
        member = self.comboRelMembers.currentText()
        beam = model.Beam.Beams[member]
        rels = []
        relvals = []
        if all(item.text()=='' for item in [self.rel_x, self.rel_y, self.rel_z, self.rel_rotx, self.rel_roty, self.rel_rotz,self.rel_x2, self.rel_y2, self.rel_z2, self.rel_rotx2, self.rel_roty2, self.rel_rotz2]):
            self.singleEvent('', 'Fill at least one line. If an angle is zero, fill with 0')
            return
        for rel in [self.rel_x, self.rel_y, self.rel_z, self.rel_rotx, self.rel_roty, self.rel_rotz,self.rel_x2, self.rel_y2, self.rel_z2, self.rel_rotx2, self.rel_roty2, self.rel_rotz2]:
            d = rel.text()
            if d=='':
                rels.append(0)
                relvals.append(0)
            else:
                rels.append(1)
                relvals.append(float(d))
        relnodes = [1,1]
        if all(item==0 for item in rels[:6]):
            relnodes[0]=0
        if all(item==0 for item in rels[6:]):
            relnodes[1]=0
        release = [relnodes, rels, relvals]
#        beam.releaseEdge(release)
        beam.release=release
        self.generateProjectTree()
        self.generateRelTree()
        self.addUpdateViewer()
        self.clearRelTab()


    def saveRelValues(self):
        reply = self.dChoiceEvent('','Are you sure you want to save changes?')
        if reply==QtWidgets.QMessageBox.Ok:
            self.getRelValues()
        else:
            return


    def deleteRelease(self, el=None):
        reply = self.dChoiceEvent('','Are you sure you want to delete the selected displacement?')
        if reply==QtWidgets.QMessageBox.Ok:
            if el!=None:
                beam = model.Beam.Beams[el]
                beam.release=None
                self.generateProjectTree()
                self.generateRelTree()
                self.addUpdateViewer()
                self.clearRelTab()
            else:
                selected_beams = self.relstree.selectedItems()
                selected_names=[]
                for el in selected_beams:
                    text = el.text(0)
                    for i,c in enumerate(text):
                        if c==',':
                            name=text[:i]
                            break
                    selected_names.append(name)
                for name in selected_names:
                    beam = model.Beam.Beams[name]
                    beam.release=None
                self.generateProjectTree()
                self.generateRelTree()
                self.addUpdateViewer()
                self.clearRelTab()
        else:
            return

#--------   END OF RELEASES FUNCTIONS  ----------------------------------------
#--------   START OF RIGID NODE FUNCTIONS  ------------------------------------

    def getRigValues(self):
        rigs = [self.rig_dxs, self.rig_dys, self.rig_dzs, self.rig_dxe, self.rig_dye, self.rig_dze]
        member = self.comboRigMembers.currentText()
        startrigs = []
        stoprigs = []
        if all(rig.text()=='' for rig in rigs):
            self.singleEvent('', 'Fill at least one line to save this node.')
            return
        for i in range(3):
            d = rigs[i].text()
            if d=='':
                startrigs.append(0)
            else:
                startrigs.append(float(d))
        for i in range(3,6):
            d = rigs[i].text()
            if d=='':
                stoprigs.append(0)
            else:
                stoprigs.append(float(d))
        model.Beam.RigidNode[member]=[startrigs, stoprigs]
        self.generateProjectTree()
        self.generateRigTree()
        self.clearRigTab()


    def saveRigValues(self):
        reply = self.dChoiceEvent('','Are you sure you want to save changes?')
        if reply==QtWidgets.QMessageBox.Ok:
            self.getRigValues()
            self.generateProjectTree()
            self.clearRigTab()
        else:
            return
  
        
    def deleteRig(self, el=None):
        reply = self.dChoiceEvent('','Are you sure you want to delete the selected item?')
        if reply==QtWidgets.QMessageBox.Ok:
            if el!=None:
                del model.Beam.RigidNode[el]
                self.generateProjectTree()
                self.generateRigTree()
                self.clearRigTab()
            else:
                selected_beams = self.rigstree.selectedItems()
                for el in selected_beams:
                    name = el.text(0)
                    del model.Beam.RigidNode[name]
                    self.generateProjectTree()
                    self.generateRigTree()
                    self.clearRigTab()
        else:
            return

#--------   END OF RIGID NODE FUNCTIONS  ----------------------------------------


#--------   START OF LOADS FUNCTIONS  -----------------------------------------

    def on_combobox_changed(self, value):
        allframes = [self.frame25, self.frame26, self.frame27, self.frame28]
        for frame in allframes:
            frame.hide()
        if value == '':
            return
        if value =="Point Load":
            self.radio_force_2.setEnabled(True)
            self.radio_moment_2.setEnabled(True)
            self.frame25.show()
        if value =="Uniform Load":
            self.radio_force_2.setEnabled(False)
            self.radio_moment_2.setEnabled(False)
            self.frame26.show()
        if value =="Triangular Load":
            self.radio_force_2.setEnabled(False)
            self.radio_moment_2.setEnabled(False)
            self.frame27.show()
        if value =="Trapezoidal Load":
            self.radio_force_2.setEnabled(False)
            self.radio_moment_2.setEnabled(False)
            self.frame28.show()


    def addNodalLoad(self):
        node = self.combo_loadNodes.currentText()
        if node=='':
            self.singleEvent('', 'Choose a node from the drop down menu')
            return
        loadgroup = self.combo_loadGroups.currentText()
        if loadgroup=='':
            self.singleEvent('', '      Choose a load group        ')
            return
        loadx = self.load_x.text()
        loady = self.load_y.text()
        loadz = self.load_z.text()
        if any(i!='' for i in [loadx, loady, loadz]):
            checkdict = {loadx:'x value load', loady:'y value load', loadz:'z value load'}
            for key, value in checkdict.items():
                if key=='':
                    self.singleEvent('', 'Fill in the {} box'.format(value))
                    return
            try:
                q=[float(loadx), float(loady), float(loadz)]
            except:
                self.singleEvent('', 'Fill the angle or value lines with valid values.')
                return
        if self.radio_force.isChecked():
            q = q + [0,0,0]
        elif self.radio_moment.isChecked():
            q =  [0,0,0] + q
        else:
            self.singleEvent('', 'Choose either the "Force" or "Moment" check box')
            return
        self.clearNodalLoadTab()
        model.nodalLoad(node, q, loadgroup = loadgroup)
        self.generateProjectTree()
        self.addUpdateViewer()


    def addPointLoad(self):
        el = self.combo_loadMembers.currentText()
        if el=='':
            self.singleEvent('', 'Choose an element from the drop down menu')
            return
        loadgroup = self.combo_loadGroups_2.currentText()
        if loadgroup=='':
            self.singleEvent('', '     Choose a load group       ')
            return
        try:
            a = float(self.dist_a_2.text())
        except:
            self.singleEvent('', 'Fill in the distance line')
            return
        loadx = self.load_x_2.text()
        loady = self.load_y_2.text()
        loadz = self.load_z_2.text()
        if any(i!='' for i in [loadx, loady, loadz]):
            checkdict = {loadx:'x value load', loady:'y value load', loadz:'z value load'}
            for key, value in checkdict.items():
                if key=='':
                    self.singleEvent('', 'Fill in the {} box'.format(value))
                    return
            try:
                q=[float(loadx), float(loady), float(loadz)]
            except:
                self.singleEvent('', 'Fill the lines with valid values.')
                return
        if self.radio_force_2.isChecked():
            function = 'Po'
        elif self.radio_moment_2.isChecked():
            function = 'M'
        else:
            self.singleEvent('', 'Choose either the "Force" or "Moment" check box')
            return
        length = model.Beam.Beams[el].L
        if a==0 or a==length:
            self.singleEvent('', 'A load at the edge of a beam is considered a nodal load.')
            return
        if a>length:
            self.singleEvent('', 'This load has been placed outside of the beam.')
            return
        self.clearMemberLoadTab()
        model.beamLoad(el, q, function, a=a, loadgroup = loadgroup)
        self.generateProjectTree()
        self.addUpdateViewer()


    def addUniformLoad(self):
        el = self.combo_loadMembers.currentText()
        if el=='':
            self.singleEvent('', 'Choose an element from the drop down menu')
            return
        loadgroup = self.combo_loadGroups_2.currentText()
        if loadgroup=='':
            self.singleEvent('', 'Choose a load group')
            return
        try:
            a = float(self.dist_a_3.text())
        except:
            a = 0
        try:
            b = float(self.dist_b_3.text())
        except:
            b = 0
        loadx = self.load_x_3.text()
        loady = self.load_y_3.text()
        loadz = self.load_z_3.text()
        if any(i!='' for i in [loadx, loady, loadz]):
            checkdict = {loadx:'x value load', loady:'y value load', loadz:'z value load'}
            for key, value in checkdict.items():
                if key=='':
                    self.singleEvent('', 'Fill in the {} box'.format(value))
                    return
            try:
                q=[float(loadx), float(loady), float(loadz)]
            except:
                self.singleEvent('', 'Fill the lines with valid values.')
                return        
        if a==0 and b==0:
            function='FE'
        else:
            function='PE'
        length = model.Beam.Beams[el].L
        if a>=length or b>=length:
            self.singleEvent('', 'Distance \'a\' and \'b\' cannot have the same or greater value \nthan the length of the beam')
            return
        if a>b:
            self.singleEvent('', 'Distance \'a\' cannot be greater than \'b\'')
            return
        if a+b==length:
            self.singleEvent('', 'Sum of \'a\' and \'b\' must not equal length of element.')
            return
        self.clearMemberLoadTab()
        model.beamLoad(el, q, function, a=a, b=b, loadgroup = loadgroup)
        self.generateProjectTree()
        self.addUpdateViewer()
    
    
    def addTriangularLoad(self):
        el = self.combo_loadMembers.currentText()
        if el=='':
            self.singleEvent('', 'Choose an element from the drop down menu')
            return
        loadgroup = self.combo_loadGroups_2.currentText()
        if loadgroup=='':
            self.singleEvent('', 'Choose a load group')
            return
        try:
            a = float(self.dist_a_4.text())
        except:
            a = 0
        try:
            b = float(self.dist_b_4.text())
        except:
            b = 0
        loadx_1 = self.load_x_4_1.text()
        loady_1 = self.load_y_4_1.text()
        loadz_1 = self.load_z_4_1.text()
        loadx_2 = self.load_x_4_2.text()
        loady_2 = self.load_y_4_2.text()
        loadz_2 = self.load_z_4_2.text()
        ascending = None
        if all(i=='' for i in [loadx_1, loady_1, loadz_1]) and any(i=='' for i in [loadx_2, loady_2, loadz_2]):
            checkdict = {loadx_2:'x value load', loady_2:'y value load', loadz_2:'z value load'}
            for key, value in checkdict.items():
                if key=='':
                    self.singleEvent('', 'Fill in the {} box'.format(value))
                    return
        elif all(i=='' for i in [loadx_2, loady_2, loadz_2]) and any(i=='' for i in [loadx_1, loady_1, loadz_1]):
            checkdict = {loadx_1:'x value load', loady_1:'y value load', loadz_1:'z value load'}
            for key, value in checkdict.items():
                if key=='':
                    self.singleEvent('', 'Fill in the {} box'.format(value))
                    return
        elif any(i!='' for i in [loadx_1, loady_1, loadz_1]) and any(i!='' for i in [loadx_2, loady_2, loadz_2]):
            self.singleEvent('', 'Fill only one line of values')
            return
        elif all(i!='' for i in [loadx_1, loady_1, loadz_1]):
            try:
                q=[float(loadx_1), float(loady_1), float(loadz_1)]
                ascending = False
            except:
                self.singleEvent('', 'Fill the lines with valid values.')
                return
        elif all(i!='' for i in [loadx_2, loady_2, loadz_2]):
            try:
                q=[float(loadx_2), float(loady_2), float(loadz_2)]
                ascending = True
            except:
                self.singleEvent('', 'Fill the lines with valid values.')
                return
        else:
            self.singleEvent('', 'Fill only one line of values'.format(value))
            return
        if ascending:
            q = (0, q)
        else:
            q = (q, 0)
        if a==0 and b==0:
            function='FT'
        else:
            function='PT'
        length = model.Beam.Beams[el].L
        if a>=length or b>=length:
            self.singleEvent('', 'Distance \'a\' and \'b\' cannot have the same or greater value \nthan the length of the beam')
            return
        if a>b:
            self.singleEvent('', 'Distance \'a\' cannot be greater than \'b\'')
            return
        if a+b==length:
            self.singleEvent('', 'Sum of \'a\' and \'b\' must not equal length of element.')
            return
        self.clearMemberLoadTab()
        model.beamLoad(el, q, function, a=a, b=b, loadgroup = loadgroup)
        self.generateProjectTree()
        self.addUpdateViewer()
    
    
    def addTrapezoidalLoad(self):
        el = self.combo_loadMembers.currentText()
        if el=='':
            self.singleEvent('', 'Choose an element from the drop down menu')
            return
        loadgroup = self.combo_loadGroups_2.currentText()
        if loadgroup=='':
            self.singleEvent('', 'Choose a load group')
            return
        try:
            a = float(self.dist_a_5.text())
        except:
            a = 0
        try:
            b = float(self.dist_b_5.text())
        except:
            b = 0
        loadx_1 = self.load_x_5_1.text()
        loady_1 = self.load_y_5_1.text()
        loadz_1 = self.load_z_5_1.text()
        loadx_2 = self.load_x_5_2.text()
        loady_2 = self.load_y_5_2.text()
        loadz_2 = self.load_z_5_2.text()
        if any(i=='' for i in [loadx_1, loady_1, loadz_1,loadx_2, loady_2, loadz_2]):
            checkdict = {loadx_1:'first x value load', loady_1:'first y value load', loadz_1:'first z value load',loadx_2:'second x value load', loady_2:'second y value load', loadz_2:'second z value load'}
            for key, value in checkdict.items():
                if key=='':
                    self.singleEvent('', 'Fill in the {} box'.format(value))
                    return
        else :
            try:
                q1=[float(loadx_1), float(loady_1), float(loadz_1)]
                q2=[float(loadx_2), float(loady_2), float(loadz_2)]
                q = [q1,q2]
            except:
                self.singleEvent('', 'Fill the lines with valid values.')
                return
            q1test = np.array([round(i,2) for i in q1])
            q2test = np.array([round(i,2) for i in q2])
            q1norm = q1test/np.linalg.norm(q1test)
            q2norm = q2test/np.linalg.norm(q2test)
            if any(q1norm[i]!=q2norm[i] for i in range(len(q1norm))):
                self.singleEvent('', 'The two vectors have not identical direction')
                return
        if a==0 and b==0:
            function = 'FR'
        else:
            function = 'PR'
        length = model.Beam.Beams[el].L
        if a>=length or b>=length:
            self.singleEvent('', 'Distance \'a\' and \'b\' cannot have the same or greater value \nthan the length of the beam')
            return
        if a>b:
            self.singleEvent('', 'Distance \'a\' cannot be greater than \'b\'')
            return
        if a+b==length:
            self.singleEvent('', 'Sum of \'a\' and \'b\' must not equal length of element.')
            return
        self.clearMemberLoadTab()
        model.beamLoad(el, q, function, a=a, b=b, loadgroup = loadgroup)
        self.generateProjectTree()
        self.addUpdateViewer()


    def addSelfLoad(self,name,beam):
        self_load = beam.selfload
        model.beamLoad(name, (0,0,self_load*(-1)), 'FE',selfload='YES')
        self.generateProjectTree()
        self.addUpdateViewer()


    def delSelfLoad(self,name,beam):
        try:
            loads = model.Beam.Loads[model.Beam.Loads.self_load!='YES'].reset_index(drop=True)
            selfloads = model.Beam.Loads[model.Beam.Loads.self_load=='YES'].reset_index(drop=True)
            selfloads = selfloads[selfloads.member!=name]
            model.Beam.Loads = pd.concat([loads,selfloads], axis=0, join='outer', ignore_index=True)
            self.generateProjectTree()
        except:
            pass

    def deleteNodalLoad(self,node,vector):
        allloads = model.Beam.Loads[model.Beam.Loads.node!=node].reset_index(drop=True)
        thisloads = model.Beam.Loads[model.Beam.Loads.node==node].reset_index(drop=True)
        if len(thisloads)==1:
            model.Beam.Loads=allloads
        else:
            thisloads = thisloads[thisloads.loadsstart!=vector]
            model.Beam.Loads = pd.concat([allloads,thisloads], axis=0, join='outer', ignore_index=True)
        self.addUpdateViewer()
        self.generateProjectTree()
                  
        
    def deleteMemberLoad(self,el, function, vector):
        allloads = model.Beam.Loads[model.Beam.Loads.member!=el].reset_index(drop=True)
        thisloads = model.Beam.Loads[model.Beam.Loads.member==el].reset_index(drop=True)
        if len(thisloads)==1:
            model.Beam.Loads=allloads
        else:
            thisloads = thisloads[(thisloads.vector!=vector) & (thisloads.function!=function)]
            model.Beam.Loads = pd.concat([allloads,thisloads], axis=0, join='outer', ignore_index=True)
        self.addUpdateViewer()
        self.generateProjectTree()        
        
        
    def clearNodalLoadTab(self):
        for item in [self.combo_loadNodes, self.combo_loadGroups]:
            item.setCurrentIndex(0)
        for item in [self.radio_force, self.radio_moment]:
            item.setChecked(False)
        for item in [self.load_x,self.load_y,self.load_z]:
            item.clear()
    
    def clearMemberLoadTab(self):
        for item in [self.dist_a_2, self.load_x_2, self.load_y_2, self.load_z_2, self.dist_a_3, self.dist_b_3, self.dist_a_4, self.dist_b_4, self.dist_a_5, self.dist_b_5]:
            item.clear()
        for item in [self.combo_loadMembers, self.combo_loadGroups_2, self.combo_loadTypes]:
            item.setCurrentIndex(0)
        for item in [self.radio_force_2, self.radio_moment_2]:
            item.setChecked(False)
       
#--------   END OF LOADS FUNCTIONS  -------------------------------------------
#--------   START OF UPDATING WINDOWS  ----------------------------------------

    def generateProjectTree(self):
        self.mainTree.clear()
        self.listWidget.clear()
        item_0 = QtWidgets.QTreeWidgetItem(self.mainTree)
        self.mainTree.topLevelItem(0).setText(0,"Nodes")
        for node,coords in model.Beam.Nodes.items():
            item_1 = QtWidgets.QTreeWidgetItem(item_0)
            item_1.setText(0,node + ': ' + str(coords))
        item_0 = QtWidgets.QTreeWidgetItem(self.mainTree)
        self.mainTree.topLevelItem(1).setText(0,"Supports")
        for node, support in model.Beam.NodalSupports.items():
            if any(s!=0 for s in support):
                item_1 = QtWidgets.QTreeWidgetItem(item_0)
                item_1.setText(0,'{}, {}'.format(node,str(support)))
        item_0 = QtWidgets.QTreeWidgetItem(self.mainTree)
        self.mainTree.topLevelItem(2).setText(0,"Members")
        for name, beam in model.Beam.Beams.items():
            item_1 = QtWidgets.QTreeWidgetItem(item_0)
            item_1.setText(0,'{}, ({}, {}, {})'.format(name,beam.start_node,beam.stop_node,beam.group))
        item_0 = QtWidgets.QTreeWidgetItem(self.mainTree)
        self.mainTree.topLevelItem(3).setText(0,"Section Groups")
        for group in model.Beam.Groups.keys():
            item_1 = QtWidgets.QTreeWidgetItem(item_0)
            item_1.setText(0,group)
        item_0 = QtWidgets.QTreeWidgetItem(self.mainTree)
        self.mainTree.topLevelItem(4).setText(0,"Displacements")
        for node, disp in model.Beam.Displacements.items():
            if any(d!=0 for d in disp):
                item_1 = QtWidgets.QTreeWidgetItem(item_0)
                item_1.setText(0,'{}, {}'.format(node,str(disp)))
        item_0 = QtWidgets.QTreeWidgetItem(self.mainTree)
        self.mainTree.topLevelItem(5).setText(0,"Releases")
        for name, beam in model.Beam.Beams.items():
            if beam.release!=None:
                release = beam.release
                edges = release[0]
                start = 'Start' if edges[0]==1 else ''
                stop = 'End' if edges[1]==1 else ''
                item_1 = QtWidgets.QTreeWidgetItem(item_0)
                item_1.setText(0,'{}, {}, {}'.format(name,start,stop))
        item_0 = QtWidgets.QTreeWidgetItem(self.mainTree)
        self.mainTree.topLevelItem(6).setText(0,"Rigid Nodes")
        for el, rig in model.Beam.RigidNode.items():
            item_1 = QtWidgets.QTreeWidgetItem(item_0)
            item_1.setText(0,'{}, {}'.format(el,str(rig)))
        item_0 = QtWidgets.QTreeWidgetItem(self.mainTree)
        self.mainTree.topLevelItem(7).setText(0,"Nodal Loads")
#        memberloads = model.Beam.Loads.loc[:,['member','function','self_load','vector']]
        func = {'Nodal load':'Nodal load','FE':'evenly distributed', 'PE':'evenly distributed', 'FT':'triangular', 'PT':'triangular', 'FR':'trapezoidal', 'PR':'trapezoidal', 'Po':'point', 'M':'moment'}
        nodes = model.Beam.Loads.node
        nodal_loads = model.Beam.Loads.loadsstart
        for i, item in enumerate(nodes):
            if item!='None' and type(item)!=float:
                item_1 = QtWidgets.QTreeWidgetItem(item_0)
                item_1.setText(0,'{}, {}'.format(item,nodal_loads[i]))
        item_0 = QtWidgets.QTreeWidgetItem(self.mainTree)
        self.mainTree.topLevelItem(8).setText(0,"Beam Loads")
        otherloads = model.Beam.Loads[model.Beam.Loads.self_load=='NO'].reset_index(drop=True)
        for i, member in enumerate(otherloads.member):
            item_1 = QtWidgets.QTreeWidgetItem(item_0)
            item_1.setText(0,'{},{}'.format(member,func[otherloads.loc[i,'function']]))
            item_2 = QtWidgets.QTreeWidgetItem(item_1)
            item_2.setText(0,str(otherloads.loc[i,'vector']))
#        for i, member in enumerate(memberloads.member):
#            if member!='None' and type(member)==str:
#                item_1 = QtWidgets.QTreeWidgetItem(item_0)
#                item_1.setText(0,'{},{}'.format(member,func[memberloads.loc[i,'function']]))
#                item_2 = QtWidgets.QTreeWidgetItem(item_1)
#                item_2.setText(0,str(memberloads.loc[i,'vector']))
#                item_3 = QtWidgets.QTreeWidgetItem(item_2)
#                item_3.setText(0,'self load: {}'.format(memberloads.loc[i,'self_load']))
#            else:
#                pass

    def generateSectionsTree(self):
        self.grouptree.clear()
        QtWidgets.QTreeWidgetItem(self.grouptree)
        self.grouptree.topLevelItem(0).setText(0,'New')        
        level = 1
        for name, beam in model.Beam.Groups.items():
            QtWidgets.QTreeWidgetItem(self.grouptree)
            self.grouptree.topLevelItem(level).setText(0,name)
            level+=1
        self.memberGrouptree.clear()
        level = 0
        for name in model.Beam.Groups.keys():
            QtWidgets.QTreeWidgetItem(self.memberGrouptree)
            self.memberGrouptree.topLevelItem(level).setText(0,name)
            level+=1
            
            
    def generateMembersTree(self):
        self.memberstree.clear()
        QtWidgets.QTreeWidgetItem(self.memberstree)
        self.memberstree.topLevelItem(0).setText(0,'New')        
        level = 1
        for name, beam in model.Beam.Beams.items():
            QtWidgets.QTreeWidgetItem(self.memberstree)
            self.memberstree.topLevelItem(level).setText(0,name)
            level+=1
            
            
    def generateSupportsTree(self):
        self.supportstree.clear()
        i = QtWidgets.QTreeWidgetItem(self.supportstree)
        self.supportstree.topLevelItem(0).setText(0,'New')
        i.setSelected(True)
        level = 1
        for node, support in model.Beam.NodalSupports.items():
            if any(s!=0 for s in support):
                QtWidgets.QTreeWidgetItem(self.supportstree)
                self.supportstree.topLevelItem(level).setText(0,node)
                level+=1
        
    def generateDispTree(self):
        self.dispstree.clear()
        i = QtWidgets.QTreeWidgetItem(self.dispstree)
        self.dispstree.topLevelItem(0).setText(0,'New')
        i.setSelected(True)
        level = 1
        for node, disp in model.Beam.Displacements.items():
            if any(d!=0 for d in disp):
                QtWidgets.QTreeWidgetItem(self.dispstree)
                self.dispstree.topLevelItem(level).setText(0,node)
                level+=1
        
          
    def generateRelTree(self):
        self.relstree.clear()
        i = QtWidgets.QTreeWidgetItem(self.relstree)
        self.relstree.topLevelItem(0).setText(0,'New')
        i.setSelected(True)
        level = 1
        for name, beam in model.Beam.Beams.items():
            if beam.release != None:
                startnode = beam.start_node
                stopnode = beam.stop_node
                QtWidgets.QTreeWidgetItem(self.relstree)
                self.relstree.topLevelItem(level).setText(0,'{},({}, {})'.format(name, startnode, stopnode))
                level+=1


    def generateRigTree(self):
        self.rigstree.clear()
        i = QtWidgets.QTreeWidgetItem(self.rigstree)
        self.rigstree.topLevelItem(0).setText(0,'New')
        i.setSelected(True)
        level = 1
        for name in model.Beam.RigidNode.keys():
            QtWidgets.QTreeWidgetItem(self.rigstree)
            self.rigstree.topLevelItem(level).setText(0,name)
            level+=1



            
    def generateAllTrees(self):
        self.generateProjectTree()
        self.generateSectionsTree()
        self.generateMembersTree()
        self.generateSupportsTree()
        self.generateDispTree()
        self.generateRelTree()
        self.generateRigTree()
        self.fillTabWidgets()


    def fillTabWidgets(self):
        '''Update element window'''
        nodelist = [' '] + list(model.Beam.Nodes.keys())
        memberlist = [' '] + list(model.Beam.Beams.keys())
#        grouplist = [' '] + list(model.Beam.Groups.keys())
        loadgrouplist = [' '] + list(model.Beam.LoadGroups)
        
        self.comboStart.clear()
        self.comboStart.addItems(nodelist)
        self.comboEnd.clear()
        self.comboEnd.addItems(nodelist)
        self.comboSupNodes.clear()
        self.comboSupNodes.addItems(nodelist)
        self.comboDispNodes.clear()
        self.comboDispNodes.addItems(nodelist)
#        self.comboStartEndNodes.clear()
#        self.comboStartEndNodes.addItems([' ', 'Start Node', 'End Node'])
        self.comboRelMembers.clear()
        self.comboRelMembers.addItems(memberlist)
        self.comboRigMembers.clear()
        self.comboRigMembers.addItems(memberlist)
        self.combo_loadMembers.clear()
        self.combo_loadMembers.addItems(memberlist)
        self.combo_loadNodes.clear()
        self.combo_loadNodes.addItems(nodelist)
        for item in [self.combo_loadGroups, self.combo_loadGroups_2]:
            item.clear()
            item.addItems(loadgrouplist)
        for box in [self.comboStart, self.comboEnd, self.comboSupNodes]:
            box.setCurrentIndex(0)
        for line in [self.lineStart, self.lineEnd, self.lineTheta]:
            line.clear()


    def addUpdateAll(self):
        '''Update everything after loading a saved project'''
        self.generateAllTrees()
        self.fillTabWidgets()
        for name, beam in model.Beam.Beams.items():
            self.addUpdateViewer(name,beam)   

  
    def clearAll(self):
        global thereisopenproject
        for dic in [model.Beam.Beams,model.Beam.RigidNode, model.Beam.Nodes, model.Beam.NodalSupports, model.Beam.RotatedSupports, model.Beam.Displacements, model.Beam.ElasticNode]:
            dic.clear()
#        model.Beam.Loads.clear()
        model.Beam.Loads = pd.DataFrame(columns = ['ITEM','node','member','function','a','b','group','nodestart','loadsstart','nodestop','loadsstop','loadsstart_release','self_load','vector'])
        model.Beam.Groups = {'Default':[[0,0,0,0,0,0,0,0],'custom']}
        for tree in [self.mainTree,self.listWidget, self.grouptree, self.memberstree, self.supportstree, self.memberGrouptree, self.dispstree, self.relstree, self.rigstree]:
            tree.clear()
        self.clearSectionTab()
        self.clearMemberTab()
        self.clearSupportTab()
        self.clearDispTab()
        self.clearRelTab()
        self.clearRigTab()
        thereisopenproject = False
        self.setWindowTitle(' ')
        self.viewer.clearAll()
        self.deactivateUI()


    def clearSectionTab(self):
        self.firstSection.setChecked(False)
        self.secondSection.setChecked(False)
        sectiontypes = [self.rbIPE, self.rbHE, self.rbIPN, self.rbHL, self.rbHD, self.rbHP, self.rbUPE, self.rbUPN, self.rbU]
        self.sectionSize.setExclusive(False)
        for sectiontype in sectiontypes:
            sectiontype.setChecked(False)
        self.sectionSize.setExclusive(True)
        self.comboSections.setCurrentText(' ')
        for item in [self.lineE1, self.linev1, self.lineG1, self.lineE, self.lineG, self.lineA, self.lineJ, self.lineIy, self.lineIz, self.lineW, self.linev]:
            item.clear()
        for item in [self.btnSaveChangGroup, self.btnDeleteGroup]:
            item.setEnabled(False)
        self.btnNewGroup.setEnabled(False)
    
    
    def clearHalfSectionTab(self,rb):
        item=self.grouptree.currentItem()
        if item==None:
            return
        group=item.text(0)
        if group=='New':
            return
        else:
            sectiontypes = [self.rbIPE, self.rbHE, self.rbIPN, self.rbHL, self.rbHD, self.rbHP, self.rbUPE, self.rbUPN, self.rbU]
            for item in [self.btnSaveChangGroup, self.btnDeleteGroup]:
                item.setEnabled(True)
            self.btnNewGroup.setEnabled(False)
            if rb==self.secondSection:
                for item in [self.lineE1, self.linev1, self.lineG1]:
                    item.clear()
                self.sectionSize.setExclusive(False)
                for sectiontype in sectiontypes:
                    sectiontype.setChecked(False)
                self.sectionSize.setExclusive(True)
            elif rb==self.firstSection:
                for item in [self.lineE, self.lineG, self.lineA, self.lineJ, self.lineIy, self.lineIz, self.lineW, self.linev]:
                    item.clear()
                self.sectionSize.setExclusive(False)
                for sectiontype in sectiontypes:
                    sectiontype.setChecked(False)
                self.sectionSize.setExclusive(True)
            else:
                return

    def clearMemberTab(self):
        self.loadList.clear()
        for box in [self.comboStart,self.comboEnd]:
            box.setCurrentIndex(0)
        for line in [self.lineStart,self.lineEnd, self.lineTheta, self.loadList]:
            line.clear()
        for button in [self.btnNewMember, self.btnSaveChangMember, self.btnDeleteMember]:
            button.setEnabled(False)


    def clearSupportTab(self):
        self.comboSupNodes.setCurrentText(' ')
        sups = [self.sup_x, self.sup_y, self.sup_z, self.sup_rotx, self.sup_roty, self.sup_rotz]
        for sup in sups:
            sup.setChecked(False)
        alllines = [self.rot_x, self.rot_y,self.rot_z, self.stiff_x, self.stiff_y, self.stiff_z, self.stiff_rotx, self.stiff_roty, self.stiff_rotz]
        for line in alllines:
            line.clear()


    def clearDispTab(self):
        self.comboDispNodes.setCurrentText(' ')
        alllines = [self.disp_x, self.disp_y, self.disp_z, self.disp_rotx, self.disp_roty, self.disp_rotz]
        for line in alllines:
            line.clear()


    def clearRelTab(self):
        self.comboRelMembers.setCurrentText(' ')
        alllines = [self.rel_x, self.rel_y, self.rel_z, self.rel_rotx, self.rel_roty, self.rel_rotz,self.rel_x2, self.rel_y2, self.rel_z2, self.rel_rotx2, self.rel_roty2, self.rel_rotz2]
        for line in alllines:
            line.clear()


    def clearRigTab(self):
        self.comboRigMembers.setCurrentText(' ')
        alllines = [self.rig_dxs, self.rig_dys, self.rig_dzs, self.rig_dxe, self.rig_dye, self.rig_dze]
        for line in alllines:
            line.clear()

    def resetView(self):
        self.viewer.GraphNodes.clear()
        self.viewer.GraphBeams.clear()
        self.viewer.GRAPHBEAMS.clear()
        self.viewer.zoom=0
        for name, beam in model.Beam.Beams.items():
            self.viewer.GraphBeams[name] = beam.start_node,beam.stop_node
            if beam.start_node not in self.viewer.GraphNodes:
                self.viewer.GraphNodes[beam.start_node] = beam.start*100
            if beam.stop_node not in self.viewer.GraphNodes:
                self.viewer.GraphNodes[beam.stop_node] = beam.stop*100
#        self.viewer.AxeNodes = {'n1':[0,0,0],'n2':[self.viewer.axis_size,0,0],'n3':[0,self.viewer.axis_size,0],'n4':[0,0,self.viewer.axis_size]}




    def addUpdateViewer(self,*args):
        if len(args)==2:
            name = args[0]
            beam= args[1]
            self.viewer.GraphBeams[name] = beam.start_node,beam.stop_node
            if beam.start_node not in self.viewer.GraphNodes:
                self.viewer.GraphNodes[beam.start_node] = beam.start*100
            if beam.stop_node not in self.viewer.GraphNodes:
                self.viewer.GraphNodes[beam.stop_node] = beam.stop*100
        self.viewer.drawStructure()


    def activateUI(self):
        for item in [self.btnyzview, self.btnxzview, self.btnxyview, self.btndefault, self.actionSave, self.actionSaveAs, self.save_file, self.analysis,self.viewresults]:
            item.setEnabled(True)
        self.tab_top.setEnabled(True)
        self.tab_bottom.setEnabled(True)
        
        
    def deactivateUI(self):
        for item in [self.btnyzview, self.btnxzview, self.btnxyview, self.btndefault, self.actionSave, self.actionSaveAs, self.save_file, self.analysis,self.viewresults]:
            item.setEnabled(False)
        self.tab_top.setEnabled(False)
        self.tab_bottom.setEnabled(False)

#####    MANAGEMENT OF CREATING, LOADING, SAVING AND CLOSING PROJECTS     #####
    
    def saveProject(self, filename):
        column_names = ['ITEM', 'GRname' ,'GRdata' ,'NOname', 'coords', 'BEname', 'start','start_node', 'stop', 'stop_node', 'theta', 'Bgroup' ,'SUPname' ,'support' ,'RSUPname' ,'angles' , 'DISPname', 'disps', 'ELNOname' ,'stiffness' ,'node','member','function','a','b','group','nodestart','loadsstart','nodestop','loadsstop','loadsstart_release','self_load']
        df = pd.DataFrame(columns = column_names)
        BEAMS = model.Beam.Beams
        NODES = model.Beam.Nodes
        NODESUPPORTS = model.Beam.NodalSupports
        ROTSUPPORTS = model.Beam.RotatedSupports
        DISPLACEMENTS = model.Beam.Displacements
        ELASTNODE = model.Beam.ElasticNode
        RIGIDNODE = model.Beam.RigidNode
        LOADS = model.Beam.Loads
        GROUPS = model.Beam.Groups
        RELS = {}
        for beam in BEAMS.values():
            df = df.append({'ITEM':'BEAM','BEname':beam.name , 'start':list(beam.start), 'start_node':beam.start_node, 'stop':list(beam.stop), 'stop_node': beam.stop_node, 'theta':beam.theta, 'Bgroup':beam.group}, ignore_index=True)
        for node,coords in NODES.items():
            df = df.append({'ITEM':'NODE','NOname': node,'coords': coords}, ignore_index=True)
        for name, value in NODESUPPORTS.items():
            df = df.append({'ITEM':'SUP','SUPname': name,'support':value}, ignore_index=True)
        for name, value in ROTSUPPORTS.items():
            df = df.append({'ITEM':'ROTSUP','RSUPname': name,'angles':value}, ignore_index=True)
        for name, value in DISPLACEMENTS.items():
            df = df.append({'ITEM':'DISPS','DISPname': name,'disps':value}, ignore_index=True)
        for name, value in ELASTNODE.items():
            df = df.append({'ITEM':'ELNO','ELNOname': name,'stiffness':value}, ignore_index=True)
        for name, value in RIGIDNODE.items():
            df = df.append({'ITEM':'RIGID','RIGname': name,'rigs':value}, ignore_index=True)
        for name,beam in BEAMS.items():
            if beam.release!=None:
                RELS[name] = beam.release
        for name , value in RELS.items():
            df = df.append({'ITEM':'REL','RELname': name,'rels':value}, ignore_index=True)
        for name, value in GROUPS.items():
            df = df.append({'ITEM':'GROUP','GRname': name,'GRdata':value}, ignore_index=True)
        df = df.fillna('None')
        loads = LOADS.loc[:,['loadsstart','loadsstop','loadsstart_release','vector']]
        for col in ['loadsstart','loadsstop','loadsstart_release','vector']:
            LOADS[col]= loads[col]
        LOADS = LOADS.fillna('None')
        df=pd.concat([df,LOADS], axis=0, join='outer', ignore_index=True)
        df = df.fillna('None')
        df.to_csv(filename)

    def loadProject(self, name):
        self.readProject(name)
        self.addUpdateAll()


    def readProject(self, name):
#        loaddf = pd.read_csv(name,dtype={'member':'str'})
        loaddf = pd.read_csv(name)
        loaddf = loaddf.astype('str')
#        loaddf = pd.DataFrame.from_csv(name)
        groups = loaddf[loaddf['ITEM']=='GROUP'].reset_index(drop=True)
        beams = loaddf[loaddf['ITEM']=='BEAM'].reset_index(drop=True)
        nodes = loaddf[loaddf['ITEM']=='NODE'].reset_index(drop=True)
        supports = loaddf[loaddf['ITEM']=='SUP'].reset_index(drop=True)
        rotsupports = loaddf[loaddf['ITEM']=='ROTSUP'].reset_index(drop=True)
        displacements = loaddf[loaddf['ITEM']=='DISPS'].reset_index(drop=True)
        elastnodes = loaddf[loaddf['ITEM']=='ELNO'].reset_index(drop=True)
        rigidnodes = loaddf[loaddf['ITEM']=='RIGID'].reset_index(drop=True)
        releases = loaddf[loaddf['ITEM']=='REL'].reset_index(drop=True)
        loads = loaddf[loaddf['ITEM']=='LOAD'].reset_index(drop=True)
        for i in range(len(groups)):
            data = []
            d = groups['GRdata'][i]
            d = d.replace(" ", "")
            d = d.replace("[", "")
            d = d.replace("]", "")
            d = d.split(',')
            data.append([float(j.replace(",", "")) for j in d[:-1]])
            data.append(d[-1][1:-1])
            model.Beam.Groups[groups['GRname'][i]]=data
        for i in range(len(nodes)):
            c = nodes['coords'][i]
            c = c.replace(" ", "")
            c = c[1:-1].split(',')
            coords = [float(j.replace(",", "")) for j in c]
            model.Beam.Nodes[nodes['NOname'][i]]=coords
        for i in range(len(beams)):
            name, start, stop, theta, group = beams['BEname'][i], beams['start_node'][i], beams['stop_node'][i], float(beams['theta'][i]), beams['Bgroup'][i]
            model.addElement(name,start, stop, theta, group)
        for i in range(len(supports)):
            s = supports['support'][i]
            s = s.replace(" ", "")
            s = s[1:-1].split(',')
            sups = [float(j.replace(",", "")) for j in s]
            model.Beam.NodalSupports[supports['SUPname'][i]]=sups
        for i in range(len(rotsupports)):
            a = rotsupports['angles'][i]
            a = a.replace(" ", "")
            a = a[1:-1].split(',')
            angles = [float(j.replace(",", "")) for j in a]            
            model.Beam.RotatedSupports[rotsupports['RSUPname'][i]] = angles
        for i in range(len(displacements)):
            d = displacements['disps'][i]
            d = d.replace(" ", "")
            d = d[1:-1].split(',')
            disp = [float(j.replace(",", "")) for j in d]            
            model.Beam.Displacements[displacements['DISPname'][i]] = disp
        for i in range(len(elastnodes)):
            e = elastnodes['stiffness'][i]
            e = e.replace(" ", "")
            e = e[1:-1].split(',')
            stiff = [float(j.replace(",", "")) for j in e]            
            model.Beam.ElasticNode[elastnodes['ELNOname'][i]] = stiff
        for i in range(len(rigidnodes)):
            v = rigidnodes['rigs'][i]
            rig=[]
            v = v.replace("[", "")
            v = v.replace("]", "")
            v = v.replace("(", "")
            v = v.replace(")", "")
            v = v.replace(" ", ",")
            v = v.split(',')
            v = [j.replace(',','') for j in v]
            v = [i for i in v if i!='']
            listvec = [float(j) for j in v]
            start = listvec[:3]
            stop = listvec[3:]
            rig.append(start)
            rig.append(stop)
            model.Beam.RigidNode[rigidnodes['RIGname'][i]] = rig
        for i in range(len(releases)):
            r = releases['rels'][i]
            name = releases['RELname'][i]
            rel = []
            r = r.replace("[", "")
            r = r.replace("]", "")
            r = r.replace("(", "")
            r = r.replace(")", "")
            r = r.replace(" ", ",")
            r = r.split(',')
            r = [j.replace(',','') for j in r]
            r = [i for i in r if i!='']
            listrel = [float(j) for j in r]
            reledge = listrel[:2]
            rels = listrel[2:14]
            angles = listrel[14:]
            rel.append(reledge)
            rel.append(rels)
            rel.append(angles)
            model.Beam.Beams[name].release=rel
        Loads = loads.loc[:,['ITEM','node','member','function','group','nodestart','nodestop','self_load']]
        readvector = loads['vector']
        vector = []
        for i in range(len(readvector)):
            v = readvector[i]
            if len(v.split(',')) ==3:
                v = v.replace(" ", ",")
                v = v[1:-1].split(',')
                v = [j.replace(',','') for j in v]
                v = [i for i in v if i!='']
                vec = [float(j) for j in v]
                vector.append(vec)
            elif len(v.split(',')) ==6:
                vec=[]
                v = v.replace("[", "")
                v = v.replace("]", "")
                v = v.replace("(", "")
                v = v.replace(")", "")
                v = v.replace(" ", ",")
                v = v.split(',')
                v = [j.replace(',','') for j in v]
                v = [i for i in v if i!='']
                listvec = [float(j) for j in v]
                start = listvec[:3]
                stop = listvec[3:]
                vec.append(start)
                vec.append(stop)
                vector.append(vec)
            elif len(v.split(',')) ==4:
                vec=[]
                v = v.replace("[", "")
                v = v.replace("]", "")
                v = v.replace("(", "")
                v = v.replace(")", "")
                v = v.replace(" ", ",")
                v = v.split(',')
                v = [j.replace(',','') for j in v]
                v = [i for i in v if i!='']
                listvec = [float(j) for j in v]
                if listvec[0]==0:
                    start = 0
                    stop = listvec[1:]
                else:
                    start = listvec[:3]
                    stop = 0
                vec.append(start)
                vec.append(stop)
                vector.append(vec)
            else:
                vector.append(None)
        a=[]
        b=[]
        for col in loads['a']:
            item = float(col) if col!='None' else 0
            a.append(item)
        for col in loads['b']:
            item = float(col) if col!='None' else 0
            b.append(item)
        loadsstart = loads['loadsstart'].reset_index(drop=True)
        lstart = []
        for i in range(len(loadsstart)):
            l = loadsstart[i]
            l = l.replace("\n", "")
            l = l.replace(" ", ",")
            l = l[1:-1].split(',')
            l = [j.replace(',','') for j in l]
            l = [i for i in l if i!='']
            load = [float(j) for j in l]
            lstart.append(load)
        loadsstop = loads['loadsstop'].reset_index(drop=True)
        lstop = []
        for i in range(len(loadsstop)):
            l = loadsstop[i]
            l = l.replace("\n", "")
            l = l.replace(" ", ",")
            l = l[1:-1].split(',')
            l = [j.replace(',','') for j in l]
            l = [i for i in l if i!='']
            load = [float(j) for j in l]
            lstop.append(load)
        loadsstart_release = loads['loadsstart_release'].reset_index(drop=True)
        lrel = []
        for i in range(len(loadsstart_release)):
            l = loadsstart_release[i]
            if l!='None':
                l = l.replace("\n", "")
                l = l.replace(" ", ",")
                l = l[1:-1].split(',')
                l = [j.replace(',','') for j in l]
                l = [i for i in l if i!='']
                load = [float(j) for j in l]
                lrel.append(load)
            else:
                lrel.append(None)
        Loads.loc[:,'a'] = pd.Series(a)
        Loads.loc[:,'b'] = pd.Series(b)
        Loads.loc[:,'loadsstart'] = pd.Series(lstart)
        Loads.loc[:,'loadsstop'] = pd.Series(lstop)
        Loads.loc[:,'loadsstart_release'] = pd.Series(lrel)
        Loads.loc[:,'vector'] = pd.Series(vector)
        model.Beam.Loads = Loads

    
    def openFileNameDialog(self):
        global thereisopenproject
        if thereisopenproject:
            self.close()
            if not thereisopenproject:
                options = QtWidgets.QFileDialog.Options()
                name, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Choose a file to open", "","All Files (*);;CSV Files (*.csv)", options=options)
                if name:
                    realname = self.realWorldName(name)
                    self.projectname = name
#                    self.loadProject(name)
                    try:
                        self.loadProject(name)
                    except:
                        self.singleEvent('', 'This project could not be loaded')
                        self.clearAll()
                        return
                    thereisopenproject=True
                    self.setWindowTitle(realname)
                    self.activateUI()
        else:
            options = QtWidgets.QFileDialog.Options()
            name, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Choose a file to open", "","All Files (*);;CSV Files (*.csv)", options=options)
            if name:
                self.projectname = name
#                self.loadProject(name)
                try:
                    self.loadProject(name)
                except:
                    self.singleEvent('', 'This project could not be loaded')
                    self.clearAll()
                    return
                thereisopenproject=True
                self.setWindowTitle(self.realWorldName(name))
                self.activateUI()


    def saveFileDialog(self):
        currentname = self.projectname
        options = QtWidgets.QFileDialog.Options()
        name, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save as",currentname,"All Files (*);;CSV Files (*.csv)", options=options)
        if name:
            self.saveProject(name)
            self.projectname = name
            realname = self.realWorldName(name)
            self.setWindowTitle(realname)
            return True
        else: 
            return False

    
    def realWorldName(self,name):
        for i,c in enumerate(name):
            if c=='/':
                realname=name[i+1:-4]
        return realname


    def saveAsIs(self):
        filename = self.projectname
        if os.path.isfile(filename):
            try:
                os.remove(filename)
                self.saveProject(filename)
            except:
                self.singleEvent('', 'Could not save this project.\nCheck if the file is already opened with another program.')
                return
        else:
            self.saveProject(filename)



    def createNewProject(self):
        global thereisopenproject
        if thereisopenproject:
            self.close()
            if not thereisopenproject:
                if self.getInitialProjectName()==True:
                    thereisopenproject=True
                    self.generateAllTrees()
                    self.activateUI()
                else:
                    return
        else:
            if self.getInitialProjectName()==True:
                thereisopenproject=True
                self.generateAllTrees()
                self.activateUI()
            else:
                return


    def getInitialProjectName(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'New Project', "Enter a name for the new project")
        if ok:
            self.projectname = text
            if text=='':
                self.singleEvent('', 'Please type a name for your project')
                self.getInitialProjectName()
                return False
            for c in text:
                if c in ["<",">",":",'"',"/","\\","?","*","|"]:
                    self.singleEvent('', 'The name contains one or more invalid characters')
                    self.getInitialProjectName()
                    return False
            if text in ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']:
                self.singleEvent('', 'This is an invalid name')
                self.getInitialProjectName()
                return False
            if text[-1]==' ' or text[-1]=='.':
                self.singleEvent('', 'The last character is invalid')
                self.getInitialProjectName()
                return False
            self.setWindowTitle(self.projectname)
            return True
        else:
            return False



#--------   START OF EVENT FUNCTIONS ------------------------------------------

    def singleEvent(self,message,explain):
        mes = QtWidgets.QMessageBox()
        mes.setWindowTitle(message)
        mes.setText(explain)
        mes.setStandardButtons(QtWidgets.QMessageBox.Close)
        style = "background-color: rgb(218, 218, 218);"
        mes.setStyleSheet(style)
        mes.exec()


    def dChoiceEvent(self,message,explain):
        mes = QtWidgets.QMessageBox()
        mes.setWindowTitle(message)
        mes.setText(explain)
        mes.setStandardButtons(QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
        style = "background-color: rgb(218, 218, 218);"
        mes.setStyleSheet(style)
        return mes.exec()


    def keyPressEvent(self,event):
        key = event.key()
        if key==QtCore.Qt.Key_Control:
            self.mainTree.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            self.grouptree.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            self.memberstree.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            self.dispstree.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            self.supportstree.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            self.relstree.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            self.rigstree.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        if self.btnNewMember.isEnabled() and event.key()==QtCore.Qt.Key_Return and self.tab_top.currentIndex()==1:
            self.addElement()
        if self.btnNewGroup.isEnabled() and event.key()==QtCore.Qt.Key_Return and self.tab_top.currentIndex()==0:
            self.getGroupvalue()
        if self.btnNewSupport.isEnabled() and event.key()==QtCore.Qt.Key_Return and self.tab_top.currentIndex()==2:
            self.getSupportValue()
        if self.btnNewDisplacement.isEnabled() and event.key()==QtCore.Qt.Key_Return and self.tab_top.currentIndex()==3:
            self.getDispValues()
        if self.btnNewRelease.isEnabled() and event.key()==QtCore.Qt.Key_Return and self.tab_top.currentIndex()==4:
            self.getRelValues()
        if self.btnNewRig.isEnabled() and event.key()==QtCore.Qt.Key_Return and self.tab_top.currentIndex()==5:
            self.getRigValues()
        if key == QtCore.Qt.Key_Escape:
            self.close()
        if key == QtCore.Qt.Key_F11:
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()


    def keyReleaseEvent(self,event):
        key = event.key()
        if key==QtCore.Qt.Key_Control:
            self.mainTree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.grouptree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.memberstree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.dispstree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.supportstree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.relstree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.rigstree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)


    def center(self):
        "get the available geometry of the screen and center the window - then move it top left"
        qr = self.frameGeometry()
        cs = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cs)
        self.move(qr.topLeft())
        
        
    def closeEvent(self, event):
        global thereisopenproject
        if thereisopenproject:
            reply = QtWidgets.QMessageBox.question(
                self, "Message",
                "This action will close the current project. Are you sure you want to proceed?",
                QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Close | QtWidgets.QMessageBox.Cancel,
                QtWidgets.QMessageBox.Save)
            if reply == QtWidgets.QMessageBox.Close:
                self.clearAll()
                event.ignore()
#                self.appExit()
            elif reply == QtWidgets.QMessageBox.Save:
                if self.saveFileDialog():
                    self.clearAll()
                    event.ignore()
#                    self.appExit()
            else:
                event.ignore()
        else:
            self.appExit()

    def appExit(self):
        QtCore.QCoreApplication.instance().quit()
        
#--------   END OF EVENTS FUNCTIONS  ------------------------------------------


class QPosFloatValidator(QtGui.QValidator):
    def __init__(self):
        super(QPosFloatValidator,self).__init__()
    
    def validate(self,number,pos):
        if not number:
            return (QtGui.QValidator.Intermediate,number,pos)
        try:
            float(number)
        except ValueError:
            return (QtGui.QValidator.Invalid,number,pos)
        if isinstance(float(number),float):
            return (QtGui.QValidator.Intermediate,number,pos)
        return (QtGui.QValidator.Acceptable,number,pos)
    
    def fixup(self, number):
        pass


class QFloatValidator(QtGui.QValidator):
    def __init__(self):
        super(QFloatValidator,self).__init__()
    
    def validate(self,number,pos):
        if not number or number=='-':
            return (QtGui.QValidator.Intermediate,number,pos)
        try:
            float(number)
        except ValueError:
            return (QtGui.QValidator.Invalid,number,pos)
        if isinstance(float(number),float):
            return (QtGui.QValidator.Intermediate,number,pos)
        return (QtGui.QValidator.Acceptable,number,pos)
    
    def fixup(self, number):
        pass



class StructureViewer(QtWidgets.QGraphicsView):
    GraphItems = {}
    GraphNodes = {}
    GraphBeams = {}
    GRAPHBEAMS = {}
    GRAPHAXES = {}
    axis_size =125
    selfGeometry = [100, 100, 700, 500]
    AxeNodes = {'n1':[0,0,0],'n2':[axis_size,0,0],'n3':[0,axis_size,0],'n4':[0,0,axis_size]}
    Axes = {'x':['n1','n2'],'y':['n1','n3'],'z':['n1','n4']}
    black = QtCore.Qt.black
    blue = QtCore.Qt.blue
    red = QtCore.Qt.red
    green = QtCore.Qt.green
    yellow = QtCore.Qt.yellow
    axecolors = {'center':black,'x':blue,'y':red,'z':yellow}


    def __init__(self,parent):
        super(StructureViewer, self).__init__(parent)
        self.zoom = 0
        self.angle = 2
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1,\
                                        stop:0 rgba(210, 210, 210, 255), stop:1 rgba(240, 240, 240, 255));border-color: rgba(140, 140, 140, 255);")
        self.setFrameShape(QtWidgets.QFrame.Panel)
        self.setGeometry(QtCore.QRect(self.selfGeometry[0], self.selfGeometry[1], self.selfGeometry[2], self.selfGeometry[3]))
        self.linewidth = 1
        self.scene = QtWidgets.QGraphicsScene()
        self.setScene(self.scene)


    def clearAll(self):
        self.zoom = 0
        self.angle = 2
        self.linewidth = 1
        for dic in [self.GRAPHAXES,self.GRAPHBEAMS, self.GraphBeams, self.GraphNodes, self.GraphItems]:
            dic.clear()
        self.scene.clear()


    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoom +=1
            self.scale(1.25,1.25)
        else:
            self.zoom-=1
            self.scale(0.8,0.8)
        if self.zoom>=0:
            for key,item in self.GRAPHBEAMS.items():
                item.setPen(QtGui.QPen(QtGui.QColor(0,0,0), self.linewidth/(1.25**(self.zoom))))
            for axe in self.GRAPHAXES.values():
                axe.setScale(1/(1.25**(self.zoom)))
        else:
            for key,item in self.GRAPHBEAMS.items():
                item.setPen(QtGui.QPen(QtGui.QColor(0,0,0), self.linewidth*(1.25**abs(self.zoom))))
            for axe in self.GRAPHAXES.values():
                axe.setScale(1.25**(abs(self.zoom)))
        self.placeAxes()

#    def itemChange(self, change):
#        if change in [QtGui.QgraphicsItem.ItemPositionChange, QtGui.QgraphicsItem.ItemSceneHasChanged]:
#            self.placeAxes()


    def rotateStructure(self, view='default'):
        self.scene.clear()
        for name in self.GraphBeams.keys():
            self.drawBeam(name, view)
        for node in self.GraphNodes.keys():
            self.drawNode(node, view)
        self.drawAxes(view)
        self.linewidth = self.v/600
        self.fitInView(0,0,self.v,self.v,QtCore.Qt.KeepAspectRatio)
        self.centerOn(100,-100)
        if self.zoom>=0:
            self.scale(1.25**(self.zoom),1.25**(self.zoom))
            for item in self.GRAPHBEAMS.values():
                item.setPen(QtGui.QPen(QtGui.QColor(0,0,0), self.linewidth/(1.25**(self.zoom))))
            for axe in self.GRAPHAXES.values():
                axe.setScale(1/(1.25**(self.zoom)))
        else:
            self.scale(0.8**abs(self.zoom),0.8**abs(self.zoom))
            for item in self.GRAPHBEAMS.values():
                item.setPen(QtGui.QPen(QtGui.QColor(0,0,0), self.linewidth*(1.25**abs(self.zoom)))) 
            for axe in self.GRAPHAXES.values():
                axe.setScale(1.25**abs(self.zoom))
        self.placeAxes()
        self.drawNames()


    def drawStructure(self,view='default'):
        self.scene.clear()
        if len(self.GraphBeams)==0:
            return
        for name in self.GraphBeams.keys():
            self.drawBeam(name, view)
        for node in self.GraphNodes.keys():
            self.drawNode(node, view)
        self.bounds = self.scene.itemsBoundingRect()
        self.scene.setSceneRect(self.bounds)
        boundsX = self.bounds.x() - 200
        boundsY = self.bounds.y() - 200
        boundsW = self.bounds.width() + 400
        boundsH = self.bounds.height() + 400
        self.myscene = QtCore.QRectF(boundsX, boundsY, boundsW, boundsH)
        self.v=max([self.myscene.width(),self.myscene.height()])
        self.linewidth = self.v/600
        self.scene.setSceneRect(self.myscene)
        self.fitInView(0,0,self.v,self.v,QtCore.Qt.KeepAspectRatio)
        if self.zoom>=0:
            self.scale(1.25**(self.zoom),1.25**(self.zoom))
            for item in self.GRAPHBEAMS.values():
                item.setPen(QtGui.QPen(QtGui.QColor(0,0,0), self.linewidth/(1.25**(self.zoom))))
        else:
            self.scale(0.8**abs(self.zoom),0.8**abs(self.zoom))
            for item in self.GRAPHBEAMS.values():
                item.setPen(QtGui.QPen(QtGui.QColor(0,0,0), self.linewidth*(1.25**abs(self.zoom))))
        if view =='default':
            self.drawLoads()
            self.drawNames()
            self.drawSupports()
        start = self.mapToScene(0,0)
        stop = self.mapToScene(0,20)
        self.axis_size = abs(stop.y()-start.y())
        self.axis_width = self.axis_size//20
        self.AxeNodes = {'n1':[0,0,0],'n2':[self.axis_size,0,0],'n3':[0,self.axis_size,0],'n4':[0,0,self.axis_size]}
        self.drawAxes(view)
        self.placeAxes()


    def drawNode(self,node, view):
        coords = self.GraphNodes[node]
        if view=='default':
            x,y = self.convert3Dto2D((coords))
        elif view=='XZ':
            x,y = self.XZconvert3Dto2D((coords))
        elif view=='YZ':
            x,y = self.YZconvert3Dto2D((coords))
        elif view=='XY':
            x,y = self.XYconvert3Dto2D((coords))
        wx,wy=8,8
        self.pen=self.black
        self.brush = QtGui.QBrush()
        self.brush.setColor(self.black)
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.scene.addEllipse(x-wx/2,y-wy/2,wx,wy,self.pen, self.brush)
        
        
    def drawBeam(self,name, view):
        start3d = self.GraphBeams[name][0]
        stop3d = self.GraphBeams[name][1]
        start3d = self.GraphNodes[start3d]
        stop3d = self.GraphNodes[stop3d]
        if view=='default':
            startx, starty = self.convert3Dto2D(start3d)
            stopx, stopy = self.convert3Dto2D(stop3d)
        elif view=='XZ':
            startx, starty = self.XZconvert3Dto2D(start3d)
            stopx, stopy = self.XZconvert3Dto2D(stop3d)
        elif view=='YZ':
            startx, starty = self.YZconvert3Dto2D(start3d)
            stopx, stopy = self.YZconvert3Dto2D(stop3d)
        elif view=='XY':
            startx, starty = self.XYconvert3Dto2D(start3d)
            stopx, stopy = self.XYconvert3Dto2D(stop3d)
        item = QtWidgets.QGraphicsLineItem()
        item.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        item.setPen(QtGui.QPen(QtGui.QColor(0,0,0), self.linewidth))
        item.setLine(startx, starty, stopx, stopy)
        self.GRAPHBEAMS[name]=item
        self.scene.addItem(item)
        
        #releases
        beam = model.Beam.Beams[name]
        if beam.release!=None:
            brush = QtGui.QBrush(self.black, QtCore.Qt.SolidPattern)

            releasestart = beam.release[0][0]
            releasestop = beam.release[0][1]
            if releasestart == 1:
                itemrelstrt = QtWidgets.QGraphicsEllipseItem(startx + (stopx - startx)/8-4, starty + (stopy-starty)/8-4, 8, 8)
                itemrelstrt.setBrush(brush)
                self.scene.addItem(itemrelstrt)
            if releasestop == 1:
                itemrelstp = QtWidgets.QGraphicsEllipseItem(stopx - (stopx - startx)/8-4, stopy - (stopy-starty)/8-4, 8, 8)
                itemrelstp.setBrush(brush)
                self.scene.addItem(itemrelstp)
        self.bounds = self.scene.itemsBoundingRect()

    
    def drawSupports(self):
        supports = model.Beam.NodalSupports
        for node in supports.keys():
            if any(s!=0 for s in supports[node]):
                if all(u==1 for u in supports[node]):
                    try:
                        x, y = self.convert3Dto2D(self.GraphNodes[node])
                        pakt = QtWidgets.QGraphicsRectItem(x-10,y-10, 20, 20)
                        self.scene.addItem(pakt)
                    except:
                        pass
                elif all(o==0 for o in supports[node][3:]):
                    if all(p==1 for p in supports[node][:3]):
                        try:
                            x, y = self.convert3Dto2D(self.GraphNodes[node])
                            arthr = QtWidgets.QGraphicsPolygonItem(QtGui.QPolygonF([QtCore.QPointF(x,y-12), QtCore.QPointF(x-12,y+12), QtCore.QPointF(x+12,y+12)]))
                            self.scene.addItem(arthr)
                        except:
                            pass
                    else:
                        try:
                            x, y = self.convert3Dto2D(self.GraphNodes[node])
                            kyl = QtWidgets.QGraphicsRectItem(x-10,y, 20, 5)
                            k1 = QtWidgets.QGraphicsEllipseItem(x-10,y+5, 10, 10)
                            k2 = QtWidgets.QGraphicsEllipseItem(x,y+5, 10, 10)
                            self.scene.addItem(kyl)
                            self.scene.addItem(k1)
                            self.scene.addItem(k2)
                        except:
                            pass
                else:
                    try:
                        x, y = self.convert3Dto2D(self.GraphNodes[node])
                        allo = QtWidgets.QGraphicsEllipseItem(x-10,y-10, 20, 20)
                        self.scene.addItem(allo)
                    except:
                        pass
                    
    def drawNames(self):
        #members
        for name, nodes in self.GraphBeams.items():
            start3d = self.GraphNodes[nodes[0]]
            stop3d = self.GraphNodes[nodes[1]]
            startx, starty = self.convert3Dto2D(start3d)
            stopx, stopy = self.convert3Dto2D(stop3d)
            beamname = QtWidgets.QGraphicsTextItem()
            beamname.setPos(startx + (stopx - startx)/3, starty + (stopy-starty)/3)
            beamname.setPlainText(name)
            self.scene.addItem(beamname)
        #nodes
        for name, coords in self.GraphNodes.items():
            x, y = self.convert3Dto2D(coords)
            nodename = QtWidgets.QGraphicsTextItem()
            nodename.setPos(x,y)
            nodename.setPlainText(name)
            self.scene.addItem(nodename)
        #supports
        supports = model.Beam.NodalSupports
        for node, support in supports.items():
            try:
                if support!=[0,0,0,0,0,0]:
                    name = str([int(i) for i in support])
                    coords = self.GraphNodes[node]
                    x, y = self.convert3Dto2D(coords)
                    supp = QtWidgets.QGraphicsTextItem()
                    if len(node)==2:
                        supp.setPos(x+15,y)
                    elif len(node)==3:
                        supp.setPos(x+20,y)
                    else:
                        supp.setPos(x+25,y)
                    supp.setPlainText(name)
                    self.scene.addItem(supp)
            except:
                pass
    

            


    def drawLoads(self):
        loads = model.Beam.Loads
        nodalloads = loads[loads['function']=='Nodal load'].reset_index(drop=True)
        pointloads = loads[loads['function']=='Po'].reset_index(drop=True)
        momentloads = loads[loads['function']=='M'].reset_index(drop=True)
        evenloads = loads[(loads['function']=='FE') | (loads['function']=='PE')].reset_index(drop=True)
        triangloads = loads[(loads['function']=='FT') | (loads['function']=='PT')].reset_index(drop=True)
        trapezloads = loads[(loads['function']=='FR') | (loads['function']=='PR')].reset_index(drop=True)
        length = self.v/5
        try:
            for i in range(len(nodalloads)):
                #arrow
                vector = self.convert3Dto2D(nodalloads['loadsstart'][i][:3])
                node = nodalloads['node'][i]
                stop = self.convert3Dto2D(self.GraphNodes[node])
                startx = stop[0] - vector[0]
                starty = stop[1] - vector[1]
                start = [startx, starty]
                item = QtWidgets.QGraphicsLineItem()
                item.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
                item.setPen(QtGui.QPen(self.red,length/50))
                item.setLine(start[0], start[1], stop[0], stop[1])
                #arrowhead
                genvec = np.array([[0,0], np.array(start)-np.array(stop)])/8
                th = np.pi/6
                rot1 = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
                rot2 = np.array([[np.cos(-th), -np.sin(-th)], [np.sin(-th), np.cos(-th)]])
                h1 = np.dot(genvec, rot1)
                h2 = np.dot(genvec, rot2)
                
                item1 = QtWidgets.QGraphicsLineItem()
                item1.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
                item1.setPen(QtGui.QPen(self.red,length/50))
                item1.setLine(h1[0][0], h1[0][1], h1[1][0], h1[1][1])
                item1.setPos(stop[0], stop[1])
                
                item2 = QtWidgets.QGraphicsLineItem()
                item2.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
                item2.setPen(QtGui.QPen(self.red,length/50))
                item2.setLine(h2[0][0], h2[0][1], h2[1][0], h2[1][1])
                item2.setPos(stop[0], stop[1])
                item.setOpacity(0.4)
                item1.setOpacity(0.4)
                item2.setOpacity(0.4)
                self.scene.addItem(item)
                self.scene.addItem(item1)
                self.scene.addItem(item2)
        except:
            pass
        try:
            for i in range(len(momentloads)):
                vector = self.convert3Dto2D(momentloads['vector'][i])
                nodes = (momentloads['nodestart'][i],momentloads['nodestop'][i])
                try:
                    vecmember = np.array([self.GraphNodes[nodes[1]][j] - self.GraphNodes[nodes[0]][j] for j in range(3)])
                except:
                    return
                univecmember = vecmember/np.linalg.norm(vecmember)
                a = momentloads['a'][i]*100
                avect = a*univecmember
                point = [avect[k]+self.GraphNodes[nodes[0]][k] for k in range(3)]
                stop = self.convert3Dto2D(point)
                startx = stop[0] - vector[0]
                starty = stop[1] - vector[1]
                start = [startx, starty]
                momentpath = QtGui.QPainterPath()
                momentpath.moveTo(stop[0], stop[1])
                momentpath.arcTo(stop[0]-20, stop[1]-20, 40,40, -45, 225)
                moment = QtWidgets.QGraphicsPathItem(momentpath)
                moment.setPen(QtGui.QPen(self.red,length/50))
                moment.setOpacity(0.4)
                self.scene.addItem(moment)
        except:
            pass
        try:
            for i in range(len(pointloads)):
                vector = self.convert3Dto2D(pointloads['vector'][i])
                nodes = (pointloads['nodestart'][i],pointloads['nodestop'][i])
                try:
                    vecmember = np.array([self.GraphNodes[nodes[1]][j] - self.GraphNodes[nodes[0]][j] for j in range(3)])
                except:
                    return
                univecmember = vecmember/np.linalg.norm(vecmember)
                a = pointloads['a'][i]*100
                avect = a*univecmember
                point = [avect[k]+self.GraphNodes[nodes[0]][k] for k in range(3)]
                stop = self.convert3Dto2D(point)
                startx = stop[0] - vector[0]
                starty = stop[1] - vector[1]
                start = [startx, starty]
                item = QtWidgets.QGraphicsLineItem()
                item.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
                item.setPen(QtGui.QPen(self.red,length/50))
                item.setLine(start[0], start[1], stop[0], stop[1])
                #arrowhead
                genvec = np.array([[0,0], np.array(start)-np.array(stop)])/8
                th = np.pi/6
                rot1 = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
                rot2 = np.array([[np.cos(-th), -np.sin(-th)], [np.sin(-th), np.cos(-th)]])
                h1 = np.dot(genvec, rot1)
                h2 = np.dot(genvec, rot2)
                
                item1 = QtWidgets.QGraphicsLineItem()
                item1.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
                item1.setPen(QtGui.QPen(self.red,length/50))
                item1.setLine(h1[0][0], h1[0][1], h1[1][0], h1[1][1])
                item1.setPos(stop[0], stop[1])
                
                item2 = QtWidgets.QGraphicsLineItem()
                item2.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
                item2.setPen(QtGui.QPen(self.red,length/50))
                item2.setLine(h2[0][0], h2[0][1], h2[1][0], h2[1][1])
                item2.setPos(stop[0], stop[1])
                item.setOpacity(0.4)
                item1.setOpacity(0.4)
                item2.setOpacity(0.4)
                self.scene.addItem(item)
                self.scene.addItem(item1)
                self.scene.addItem(item2)
        except:
            pass
        evenloads = evenloads[evenloads['self_load']=='NO'].reset_index(drop=True)
        try:
            for i in range(len(evenloads)):
                nodes = (evenloads['nodestart'][i],evenloads['nodestop'][i])
                vector = self.convert3Dto2D(evenloads['vector'][i])
                try:
                    vecmember = np.array([self.GraphNodes[nodes[1]][j] - self.GraphNodes[nodes[0]][j] for j in range(3)])
                except:
                    return
                univecmember = vecmember/np.linalg.norm(vecmember)
                a = evenloads['a'][i]*100
                b = evenloads['b'][i]*100
                avect = a*univecmember
                bvect = b*univecmember
                pointstart = [avect[k]+self.GraphNodes[nodes[0]][k] for k in range(3)]
                pointstart_end = self.convert3Dto2D(pointstart)
                pointstop = [self.GraphNodes[nodes[1]][k] - bvect[k] for k in range(3)]
                pointstop_end = self.convert3Dto2D(pointstop)
                x1 = pointstart_end[0] - vector[0]
                y1 = pointstart_end[1] - vector[1]
    #                pointstart_start = [x1, y1]
                x2 = pointstop_end[0] - vector[0]
                y2 = pointstop_end[1] - vector[1]
    #                pointstop_start = [x2, y2]
                load = QtWidgets.QGraphicsPolygonItem(QtGui.QPolygonF([QtCore.QPointF(x1,y1),QtCore.QPointF(pointstart_end[0], pointstart_end[1]),QtCore.QPointF(pointstop_end[0], pointstop_end[1]),QtCore.QPointF(x2,y2)]))
                load.setPen(QtGui.QPen(self.red,length/100))
                brush = QtGui.QBrush(self.red, QtCore.Qt.SolidPattern)
                load.setBrush(brush)
                load.setOpacity(0.4)
                self.scene.addItem(load)
        except:
            pass
        try:
            for i in range(len(triangloads)):
                nodes = (triangloads['nodestart'][i],triangloads['nodestop'][i])
                if vector[0]==0:
                    ascending=True
                    vector = self.convert3Dto2D(triangloads['vector'][i][1])
                else:
                    ascending=False
                    vector = self.convert3Dto2D(triangloads['vector'][i][0])
                try:
                    vecmember = np.array([self.GraphNodes[nodes[1]][j] - self.GraphNodes[nodes[0]][j] for j in range(3)])
                except:
                    return
                univecmember = vecmember/np.linalg.norm(vecmember)
                a = triangloads['a'][i]*100
                b = triangloads['b'][i]*100
                avect = a*univecmember
                bvect = b*univecmember
                
                pointstart = [avect[k]+self.GraphNodes[nodes[0]][k] for k in range(3)]
                pointstart_end = self.convert3Dto2D(pointstart)
                pointstop = [self.GraphNodes[nodes[1]][k] - bvect[k] for k in range(3)]
                pointstop_end = self.convert3Dto2D(pointstop)
                
                if ascending:
                    x1 = pointstop_end[0] - vector[0]
                    y1 = pointstop_end[1] - vector[1]
    #                pointstop_start = [x1, y1]
                    load = QtWidgets.QGraphicsPolygonItem(QtGui.QPolygonF([QtCore.QPointF(x1,y1),QtCore.QPointF(pointstart_end[0], pointstart_end[1]),QtCore.QPointF(pointstop_end[0], pointstop_end[1])]))
                elif not ascending:
                    x1 = pointstart_end[0] - vector[0]
                    y1 = pointstart_end[1] - vector[1]
    #                pointstart_start = [x1, y1]
                    load = QtWidgets.QGraphicsPolygonItem(QtGui.QPolygonF([QtCore.QPointF(x1,y1),QtCore.QPointF(pointstart_end[0], pointstart_end[1]),QtCore.QPointF(pointstop_end[0], pointstop_end[1])]))
    
                load.setPen(QtGui.QPen(self.red,length/100))
                brush = QtGui.QBrush(self.red, QtCore.Qt.SolidPattern)
                load.setBrush(brush)
                load.setOpacity(0.4)
                self.scene.addItem(load)
        except:
            pass
        try:
            for i in range(len(trapezloads)):
                nodes = (trapezloads['nodestart'][i],trapezloads['nodestop'][i])
                vectorstart = self.convert3Dto2D(trapezloads['vector'][i][0])
                vectorstop = self.convert3Dto2D(trapezloads['vector'][i][1])
                try:
                    vecmember = np.array([self.GraphNodes[nodes[1]][j] - self.GraphNodes[nodes[0]][j] for j in range(3)])
                except:
                    return
                univecmember = vecmember/np.linalg.norm(vecmember)
                a = trapezloads['a'][i]*100
                b = trapezloads['b'][i]*100
                avect = a*univecmember
                bvect = b*univecmember
                pointstart = [avect[k]+self.GraphNodes[nodes[0]][k] for k in range(3)]
                pointstart_end = self.convert3Dto2D(pointstart)
                pointstop = [self.GraphNodes[nodes[1]][k] - bvect[k] for k in range(3)]
                pointstop_end = self.convert3Dto2D(pointstop)
                x1 = pointstart_end[0] - vectorstart[0]
                y1 = pointstart_end[1] - vectorstart[1]
    #                pointstart_start = [x1, y1]
                x2 = pointstop_end[0] - vectorstop[0]
                y2 = pointstop_end[1] - vectorstop[1]
    #                pointstop_start = [x2, y2]
                load = QtWidgets.QGraphicsPolygonItem(QtGui.QPolygonF([QtCore.QPointF(x1,y1),QtCore.QPointF(pointstart_end[0], pointstart_end[1]),QtCore.QPointF(pointstop_end[0], pointstop_end[1]),QtCore.QPointF(x2,y2)]))
                load.setPen(QtGui.QPen(self.red,length/100))
                brush = QtGui.QBrush(self.red, QtCore.Qt.SolidPattern)
                load.setBrush(brush)
                load.setOpacity(0.4)
                self.scene.addItem(load)
        except:
            pass

        

    def deleteBeam(self,name):
        nodes = self.GraphBeams[name]
        del self.GraphBeams[name]
        del self.GRAPHBEAMS[name]
        othernodes = []
        for node in self.GraphBeams.values():
            othernodes.append(node[0])
            othernodes.append(node[1])
        for nod in nodes:
            if nod not in othernodes:
                del self.GraphNodes[nod]
        self.drawStructure()
        


    def drawAxes(self, view):
        for name in self.Axes.keys():
            start3d = self.Axes[name][0]
            stop3d = self.Axes[name][1]
            start3d = self.AxeNodes[start3d]
            stop3d = self.AxeNodes[stop3d]
            if view=='default':
                startx, starty = self.convert3Dto2D(start3d)
                stopx, stopy = self.convert3Dto2D(stop3d)
            elif view=='XZ':
                startx, starty = self.XZconvert3Dto2D(start3d)
                stopx, stopy = self.XZconvert3Dto2D(stop3d)
            elif view=='YZ':
                startx, starty = self.YZconvert3Dto2D(start3d)
                stopx, stopy = self.YZconvert3Dto2D(stop3d)
            elif view=='XY':
                startx, starty = self.XYconvert3Dto2D(start3d)
                stopx, stopy = self.XYconvert3Dto2D(stop3d)
            item = QtWidgets.QGraphicsLineItem()
            item.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
            item.setPen(QtGui.QPen(QtGui.QColor(0,0,0),self.axis_width))
            item.setLine(startx, starty, stopx, stopy)
#            item.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
            self.GRAPHAXES[name]=item
            self.scene.addItem(item)
        self.drawAxeCenter()
        self.placeAxes()
        
        
    def drawAxeCenter(self):
        if self.axis_width<10:
            self.axis_width=5
        item = QtWidgets.QGraphicsEllipseItem((-1)*self.axis_width//2,(-1)*self.axis_width//2,self.axis_width,self.axis_width)
        item.setPen(QtGui.QPen(self.black))
        brush = QtGui.QBrush()
        brush.setColor(self.black)
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBrush(brush)
        self.GRAPHAXES['center']=item
        self.scene.addItem(item)


    def placeAxes(self):
        axescenter = self.mapToScene(40,380)
        for name,axe in self.GRAPHAXES.items():
            axe.setPos(axescenter)
            axe.setPen(QtGui.QPen(self.axecolors[name], self.axis_width))
      
        
    def findCentre(self):
        """ Find the centre of the wireframe. """
        num_nodes = len(self.GraphNodes)
        if num_nodes!=0:
            meanX = sum([value[0] for value in self.GraphNodes.values()]) / num_nodes
            meanY = sum([value[1] for value in self.GraphNodes.values()]) / num_nodes
            meanZ = sum([value[2] for value in self.GraphNodes.values()]) / num_nodes
        else:
            return
        return (meanX, meanY, meanZ)


    def rotateZ(self, cx_cy_cz, radians):
        if cx_cy_cz!=None:
            cx, cy, cz=cx_cy_cz
        else: return
        for name,node in self.GraphNodes.items():
            newnode =[]
            y      = node[1] - cy
            x      = node[0] - cx
            d      = np.hypot(y, x)
            theta  = np.arctan2(y, x) + radians
            newnode.append(cx + d * np.cos(theta))
            newnode.append(cy + d * np.sin(theta))
            newnode.append(node[2])
            self.GraphNodes[name] = newnode
        for name,node in self.AxeNodes.items():
            newnode =[]
            y      = node[1]
            x      = node[0]
            d      = np.hypot(y, x)
            theta  = np.arctan2(y, x) + radians
            newnode.append(d * np.cos(theta))
            newnode.append(d * np.sin(theta))
            newnode.append(node[2])
            self.AxeNodes[name] = newnode
        self.rotateStructure()

    def rotateX(self, cx_cy_cz, radians):
        if cx_cy_cz!=None:
            cx, cy, cz=cx_cy_cz
        else: return
        for name,node in self.GraphNodes.items():
            newnode =[]
            y      = node[1] - cy
            z      = node[2] - cz
            d      = np.hypot(y, z)
            theta  = np.arctan2(y, z) + radians
            newnode.append(node[0])
            newnode.append(cy + d * np.sin(theta))
            newnode.append(cz + d * np.cos(theta))
            self.GraphNodes[name] = newnode
        for name,node in self.AxeNodes.items():
            newnode =[]
            y      = node[1]
            z      = node[2]
            d      = np.hypot(y, z)
            theta  = np.arctan2(y, z) + radians
            newnode.append(node[0])
            newnode.append(d * np.sin(theta))
            newnode.append(d * np.cos(theta))
            self.AxeNodes[name] = newnode
        self.rotateStructure()


    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Z:
            self.rotateZ(self.findCentre(),0.05)
        elif event.key() == QtCore.Qt.Key_X:
            self.rotateZ(self.findCentre(),-0.05)
        elif event.key() == QtCore.Qt.Key_A:
            self.rotateX(self.findCentre(),0.05)
        elif event.key() == QtCore.Qt.Key_S:
            self.rotateX(self.findCentre(),-0.05)


    def convert3Dto2D(self,coords):
        x,y,z=coords[0],coords[1],coords[2]
        x = x * np.cos(np.pi*20/180) + y * np.cos(np.pi*140/180)
        y = x * np.sin(np.pi*20/180) + y * np.sin(np.pi*(180-140)/180) + z
        return x, -y 


#    def convert3Dto2D(self,coords):
#        c = np.array(coords)
#        sx=sz = 2
#        cx=cz = 2
#        xy = np.dot(np.array([[sx,0.25,0],[0,0.25,sz]]),c) + np.array([cx,cz])
#        return xy[0], -xy[1] 


    def XZconvert3Dto2D(self,coords):
        c = np.array(coords)
        sx=sz = 1
        cx=cz = 2
        xy = np.dot(np.array([[sx,0,0],[0,0,sz]]),c) + np.array([cx,cz])
        return xy[0], -xy[1] 
    
    
    def YZconvert3Dto2D(self,coords):
        c = np.array(coords)
        sy=sz = 1
        cx=cz = 2
        xy = np.dot(np.array([[0,sy,0],[0,0,sz]]),c) + np.array([cx,cz])
        return xy[0], -xy[1] 
    
    def XYconvert3Dto2D(self,coords):
        c = np.array(coords)
        sx=sy = 1
        cx=cz = 2
        xy = np.dot(np.array([[sx,0,0],[0,sy,0]]),c) + np.array([cx,cz])
        return xy[0], -xy[1] 


class AnalysisWindow(QtWidgets.QDialog):
    def __init__(self,projectname):
        super(AnalysisWindow,self).__init__()
        self.name = projectname
        self.setWindowIcon(QtGui.QIcon("Pyrforos.ico"))
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        onlyPosFloat = QPosFloatValidator()        
        frame1 = QtWidgets.QFrame(self)
        frame2 = QtWidgets.QFrame(self)
        frame3 = QtWidgets.QFrame(self)
        self.resultlist = QtWidgets.QListWidget(self)
        frame4 = QtWidgets.QFrame(self)
#        labelselfloads = QtWidgets.QLabel('Check the box below\nif you want to include\nself loads in the calculation',self)
        self.checkSelfLoads = QtWidgets.QCheckBox('Check the box to include\nself loads of members\nin the calculation',frame2)
        labelG = QtWidgets.QLabel('Factor for G loads',frame1)
        self.Gfactor = QtWidgets.QLineEdit(frame1)
        labelQ = QtWidgets.QLabel('Factor for Q loads',frame1)
        self.Qfactor = QtWidgets.QLineEdit(frame1)
        self.resultopen = QtWidgets.QCheckBox('Open results file',frame3)
        self.resultopen.setChecked(True)
        self.resultsave = QtWidgets.QCheckBox('Save results automatically',frame3)
        self.resultsave.setChecked(True)
        self.btncalculate = QtWidgets.QPushButton('Analysis',frame4)
        for line in [self.Gfactor, self.Qfactor]:
            line.setValidator(onlyPosFloat)
        gridframe1 = QtWidgets.QGridLayout(frame1)
        gridframe1.addWidget(labelG,0,0,1,1)
        gridframe1.addWidget(self.Gfactor,0,1,1,1)
        gridframe1.addWidget(labelQ,1,0,1,1)
        gridframe1.addWidget(self.Qfactor,1,1,1,1)
        gridframe2 = QtWidgets.QGridLayout(frame2)
#        gridframe2.addWidget(labelselfloads,0,0,1,1)
        gridframe2.addWidget(self.checkSelfLoads,1,0,1,1)
        gridframe3 = QtWidgets.QGridLayout(frame3)
        gridframe3.addWidget(self.resultopen,0,0,1,1)
        gridframe3.addWidget(self.resultsave,1,0,1,1)
        gridframe4 = QtWidgets.QGridLayout(frame4)
        gridframe4.addWidget(self.btncalculate,0,1,1,1)
        for i in [0,1,2]:
            gridframe4.setColumnStretch(i,1)
        gridframe5 = QtWidgets.QGridLayout(frame4)
        for i in [0,1,2]:
            gridframe5.setColumnStretch(i,1)
        gridLayout = QtWidgets.QGridLayout(self)
        gridLayout.addWidget(frame1,0,0,1,1)
        gridLayout.addWidget(frame2,0,1,1,1)
        gridLayout.addWidget(frame3,0,2,1,1)
        gridLayout.addWidget(self.resultlist,2,0,1,3)
        gridLayout.addWidget(frame4,1,0,1,3)
        gridLayout.setRowStretch(0,8)
        gridLayout.setRowStretch(1,1)
        gridLayout.setRowStretch(2,3)
        filename = self.name[:-4] + '_results'
        for i in range(1,81):
            if os.path.isfile('{}{}.txt'.format(filename,str(i))):
                thisfile = '{}{}.txt'.format(filename,str(i))
                self.resultlist.addItem(thisfile)
        self.btncalculate.clicked.connect(self.analysis)
        self.center()



    def analysis(self):
        if self.save()==False:
            return
        gfactor = 1 if self.Gfactor.text()=='' else float(self.Gfactor.text())
        qfactor = 1 if self.Qfactor.text()=='' else float(self.Qfactor.text())
        sl = self.checkSelfLoads.isChecked()
        EdgeForces, IntForces, Disps, Reacts = analyze.analysis(gfactor, qfactor, sl)
        ro = self.resultopen.isChecked()
        rs = self.resultsave.isChecked()
        filename = self.name[:-4] + '_results'
        if rs:
            for i in range(1,81):
                if not os.path.isfile('{}{}.txt'.format(filename,str(i))):
                    self.saveResults(EdgeForces, IntForces, Reacts, Disps, '{}{}.txt'.format(filename,str(i)), gfactor, qfactor, sl)
                    thisfile = '{}{}.txt'.format(filename,str(i))
                    break
        if ro:
            osCommandString = "notepad.exe {}".format(thisfile)
            os.system(osCommandString)

        

    def saveResults(self, EdgeForces,  IntForces, Reacts, disps, filename, gfactor, qfactor, sl):
        vals = ['Qx','Qy','Qz','Mx','My','Mz']
        Disps = self.returnDisplacements(disps)
        with open(filename,'w') as file:
            file.write('\n\nFactor for G loads: {}\n'.format(gfactor))
            file.write('Factor for Q loads: {}\n\n'.format(qfactor))
            if sl:
                file.write('Self loads are included\n\n')
            else:
                file.write('Self loads are not included\n\n')
            file.write('Displacements of nodes (in mm and 0.001*rad):\n')
            for node, disp in Disps.items():
                file.write('Node {}: {}\n'.format(node, disp))
            file.write('\nReactions:\n')
            for react, value in Reacts.items():
                file.write('{} is {}\n'.format(react,value))
            file.write('\n\n')
            file.write('Edge forces of mebers for starting and ending node\n\n')
            for member, forces in EdgeForces.items():
                forces = [str(round(i,3)) for i in forces]
                startF = '{}, {}, {}, {}, {}, {}'.format(forces[0], forces[1], forces[2], forces[3], forces[4], forces[5])
                stopF = '{}, {}, {}, {}, {}, {}'.format(forces[6], forces[7], forces[8], forces[9], forces[10], forces[11])
                file.write('Member {}: starting node: {}, ending node: {} \n'.format(member, startF, stopF))
            file.write('\n\n')
            for member in IntForces.keys():
                file.write('Internal Forces of member: {}             \n'.format(member))
                for i,lval in enumerate(IntForces[member]):
                    file.write('{}                             \n{}\n#\n'.format(vals[i],str(lval)))
                file.write('\n\n')
   
    
    def returnDisplacements(self, disps):
        disps = [round(i*1000,3) for i in disps]
        supports = model.Beam.NodalSupports
        nodes = sorted(supports.keys(), key = lambda x: int(x[1:]))
        dispdict = {}
        for i,node in enumerate(nodes):
            dispdict[node]=disps[i*6:(i+1)*6]
        return dispdict

    
    def save(self):
        filename = self.name
        if os.path.isfile(filename):
            try:
                os.remove(filename)
                self.saveProject(filename)
            except:
                self.singleEvent('', 'Could not save this project.\nCheck if the file {} is already opened with another program.'.format(filename))
                return False
        else:
            self.saveProject(filename)


    def saveProject(self, filename):
        column_names = ['ITEM', 'GRname' ,'GRdata' ,'NOname', 'coords', 'BEname', 'start','start_node', 'stop', 'stop_node', 'theta', 'Bgroup' ,'SUPname' ,'support' ,'RSUPname' ,'angles' , 'DISPname', 'disps', 'ELNOname' ,'stiffness' ,'node','member','function','a','b','group','nodestart','loadsstart','nodestop','loadsstop','loadsstart_release','self_load']
        df = pd.DataFrame(columns = column_names)
        BEAMS = model.Beam.Beams
        NODES = model.Beam.Nodes
        NODESUPPORTS = model.Beam.NodalSupports
        ROTSUPPORTS = model.Beam.RotatedSupports
        DISPLACEMENTS = model.Beam.Displacements
        ELASTNODE = model.Beam.ElasticNode
        RIGIDNODE = model.Beam.RigidNode
        LOADS = model.Beam.Loads
        GROUPS = model.Beam.Groups
        RELS = {}
        for beam in BEAMS.values():
            df = df.append({'ITEM':'BEAM','BEname':beam.name , 'start':list(beam.start), 'start_node':beam.start_node, 'stop':list(beam.stop), 'stop_node': beam.stop_node, 'theta':beam.theta, 'Bgroup':beam.group}, ignore_index=True)
        for node,coords in NODES.items():
            df = df.append({'ITEM':'NODE','NOname': node,'coords': coords}, ignore_index=True)
        for name, value in NODESUPPORTS.items():
            df = df.append({'ITEM':'SUP','SUPname': name,'support':value}, ignore_index=True)
        for name, value in ROTSUPPORTS.items():
            df = df.append({'ITEM':'ROTSUP','RSUPname': name,'angles':value}, ignore_index=True)
        for name, value in DISPLACEMENTS.items():
            df = df.append({'ITEM':'DISPS','DISPname': name,'disps':value}, ignore_index=True)
        for name, value in ELASTNODE.items():
            df = df.append({'ITEM':'ELNO','ELNOname': name,'stiffness':value}, ignore_index=True)
        for name, value in RIGIDNODE.items():
            df = df.append({'ITEM':'RIGID','RIGname': name,'rigs':value}, ignore_index=True)
        for name,beam in BEAMS.items():
            if beam.release!=None:
                RELS[name] = beam.release
        for name , value in RELS.items():
            df = df.append({'ITEM':'REL','RELname': name,'rels':value}, ignore_index=True)
        for name, value in GROUPS.items():
            df = df.append({'ITEM':'GROUP','GRname': name,'GRdata':value}, ignore_index=True)
        df = df.fillna('None')
        loads = LOADS.loc[:,['loadsstart','loadsstop','loadsstart_release','vector']]
        for col in ['loadsstart','loadsstop','loadsstart_release','vector']:
            LOADS[col]= loads[col]
        LOADS = LOADS.fillna('None')
        df=pd.concat([df,LOADS], axis=0, join='outer', ignore_index=True)
        df = df.fillna('None')
        df.to_csv(filename)

    def singleEvent(self,message,explain):
        mes = QtWidgets.QMessageBox()
        mes.setWindowTitle(message)
        mes.setText(explain)
        mes.setStandardButtons(QtWidgets.QMessageBox.Close)
        style = "background-color: rgb(218, 218, 218);"
        mes.setStyleSheet(style)
        mes.exec()

        
    def center(self):
        qr = self.frameGeometry()
        cs = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cs)
        self.move(qr.topLeft())


class ViewResultsWindow(QtWidgets.QDialog):
    def __init__(self,projectname):
        super(ViewResultsWindow,self).__init__()
        self.name = projectname
        self.setWindowIcon(QtGui.QIcon("Pyrforos.ico"))
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setMinimumWidth(600)
        self.resultlist = QtWidgets.QListWidget(self)
        self.elementslist = QtWidgets.QListWidget(self)
        self.btnplot = QtWidgets.QPushButton('View results',self)
        self.opentxt = QtWidgets.QCheckBox('Open the text file', self)
        gridLayout = QtWidgets.QGridLayout(self)
        gridLayout.addWidget(self.resultlist,0,0,1,3)
        gridLayout.addWidget(self.elementslist,1,0,1,3)
        gridLayout.addWidget(self.btnplot,2,2,1,1)
        gridLayout.addWidget(self.opentxt,2,0,1,1)
        gridLayout.setRowStretch(0,4)
        gridLayout.setRowStretch(1,4)
        gridLayout.setRowStretch(2,1)
        for i in range(3):
            gridLayout.setColumnStretch(i,1)
        filename = self.name[:-4] + '_results'
        
        for i in range(1,81):
            if os.path.isfile('{}{}.txt'.format(filename,str(i))):
                thisfile = '{}{}.txt'.format(filename,str(i))
                self.resultlist.addItem(thisfile)
        for el in model.Beam.Beams.keys():
            self.elementslist.addItem(el)
        self.btnplot.clicked.connect(self.viewResults)
        self.center()


    def viewResults(self):
        file = self.resultlist.currentItem().text()
        if self.opentxt.isChecked():
            osCommandString =  "notepad.exe {}".format(file)
            os.system(osCommandString)
        dfIntForces = self.readFile(file)
        try:
            member = self.elementslist.currentItem().text()
        except:
            return
        elDf = dfIntForces[member]
        
        Qxdf = pd.DataFrame({'Qx':[v for v in elDf.at['Qx']]})
        Qydf = pd.DataFrame({'Qy':[v for v in elDf.at['Qy']]})
        Qzdf = pd.DataFrame({'Qz':[v for v in elDf.at['Qz']]})
        Mxdf = pd.DataFrame({'Mx':[v for v in elDf.at['Mx']]})
        Mydf = pd.DataFrame({'My':[v for v in elDf.at['My']]})
        Mzdf = pd.DataFrame({'Mz':[v for v in elDf.at['Mz']]})
                
        elDf = pd.concat([Qxdf, Qydf, Qzdf, Mxdf, Mydf, Mzdf], axis=1)
        elDf.plot(subplots=True, layout=(2,3),use_index =True, kind='line')
        





    def readFile(self,file):
        index = ['Qx','Qy','Qz','Mx','My','Mz']
        columns = sorted(model.Beam.Beams.keys(), key = lambda x: int(x[2:]))
        dfIntForces = pd.DataFrame(index=index, columns=columns)
        with open(file,'r') as outfile:
            alllines = outfile.readlines()
            for i,line in enumerate(alllines):
                if line[:8]=='Internal':
                    membersname = line[27:36].replace(' ','')
                elif line[:2] in ['Qx','Qy','Qz','Mx','My','Mz']:
                    intforce = line[:2]
                    values = alllines[i+1].replace(' ','')
                    values = values.replace('[','')
                    values = values.replace(']','')
                    values = values.split(',')
                    if values!=['']:
                        values = [float(j.replace(',','')) for j in values]
                    dfIntForces.at[intforce,membersname] = values
        return dfIntForces
                    
                    
        
        
    def center(self):
        qr = self.frameGeometry()
        cs = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cs)
        self.move(qr.topLeft())




def main():
    import sys
    global MAINWINDOW
    MAINWINDOW = QtCore.QCoreApplication.instance()
    if MAINWINDOW is None:
        MAINWINDOW = QtWidgets.QApplication(sys.argv)
    MAINWINDOW.aboutToQuit.connect(MAINWINDOW.deleteLater) 
    splash_pix = QtGui.QPixmap('pyrforos_bw.png')
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    MAINWINDOW.processEvents()
    m=MainWindow()
    m.show()
    splash.hide()
    splash.finish(m)
    
    sys.exit(MAINWINDOW.exec_())  

main()

