###############################################################################
# AppMenu.py
# Author: Tom Kerr AB3GY
#
# AppMenu class for use with the pySatCat application.
# Implements the application menu and associated dialog boxes.
#
# Designed for personal use by the author, but available to anyone under the
# license terms below.
###############################################################################

###############################################################################
# License
# Copyright (c) 2022 Tom Kerr AB3GY (ab3gy@arrl.net).
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,   
# this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,  
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without 
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
###############################################################################

# System level packages.
import sys

# Tkinter packages.
import tkinter as tk
from tkinter import ttk
from tkinter import Menu, filedialog
from tkinter.messagebox import showinfo, showwarning, askyesnocancel

# Local packages.
import globals
from src.pySatCatUtils import *
from src.DlgConfigCat import DlgConfigCat
from src.DlgConfigObserver import DlgConfigObserver
from src.DlgConfigTLE import DlgConfigTLE


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

# ------------------------------------------------------------------------
def about_msg():
    """
    Display a Help -> About message box.
    """
    msg = globals.APP_NAME + ' Version ' + globals.APP_VERSION + '\n'
    msg += 'Transceiver control for satellite operation\n'
    msg += '(c) ' + globals.APP_COPYRIGHT + ' by Tom Kerr AB3GY\n'
    msg += 'ab3gy@arrl.net'
    
    showinfo(
        title='About ' + globals.APP_NAME,
        message=msg)


##############################################################################
# AppMenu class.
##############################################################################
class AppMenu(object):

    # ------------------------------------------------------------------------
    def __init__(self, root):
        """
        Class constructor.
        
        Parameters
        ----------
        root : Tk object
            The potalog application root window.

        Returns
        -------
        None.
        """
        self.root = root
        
        # The application menu.
        self.menubar = Menu(root)
        root.config(menu=self.menubar)
        self._menu_init()

    # ------------------------------------------------------------------------
    def _menu_init(self):
        """
        Internal method to create and initialize the menu.
        """
        
        # Config menu.
        config_menu = Menu(self.menubar, tearoff=False)
        config_menu.add_command(
            label='Observer...',
            command=self._dlg_observer)
        config_menu.add_command(
            label='CAT Interface...',
            command=self._dlg_cat)
        config_menu.add_command(
            label='TLE Source...',
            command=self._dlg_tle)
        self.menubar.add_cascade(
            label='Config',
            menu=config_menu)

        # Help menu.
        help_menu = Menu(self.menubar, tearoff=False)
        help_menu.add_command(
            label='About',
            command=about_msg)
        self.menubar.add_cascade(
            label='Help',
            menu=help_menu)

    # ------------------------------------------------------------------------
    def _dlg_cat(self):
        """
        CAT dialog box for managing the Computer Aided Transceiver (CAT) interface.
        """
        dlg = DlgConfigCat(self.root)
        pass

    # ------------------------------------------------------------------------
    def _dlg_observer(self):
        """
        Observer dialog box for entering location info.
        """
        dlg = DlgConfigObserver(self.root)

    # ------------------------------------------------------------------------
    def _dlg_tle(self):
        """
        TLE dialog box for configuring Two Line Element (TLE) data sources.
        """
        dlg = DlgConfigTLE(self.root)


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    
    print('AppMenu test program not implemented.')

   