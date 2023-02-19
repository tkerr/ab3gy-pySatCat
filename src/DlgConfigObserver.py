###############################################################################
# DlgConfigObserver.py
# Author: Tom Kerr AB3GY
#
# DlgConfigObserver class for use with the pySatCat application.
# Implements a dialog box for selecting observer location.
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
import os
import re
import sys

# Tkinter packages.
import tkinter as tk
from tkinter import ttk

# Local packages.
import globals
from src.pySatCatUtils import *

##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################


##############################################################################
# DlgConfigObserver class.
##############################################################################
class DlgConfigObserver(object):
    """
    DlgConfigObserver class for use with the pySatCat application.
    Implements a dialog box for selecting observer location.
    """

    # ------------------------------------------------------------------------
    def __init__(self, root):
        """
        Class constructor.
    
        Parameters
        ----------
        root : Tk object
            The pySatCat application root window.
        
        Returns
        -------
        None.
        """
        self.root = root                 # The root window
        self.dlg_config_observer = None  # The dialog box
        self.section = 'OBSERVER'        # Config file section
        
        # Text entry variables.
        self.lat_text = tk.StringVar(self.root)
        self.lon_text = tk.StringVar(self.root)
        self.alt_text = tk.StringVar(self.root)

        self._dlg_init()

    # ------------------------------------------------------------------------
    def _dlg_init(self):
        """
        Internal method to create and initialize the dialog box.
        """
        self.dlg_config_observer = tk.Toplevel(self.root)
        self.dlg_config_observer.title('Observer Configuration')

        # Text box labels.
        ttk.Label(self.dlg_config_observer, text='Latitude:  ').grid(row=0, column=0, padx=3, pady=6, sticky='EW')
        ttk.Label(self.dlg_config_observer, text='Longitude: ').grid(row=1, column=0, padx=3, pady=6, sticky='EW')
        ttk.Label(self.dlg_config_observer, text='Altitude:  ').grid(row=2, column=0, padx=3, pady=6, sticky='EW')

        validateNumberCommand = self.dlg_config_observer.register(self._validate_number)

        # Latitude entry box.
        self.lat_text.set(globals.config.get(self.section, 'LAT'))
        tb_lat = ttk.Entry(self.dlg_config_observer, 
            textvariable=self.lat_text, 
            validate='key', 
            validatecommand=(validateNumberCommand, '%d', '%i', '%S', '%P'))
        tb_lat.grid(row=0, column=1, padx=6, sticky='EW')
        
        # Longitude entry box.
        self.lon_text.set(globals.config.get(self.section, 'LON'))
        tb_lon = ttk.Entry(self.dlg_config_observer, 
            textvariable=self.lon_text, 
            validate='key', 
            validatecommand=(validateNumberCommand, '%d', '%i', '%S', '%P'))
        tb_lon.grid(row=1, column=1, padx=6, sticky='EW')
        
        # Altitude entry box.
        self.alt_text.set(globals.config.get(self.section, 'ALT'))
        tb_alt = ttk.Entry(self.dlg_config_observer, 
            textvariable=self.alt_text, 
            validate='key', 
            validatecommand=(validateNumberCommand, '%d', '%i', '%S', '%P'))
        tb_alt.grid(row=2, column=1, padx=6, sticky='EW')
        
        # OK button.
        btn_ok = tk.Button(self.dlg_config_observer, 
            text='OK', 
            width=10, 
            command=self._dlg_config_observer_ok)
        btn_ok.grid(row=3, column=1, padx=6, pady=6)
        
        # Cancel button.
        btn_cancel = tk.Button(self.dlg_config_observer, 
            text='Cancel', 
            width=10, 
            command=self.dlg_config_observer.destroy)
        btn_cancel.grid(row=3, column=2, padx=6, pady=6)
    
        tb_lat.focus_set()
        self.dlg_config_observer.grab_set() # Make the dialog modal
        
        # Set the proper window size and center it on the screen.
        set_geometry(self.dlg_config_observer)

    # ------------------------------------------------------------------------
    def _dlg_config_observer_ok(self):
        """
        Dialog box OK button handler.
        """
        if not globals.config.has_section(self.section):
            globals.config.add_section(self.section)
        globals.config.set(self.section, 'LAT', self.lat_text.get())
        globals.config.set(self.section, 'LON', self.lon_text.get())
        globals.config.set(self.section, 'ALT', self.alt_text.get())
        
        # Save parameters to .INI file.
        globals.config.write()
        
        # Update the satellite observer.
        update_location()

        self.dlg_config_observer.destroy()

    # ------------------------------------------------------------------------
    def _validate_number(self, why, where, what, all):
        """
        Validate numeric entries.

        Parameters
        ----------
            why : int
                Action code: 0 for an attempted deletion, 1 for an attempted 
                insertion, or -1 for everything else.
            where : int
                Index of the beginning of the insertion or deletion.
            what : str
                The text being inserted or deleted.
            all : str
                The value that the text will have if the change is allowed. 
        Returns
        -------
            status : bool
                True if the character string is allowable, False otherwise.
                The text entry box will accept the character if True, or reject it if False.
        """
        #print(str(why), str(where), str(what), str(all))
        idx = int(where)
        if (why != '1'): return True         # 1 = insertion
        if (len(all) > 12): return False     # Limit entry length
        if what.isnumeric(): return True
        if (what == '+') or (what == '-'):
            if (idx != 0): return False      # Must be first character
            if '+' in all[1:]: return False  # Only one occurrence allowed
            if '-' in all[1:]: return False  # Only one occurrence allowed
            return True
        if (what == '.'):
            if '.' in all[:idx]: return False # Only one occurrence allowed
            return True
        return False  # Nothing else allowed


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('DlgConfigObserver main program not implemented.')
