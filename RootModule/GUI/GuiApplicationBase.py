# -*- coding: utf-8 -*-

####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) Fabrice Salvaire 2013 
# 
####################################################################################################

###################################################################################################
#
# If an exception is raise before application.exec then application exit.
#
####################################################################################################

####################################################################################################

import logging
import sys
import traceback

from PyQt4 import QtGui, QtCore

####################################################################################################

from .CriticalErrorForm import CriticalErrorForm
from .EmailBugForm import EmailBugForm
from RootModule.Application.ApplicationBase import ApplicationBase
import RootModule.Config.Config as Config
import RootModule.Config.Messages as Messages
import RootModule.Version as Version

# Load RC
#import .ui.babel_rc

####################################################################################################

class GuiApplicationBase(ApplicationBase, QtGui.QApplication):

    _logger = logging.getLogger(__name__)

    has_gui = True
    
    ##############################################
    
    def __init__(self, args, **kwargs):

        super(GuiApplicationBase, self).__init__(args=args, **kwargs)
        # Fixme: Why ?
        self._logger.debug("QtGui.QApplication " + str(sys.argv))
        QtGui.QApplication.__init__(self, sys.argv)
        self._logger.debug('GuiApplicationBase ' + str(args) + ' ' + str(kwargs))

        self._display_splash_screen()

        self._main_window = None
        self._init_actions()

    ##############################################

    @property
    def main_window(self):
        return self._main_window

    ##############################################

    def _exception_hook(self, exception_type, exception_value, exception_traceback):

        traceback.print_exception(exception_type, exception_value, exception_traceback)
        dialog = CriticalErrorForm(exception_type, exception_value, exception_traceback)
        dialog.exec_()

        # return sys.__excepthook__(exception_type, exception_value, exception_traceback)

    ##############################################

    def _display_splash_screen(self):

        pixmap = QtGui.QPixmap(':/splash screen/images/splash_screen.png')
        self._splash = QtGui.QSplashScreen(pixmap)
        self._splash.show()
        self._splash.showMessage('<h2>RootModule %(version)s</h2>' % {'version':str(Version.babel)})
        self.processEvents()

    ##############################################

    def _init_actions(self):

        self.about_action = \
            QtGui.QAction('About RootModule',
                          self,
                          triggered=self.about)

        self.exit_action = \
            QtGui.QAction('Exit',
                          self,
                          triggered=self.exit)

        self.help_action = \
            QtGui.QAction('Help',
                          self,
                          triggered=self.open_help)

        self.show_system_information_action = \
            QtGui.QAction('System Information',
                          self,
                          triggered=self.show_system_information)
        
        self.send_email_action = \
            QtGui.QAction('Send Email',
                          self,
                          triggered=self.send_email)

    ##############################################
    
    def post_init(self):
         
        self._splash.finish(self._main_window)
        self.processEvents()
        del self._splash

        QtCore.QTimer.singleShot(0, self.execute_given_user_script)

        self.show_message('Welcome to RootModule')

        # return to main and then enter to event loop
        
    ##############################################

    def show_message(self, message=None, echo=False, timeout=0):

        if self._main_window is not None:
            self._main_window.show_message(message, echo, timeout)

    ##############################################
    
    # Fixme: CriticalErrorForm vs critical_error

    def critical_error(self, title='RootModule Critical Error', message=''):
        
        QtGui.QMessageBox.critical(None, title, message)
        
        # Fixme: qt close?
        sys.exit(1)

    ##############################################

    def open_help(self):

        url = QtCore.QUrl()
        url.setScheme(Config.Help.url_scheme)
        url.setHost(Config.Help.host)
        url.setPath(Config.Help.url_path_pattern) # % str(Version.babel))
        QtGui.QDesktopServices.openUrl(url)

    ##############################################

    def about(self):
        
        message = Messages.about_babel % {'version':str(Version.babel)}
        QtGui.QMessageBox.about(self.main_window, 'About RootModule', message)

    ##############################################

    def show_system_information(self):

        fields = dict(self._platform.__dict__)
        fields.update({
                'babel_version': str(Version.babel),
                })  
        message = Messages.system_information_message_pattern % fields
        QtGui.QMessageBox.about(self.main_window, 'System Information', message)

    ###############################################

    def send_email(self):
        
        dialog = EmailBugForm()
        dialog.exec_()
        
####################################################################################################
#
# End
#
####################################################################################################
