###############################################################################
# WidgetDesiredFrequency.py
# Author: Tom Kerr AB3GY
#
# WidgetDesiredFrequency class for use with the pySatCat application.
# Provides the Desired Frequency GUI widget.
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
# WidgetDesiredFrequency class.
##############################################################################
class WidgetDesiredFrequency(object):
    """
    WidgetDesiredFrequency class for use with the pySatCat application.
    Implements the Desired Frequency GUI widget.
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
        globals.rig_cat_uplink_desired = 0.0
        globals.rig_cat_downlink_desired = 0.0
        
    # ------------------------------------------------------------------------        
    def uplink_float(self):
        """
        Return the uplink frequency as a float.
        """
        f = to_float(self.tb_uplink.get())
        return f
    
    # ------------------------------------------------------------------------        
    def downlink_float(self):
        """
        Return the downlink frequency as a float.
        """
        f = to_float(self.tb_downlink.get())
        return f
    
    # ------------------------------------------------------------------------        
    def set_uplink(self, val):
        """
        Set the uplink frequency.
        """
        f = to_float(val)
        self.uplink_text.set('%0.3f' % f)
        globals.rig_cat_uplink_desired = f
    
    # ------------------------------------------------------------------------        
    def set_downlink(self, val):
        """
        Set the downlink frequency.
        """
        f = to_float(val)
        self.downlink_text.set('%0.3f' % f)
        globals.rig_cat_downlink_desired = f

    # ------------------------------------------------------------------------        
    def _validate_frequency(self, why, where, what, all):
        """
        Validate a frequency field.
        Allows up to 10 characters including decimal point.
        
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
        if (why != '1'): return True       # 1 = insertion
        if (len(all) > 10): return False   # Max 10 characters
        if what.isnumeric(): return True   # Only numeric allowed
        if (what == '.'):
            if '.' in all[:idx]: return False # Only one occurrence allowed
            else: return True
        return False
        
    # ------------------------------------------------------------------------
    def _widget_init(self):
        """
        Internal method to create and initialize the UI widget.
        """
        validateFreqCommand = self.frame.register(self._validate_frequency)
        
        self.clear()
        
        lbl = tk.Label(self.frame, 
            text='Desired Frequency (MHz)', 
            font=tkFont.Font(size=10))
        lbl.grid(
            row=0, 
            column=0,
            columnspan=2,
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
            width=12,
            textvariable=self.uplink_text,
            font=tkFont.Font(size=10),
            validate='key', 
            validatecommand=(validateFreqCommand, '%d', '%i', '%S', '%P'))
        self.tb_uplink.grid(
            row=1, 
            column=1,
            sticky='W',
            padx=(0, self.PADX), 
            pady=self.PADY)

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
            width=12,
            textvariable=self.downlink_text,
            font=tkFont.Font(size=10),
            validate='key', 
            validatecommand=(validateFreqCommand, '%d', '%i', '%S', '%P'))
        self.tb_downlink.grid(
            row=2, 
            column=1,
            sticky='W',
            padx=(0, self.PADX), 
            pady=self.PADY)


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('WidgetDesiredFrequency main program not implemented.')
   