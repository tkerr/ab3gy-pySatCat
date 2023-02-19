###############################################################################
# DlgConfigCat.py
# Author: Tom Kerr AB3GY
#
# DlgConfigCat class for use with the pySatCat application.
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
from src.RigCat import update_rig_cat


##############################################################################
# Globals.
##############################################################################

# The list of supported transceivers.
rig_list = (
    'NONE',
    'FT-817',
    'FT-991',
    'IC-7000',
    )

# The list of selectable baud rates.
baud_list = (
    '1200',
    '2400',
    '4800',
    '9600',
    '19200',
    '38400',
    '57600',
    '115200',
)

# The list of selectable data bit sizes.
data_list = (
    '5',
    '6',
    '7',
    '8',
)

# The list of selectable parity types.
parity_list = (
    'NONE',
    'EVEN',
    'ODD',
)

# The list of selectable stop bit sizes.
stop_list = (
    '1',
    '1.5',
    '2',
)


##############################################################################
# Functions.
##############################################################################


##############################################################################
# DlgConfigCat class.
##############################################################################
class DlgConfigCat(object):
    """
    DlgConfigCat class for use with the pySatCat application.
    Implements a dialog box for configuring the Computer Aided Transceiver (CAT)
    interface.
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
        self.root = root            # The root window
        self.dlg_config_cat = None  # The dialog box
        self.section = 'CAT'        # Config file section
        
        # Control variables.
        self.rig_text       = tk.StringVar(self.root)
        self.port_text      = tk.StringVar(self.root)
        self.baud_text      = tk.StringVar(self.root)
        self.parity_text    = tk.StringVar(self.root)
        self.stop_bits_text = tk.StringVar(self.root)
        self.data_bits_text = tk.StringVar(self.root)
        
        self.on_enable_split  = tk.IntVar(self.root)
        self.on_enable_mode   = tk.IntVar(self.root)
        self.on_disable_split = tk.IntVar(self.root)
        self.on_disable_mode  = tk.IntVar(self.root)
        self.on_disable_ctcss = tk.IntVar(self.root)

        self._dlg_init()

    # ------------------------------------------------------------------------
    def _dlg_init(self):
        """
        Internal method to create and initialize the dialog box.
        """
        global rig_list
        global baud_list
        global data_list
        global parity_list
        global stop_list
        
        # Initialize parameters.
        
        # Build the list of serial ports on this machine.
        port_list = ['NONE']
        serial_list = get_serial_ports()
        for s in serial_list:
            port_list.append(s)
        
        # Get existing config settings.
        rig = str(globals.config.get(self.section, 'RIG'))
        if (len(rig) > 0): self.rig_text.set(rig)
        else: self.rig_text.set(rig_list[0])
        
        port = str(globals.config.get(self.section, 'PORT'))
        if (len(port) > 0): self.port_text.set(port)
        else: self.port_text.set(port_list[0])
        
        self.baud_text.set(str(globals.config.get(self.section, 'BAUD')))
        
        data = str(globals.config.get(self.section, 'DATA'))
        if (len(data) > 0): self.data_bits_text.set(data)
        else: self.data_bits_text.set('8')
        
        parity = str(globals.config.get(self.section, 'PARITY'))
        if (len(parity) > 0): self.parity_text.set(parity)
        else: self.parity_text.set('NONE')
        
        stop = str(globals.config.get(self.section, 'STOP'))
        if (len(stop) > 0): self.stop_bits_text.set(stop)
        else: self.stop_bits_text.set('1')
        
        ena_split = str(globals.config.get(self.section, 'ON_ENABLE_SPLIT'))
        if (len(ena_split) > 0): self.on_enable_split.set(int(ena_split))
        else: self.on_enable_split.set(1)
        
        ena_mode = str(globals.config.get(self.section, 'ON_ENABLE_MODE'))
        if (len(ena_mode) > 0): self.on_enable_mode.set(int(ena_mode))
        else: self.on_enable_mode.set(1)
        
        dis_split = str(globals.config.get(self.section, 'ON_DISABLE_SPLIT'))
        if (len(dis_split) > 0): self.on_disable_split.set(int(dis_split))
        else: self.on_disable_split.set(1)
        
        dis_mode = str(globals.config.get(self.section, 'ON_DISABLE_MODE'))
        if (len(dis_mode) > 0): self.on_disable_mode.set(int(dis_mode))
        else: self.on_disable_mode.set(0)
        
        dis_ctcss = str(globals.config.get(self.section, 'ON_DISABLE_CTCSS'))
        if (len(dis_ctcss) > 0): self.on_disable_ctcss.set(int(dis_ctcss))
        else: self.on_disable_ctcss.set(0)

        # Create the dialog box.
        self.dlg_config_cat = tk.Toplevel(self.root)
        self.dlg_config_cat.title('CAT Interface Configuration')
        validateNumberCommand = self.dlg_config_cat.register(self._validate_number)
        
        # Rig selection menu.
        row = 0
        ttk.Label(self.dlg_config_cat, text='Rig:  ').grid(row=row, column=0, padx=3, pady=6, sticky='E')
        mnu_rig = tk.OptionMenu(
            self.dlg_config_cat,
            self.rig_text,
            *rig_list)
        mnu_rig.config(width=10)
        mnu_rig.grid(row=row, column=1, padx=6, pady=3, sticky='W')
        row += 1
        
        # Port selection menu.
        ttk.Label(self.dlg_config_cat, text='Port:  ').grid(row=row, column=0, padx=3, pady=6, sticky='E')
        mnu_port = tk.OptionMenu(
            self.dlg_config_cat,
            self.port_text,
            *port_list)
        mnu_port.config(width=10)
        mnu_port.grid(row=row, column=1, padx=6, pady=3, sticky='W')
        row += 1
        
        # Baud rate selection menu.
        ttk.Label(self.dlg_config_cat, text='Baud:  ').grid(row=row, column=0, padx=3, pady=6, sticky='E')
        mnu_baud = tk.OptionMenu(
            self.dlg_config_cat,
            self.baud_text,
            *baud_list)
        mnu_baud.config(width=10)
        mnu_baud.grid(row=row, column=1, padx=6, pady=3, sticky='W')
        row += 1
        
        # Data bits selection menu.
        ttk.Label(self.dlg_config_cat, text='Data bits:  ').grid(row=row, column=0, padx=3, pady=6, sticky='E')
        mnu_data = tk.OptionMenu(
            self.dlg_config_cat,
            self.data_bits_text,
            *data_list)
        mnu_data.config(width=10)
        mnu_data.grid(row=row, column=1, padx=6, pady=3, sticky='W')
        row += 1
        
        # Parity selection menu.
        ttk.Label(self.dlg_config_cat, text='Parity:  ').grid(row=row, column=0, padx=3, pady=6, sticky='E')
        mnu_parity = tk.OptionMenu(
            self.dlg_config_cat,
            self.parity_text,
            *parity_list)
        mnu_parity.config(width=10)
        mnu_parity.grid(row=row, column=1, padx=6, pady=3, sticky='W')
        row += 1
        
        # Stop bits selection menu.
        ttk.Label(self.dlg_config_cat, text='Stop bits:  ').grid(row=row, column=0, padx=3, pady=6, sticky='E')
        mnu_stop = tk.OptionMenu(
            self.dlg_config_cat,
            self.stop_bits_text,
            *stop_list)
        mnu_stop.config(width=10)
        mnu_stop.grid(row=row, column=1, padx=6, pady=3, sticky='W')
        row += 1
        
        # Options to select when CAT interface is enabled.
        ttk.Label(self.dlg_config_cat, text='When enabled:').grid(row=row, column=0, padx=3, pady=6, sticky='E')
        ena_frame = tk.Frame(self.dlg_config_cat)
        ck = tk.Checkbutton(ena_frame, 
            text='Turn split on',
            variable=self.on_enable_split,
            command=None,
            onvalue = 1, 
            offvalue = 0)
        ck.grid(row=0, column=0)
        ck = tk.Checkbutton(ena_frame, 
            text='Set mode',
            variable=self.on_enable_mode,
            command=None,
            onvalue = 1, 
            offvalue = 0)
        ck.grid(row=0, column=1)
        ena_frame.grid(row=row, column=1, padx=6, pady=3, sticky='EW')
        row += 1
        
        # Options to select when CAT interface is disabled.
        ttk.Label(self.dlg_config_cat, text='When disabled:').grid(row=row, column=0, padx=3, pady=6, sticky='E')
        dis_frame = tk.Frame(self.dlg_config_cat)
        ck = tk.Checkbutton(dis_frame, 
            text='Turn split off',
            variable=self.on_disable_split,
            command=None,
            onvalue = 1, 
            offvalue = 0)
        ck.grid(row=0, column=0)
        ck = tk.Checkbutton(dis_frame, 
            text='Restore frequency/mode',
            variable=self.on_disable_mode,
            command=None,
            onvalue = 1, 
            offvalue = 0)
        ck.grid(row=0, column=1)
        ck = tk.Checkbutton(dis_frame, 
            text='Turn CTCSS off',
            variable=self.on_disable_ctcss,
            command=None,
            onvalue = 1, 
            offvalue = 0)
        ck.grid(row=0, column=2)
        dis_frame.grid(row=row, column=1, padx=6, pady=3, sticky='EW')
        row += 1

        # Button frame for OK/Cancel buttons.
        btn_frm = tk.Frame(self.dlg_config_cat)
        
        # OK button.
        btn_ok = tk.Button(btn_frm, 
            text='OK', 
            width=10, 
            command=self._dlg_config_cat_ok)
        btn_ok.grid(row=0, column=0, padx=6, pady=6)
        
        # Cancel button.
        btn_cancel = tk.Button(btn_frm, 
            text='Cancel', 
            width=10, 
            command=self.dlg_config_cat.destroy)
        btn_cancel.grid(row=0, column=1, padx=6, pady=6)
        
        # Center the buttons at the bottom of the dialog box.
        btn_frm.grid(row=row, column=0, columnspan=4, padx=6, pady=6)
    
        mnu_rig.focus_set()
        self.dlg_config_cat.grab_set() # Make the dialog modal
        
        # Set the proper window size and center it on the screen.
        set_geometry(self.dlg_config_cat)

    # ------------------------------------------------------------------------
    def _dlg_config_cat_ok(self):
        """
        Dialog box OK button handler.
        """
        if not globals.config.has_section(self.section):
            globals.config.add_section(self.section)
        globals.config.set(self.section, 'RIG', self.rig_text.get())
        globals.config.set(self.section, 'PORT', self.port_text.get())
        globals.config.set(self.section, 'BAUD', self.baud_text.get())
        globals.config.set(self.section, 'DATA', str(self.data_bits_text.get()))
        globals.config.set(self.section, 'PARITY', self.parity_text.get())
        globals.config.set(self.section, 'STOP', self.stop_bits_text.get())
        globals.config.set(self.section, 'ON_ENABLE_SPLIT', self.on_enable_split.get())
        globals.config.set(self.section, 'ON_ENABLE_MODE', self.on_enable_mode.get())
        globals.config.set(self.section, 'ON_DISABLE_SPLIT', self.on_disable_split.get())
        globals.config.set(self.section, 'ON_DISABLE_MODE', self.on_disable_mode.get())
        globals.config.set(self.section, 'ON_DISABLE_CTCSS', self.on_disable_ctcss.get())
        
        # Save parameters to .INI file.
        globals.config.write()
        
        # Update the rig CAT control object.
        update_rig_cat()

        self.dlg_config_cat.destroy()

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
        if (len(all) > 7): return False      # Limit entry length
        if what.isnumeric(): return True     # Must be numeric
        return False                         # Nothing else allowed


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('DlgConfigCat main program not implemented.')
