###############################################################################
# WidgetCatControl.py
# Author: Tom Kerr AB3GY
#
# WidgetCatControl class for use with the pySatCat application.
# Provides Computer Aided Transceiver (CAT) control through the GUI.
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

# Tkinter packages.
import tkinter as tk
import tkinter.font as tkFont
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
# WidgetCatControl class.
##############################################################################
class WidgetCatControl(object):
    """
    WidgetCatControl class for use with the pySatCat application.
    Provides Computer Aided Transceiver (CAT) control through the GUI.
    """
    # ------------------------------------------------------------------------
    def __init__(self, parent):
        """
        Class constructor.
        
        Parameters
        ----------
        parent : Tk object
            The parent object containing the widget

        Returns
        -------
        None.
        """
        self.parent = parent
        self.frame = tk.Frame(parent,
            highlightbackground="blue",
            highlightthickness=2)
        
        self.is_enabled = False
        self.rig_label_text = tk.StringVar(self.frame)
        self.comm_status_text = tk.StringVar(self.frame)
        self.cat_enable = tk.IntVar(self.frame)

        self.PADX = 6
        self.PADY = 3
        self.RIG_NONE = 'NONE'
        
        self._widget_init()
   
    # ------------------------------------------------------------------------
    def set_comm_status(self, state=False):
        """
        Set the CAT communication status.
        """
        msg = 'Comm: NOT CONNECTED'
        if self.is_enabled:
            if state:
                msg = 'Comm: CONNECTED    '
        self.comm_status_text.set(msg)

    # ------------------------------------------------------------------------
    def set_rig_name(self, name=None):
        """
        Set the rig name.
        """
        if name is None: name = self.RIG_NONE
        self.rig_label_text.set('Rig: ' + str(name))

    # ------------------------------------------------------------------------
    def _enable_ckbx_handler(self):
        """
        Event handler for Enable/Disable checkbox.
        """
        state = self.cat_enable.get()
        if (state == 0):
            self.is_enabled = False
            globals.rig_cat_enabled = False
        else:
            self.is_enabled = True
            globals.rig_cat_enabled = True

    # ------------------------------------------------------------------------
    def _widget_init(self):
        """
        Internal method to create and initialize the UI widget.
        """
        row = 0
        col = 0
        
        # CAT rig label.
        self.set_rig_name(self.RIG_NONE)
        lbl = tk.Label(self.frame, 
            textvariable=self.rig_label_text,
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=col,
            sticky='W',
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        # CAT communication status label.
        self.set_comm_status(False)
        lbl = tk.Label(self.frame, 
            textvariable=self.comm_status_text,
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=col,
            sticky='EW',
            padx=self.PADX,
            pady=self.PADY)
        col += 1

        # Enable/disable checkbox.
        ckbx = tk.Checkbutton(self.frame, 
            text='Enable',
            variable=self.cat_enable,
            command=self._enable_ckbx_handler,
            onvalue = 1, 
            offvalue = 0,
            font=tkFont.Font(size=10))
        ckbx.grid(
            row=row,
            column=col,
            sticky='E',
            padx=self.PADX,
            pady=self.PADY)
        col+= 1
        
        self.cat_enable.set(0)
        self._enable_ckbx_handler()


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('WidgetCatControl main program not implemented.')
   