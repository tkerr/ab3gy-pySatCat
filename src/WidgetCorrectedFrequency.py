###############################################################################
# WidgetCorrectedFrequency.py
# Author: Tom Kerr AB3GY
#
# WidgetCorrectedFrequency class for use with the pySatCat application.
# Provides the Doppler Corrected Frequency GUI widget.
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
# WidgetCorrectedFrequency class.
##############################################################################
class WidgetCorrectedFrequency(object):
    """
    WidgetCorrectedFrequency class for use with the pySatCat application.
    Implements the Doppler Corrected Frequency GUI widget.
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
        
        # Text entry variables.
        self.uplink_text = tk.StringVar(self.frame)
        self.downlink_text = tk.StringVar(self.frame)
        
        # Text entry widgets.
        self.tb_uplink = None
        self.tb_downlink = None
        
        # Checkbox variables.
        self.ck_uplink_enable = tk.IntVar(self.frame)
        self.ck_downlink_enable = tk.IntVar(self.frame)
        
        self.PADX = 3
        self.PADY = 3
        
        self._widget_init()

    # ------------------------------------------------------------------------
    def clear(self):
        """
        Clear all text entry fields.
        """
        self.uplink_text.set('0.000')
        self.downlink_text.set('0.000')
        self.ck_uplink_enable.set(0)
        self.ck_downlink_enable.set(0)

    # ------------------------------------------------------------------------
    def set_uplink(self, freq):
        """
        Set the corrected uplink frequency.
        """
        freq_str = ('%0.6f' % freq)
        self.uplink_text.set(freq_str)

    # ------------------------------------------------------------------------
    def set_uplink_corrected_enable(self, val):
        """
        Set/clear the uplink corrected frequency enable checkbox
        val: 0 = unchecked, 1 = checked
        """
        ctrl = to_int(val)
        if (ctrl != 0): ctrl = 1
        self.ck_uplink_enable.set(ctrl)
        globals.rig_cat_uplink_enabled = (ctrl == 1)
    
    # ------------------------------------------------------------------------
    def set_downlink(self, freq):
        """
        Set the corrected downlink frequency.
        """
        freq_str = ('%0.6f' % freq)
        self.downlink_text.set(freq_str)
    
    # ------------------------------------------------------------------------
    def set_downlink_corrected_enable(self, val):
        """
        Set/clear the downlink corrected frequency enable checkbox
        val: 0 = unchecked, 1 = checked
        """
        ctrl = to_int(val)
        if (ctrl != 0): ctrl = 1
        self.ck_downlink_enable.set(ctrl)
        globals.rig_cat_downlink_enabled = (ctrl == 1)
    
    # ------------------------------------------------------------------------
    def _widget_init(self):
        """
        Internal method to create and initialize the UI widget.
        """
        self.clear()
        
        lbl = tk.Label(self.frame, 
            text='Corrected Frequency (MHz)', 
            font=tkFont.Font(size=10))
        lbl.grid(
            row=0, 
            column=0,
            columnspan=3,
            padx=self.PADX,
            pady=self.PADY)
            
        lbl = tk.Label(self.frame, 
            text='Uplink: ', 
            font=tkFont.Font(size=10))
        lbl.grid(
            row=1, 
            column=0,  
            sticky='W', 
            padx=self.PADX,
            pady=self.PADY)
        
        self.tb_uplink = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=12,
            textvariable=self.uplink_text,
            font=tkFont.Font(size=10))
        self.tb_uplink.grid(
            row=1, 
            column=1,
            sticky='W',
            padx=(0, self.PADX), 
            pady=self.PADY)
        
        ckbx = tk.Checkbutton(self.frame, 
            text='Enable',
            variable=self.ck_uplink_enable,
            command=self._ck_uplink_handler,
            onvalue = 1, 
            offvalue = 0)
        ckbx.grid(
            row=1, 
            column=2,
            sticky='W',
            padx=self.PADX, 
            pady=0)
        
        lbl = tk.Label(self.frame,
            text='Downlink: ', 
            font=tkFont.Font(size=10))
        lbl.grid(
            row=2, 
            column=0,  
            sticky='W',
            padx=self.PADX, 
            pady=self.PADY)
        
        self.tb_downlink = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=12,
            textvariable=self.downlink_text,
            font=tkFont.Font(size=10))
        self.tb_downlink.grid(
            row=2, 
            column=1,
            sticky='W',
            padx=(0, self.PADX), 
            pady=self.PADY)
        
        ckbx = tk.Checkbutton(self.frame, 
            text='Enable',
            variable=self.ck_downlink_enable,
            command=self._ck_downlink_handler,
            onvalue = 1, 
            offvalue = 0)
        ckbx.grid(
            row=2, 
            column=2,
            sticky='W',
            padx=self.PADX, 
            pady=0)

    # ------------------------------------------------------------------------
    def _ck_uplink_handler(self):
        """
        Uplink corrected frequency enable checkbox handler.
        """
        ctrl = self.ck_uplink_enable.get()
        globals.rig_cat_uplink_enabled = (ctrl == 1)

    # ------------------------------------------------------------------------
    def _ck_downlink_handler(self):
        """
        Downlink corrected frequency enable checkbox handler.
        """
        ctrl = self.ck_downlink_enable.get()
        globals.rig_cat_downlink_enabled = (ctrl == 1)


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('WidgetCorrectedFrequency main program not implemented.')
   