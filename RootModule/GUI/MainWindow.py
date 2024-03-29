# -*- coding: utf-8 -*-

####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) Fabrice Salvaire 2013 
# 
####################################################################################################

####################################################################################################

from PyQt4 import QtCore, QtGui

####################################################################################################

from .MainWindowBase import MainWindowBase

####################################################################################################

class MainWindow(MainWindowBase):

    ##############################################

    def __init__(self):

        super(MainWindow, self).__init__(title='RootModule')

        self._init_ui()

    ##############################################

    def init_menu(self):

        super(MainWindow, self).init_menu()

    ##############################################

    def _init_ui(self):

        self.statusBar()

        self._translate_ui()

    ##############################################

    def _translate_ui(self):

        pass
        # self.foo.setText(self.translate("..."))

    ##############################################

    def closeEvent(self, event=None):

        self._application.exit()

####################################################################################################
#
# End
#
####################################################################################################
