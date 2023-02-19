###############################################################################
# DlgConfigPreset.py
# Author: Tom Kerr AB3GY
#
# DlgConfigPreset class for use with the pySatCat application.
# Implements a dialog box for configuring a satellite preset.
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
import tkinter.font as tkFont
from tkinter import ttk

# Local packages.
import globals
from src.pySatCatUtils import *
from src.PresetConfiguration import PresetConfiguration
from src.RigCat import CTCSS_TONES
from PyRigCat.PyRigCat import OperatingMode

##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################


##############################################################################
# DlgConfigPreset class.
##############################################################################
class DlgConfigPreset(object):
    """
    DlgConfigStation class for use with the pySatCat application.
    Implements a dialog box for configuring a satellite preset.
    """

    # ------------------------------------------------------------------------
    def __init__(self, root, preset_config):
        """
        Class constructor.
    
        Parameters
        ----------
        root : Tk object
            The pySatCat application root window.
        preset_config : PresetConfiguration object
            Used to pass configuration parameters between the dialog box and its parent.
        
        Returns
        -------
        None.
        """
        self.root = root # The root window
        self.dlg_config_preset = tk.Toplevel(root)  # The dialog box
        self.config = preset_config
        
        self.PADX = 3
        self.PADY = 3
        
        # Text entry variables.
        self.preset_name_text = tk.StringVar(self.root)             # Preset name
        self.sat_name_text = tk.StringVar(self.root)                # Satellite name
        self.tle_file_text = tk.StringVar(self.root)                # TLE file name
        self.uplink_freq_mhz_text = tk.DoubleVar(self.root)         # Uplink frequency in MHz
        self.uplink_use_corrected = tk.IntVar(self.root)            # Doppler corrected frequency checkbox
        self.uplink_mode_text = tk.StringVar(self.root)             # Uplink transceiver mode
        self.uplink_tuning_step_text = tk.DoubleVar(self.root)      # Uplink tuning step in KHz
        self.uplink_tune_threshold_text = tk.DoubleVar(self.root)   # Uplink tuning threshold in KHz
        self.uplink_ctcss_text = tk.StringVar(self.root)            # Uplink CTCSS tone
        self.downlink_freq_mhz_text = tk.DoubleVar(self.root)       # Downlink frequency in MHz
        self.downlink_use_corrected = tk.IntVar(self.root)          # Doppler corrected frequency checkbox
        self.downlink_mode_text = tk.StringVar(self.root)           # Downlink transceiver mode
        self.downlink_tuning_step_text = tk.DoubleVar(self.root)    # Downlink tuning step in KHz
        self.downlink_tune_threshold_text = tk.DoubleVar(self.root) # Downlink tuning threshold in KHz

        self._dlg_init()

    # ------------------------------------------------------------------------
    def _dlg_init(self):
        """
        Internal method to create and initialize the dialog box.
        """
        
        # Initialize dialog variables.
        self.config.init()
        self.preset_name_text.set(self.config.get_preset_name())
        self.sat_name_text.set(self.config.get_sat_name())
        self.tle_file_text.set(self.config.get_file_name())
        self.uplink_freq_mhz_text.set(to_float(self.config.get_uplink_freq_mhz()))
        self.uplink_use_corrected.set(to_int(self.config.get_uplink_use_corrected()))
        self.uplink_mode_text.set(self.config.get_uplink_mode())
        self.uplink_tuning_step_text.set(to_float(self.config.get_uplink_tuning_step()))
        self.uplink_tune_threshold_text.set(to_float(self.config.get_uplink_tune_threshold()))
        self.uplink_ctcss_text.set(self.config.get_uplink_ctcss_tone())
        self.downlink_freq_mhz_text.set(to_float(self.config.get_downlink_freq_mhz()))
        self.downlink_use_corrected.set(to_int(self.config.get_downlink_use_corrected()))
        self.downlink_mode_text.set(self.config.get_downlink_mode())
        self.downlink_tuning_step_text.set(to_float(self.config.get_downlink_tuning_step()))
        self.downlink_tune_threshold_text.set(to_float(self.config.get_downlink_tune_threshold()))
        
        self.dlg_config_preset.title('Satellite Preset ' + str(self.config.get_id()))
        
        validateFloatCommand = self.dlg_config_preset.register(self._validate_float)
        row = 0
        col = 0

        # Preset name.
        lbl = tk.Label(self.dlg_config_preset, 
            text='Preset Name:',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=col,
            sticky='E',
            padx=self.PADX,
            pady=(2*self.PADY, self.PADY))
        col += 1
        tb = tk.Entry(self.dlg_config_preset,
            width=15,
            textvariable=self.preset_name_text,
            font=tkFont.Font(size=10))
        tb.grid(
            row=row, 
            column=col,
            padx=self.PADX, 
            pady=(2*self.PADY, self.PADY))
        col += 1
        
        # Satellite name.
        lbl = tk.Label(self.dlg_config_preset, 
            text='Satellite Name:',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=col,
            sticky='E',
            padx=self.PADX,
            pady=(2*self.PADY, self.PADY))
        col += 1
        tb = tk.Entry(self.dlg_config_preset,
            width=15,
            textvariable=self.sat_name_text,
            font=tkFont.Font(size=10))
        tb.grid(
            row=row, 
            column=col,
            padx=self.PADX, 
            pady=(2*self.PADY, self.PADY))
        col += 1
        
        # TLE file name.
        lbl = tk.Label(self.dlg_config_preset, 
            text='TLE File:',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=col,
            sticky='E',
            padx=self.PADX,
            pady=(2*self.PADY, self.PADY))
        col += 1
        tb = tk.Entry(self.dlg_config_preset,
            width=15,
            textvariable=self.tle_file_text,
            font=tkFont.Font(size=10))
        tb.grid(
            row=row, 
            column=col,
            padx=self.PADX, 
            pady=(2*self.PADY, self.PADY))
        col += 1

        # Uplink/downlink field titles.
        row += 1
        col = 1
        lbl = tk.Label(self.dlg_config_preset, 
            text='Freq (MHz)',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        lbl = tk.Label(self.dlg_config_preset, 
            text='Corrected',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        lbl = tk.Label(self.dlg_config_preset, 
            text='Mode',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        lbl = tk.Label(self.dlg_config_preset, 
            text='Tuning Step (KHz)',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        lbl = tk.Label(self.dlg_config_preset, 
            text='Threshold (KHz)',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        lbl = tk.Label(self.dlg_config_preset, 
            text='CTCSS Tone',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        # Uplink parameter entry.
        row += 1
        col = 0
        lbl = tk.Label(self.dlg_config_preset, 
            text='Uplink:',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        # Uplink frequency.
        tb = tk.Entry(self.dlg_config_preset,
            width=10,
            textvariable=self.uplink_freq_mhz_text,
            validate='key', 
            validatecommand=(validateFloatCommand, '%d', '%i', '%S', '%P'),
            font=tkFont.Font(size=10))
        tb.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        # Uplink Doppler correction enable.
        ckbx = tk.Checkbutton(self.dlg_config_preset, 
            variable=self.uplink_use_corrected,
            command=None,
            onvalue = 1, 
            offvalue = 0)
        ckbx.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=(0, self.PADY))
        col += 1
        
        # Uplink mode.
        mnu = tk.OptionMenu(
            self.dlg_config_preset,
            self.uplink_mode_text,
            *OperatingMode.MODE_LIST)
        mnu.config(width=10)
        mnu.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        # Uplink tuning step.
        tb = tk.Entry(self.dlg_config_preset,
            width=10,
            textvariable=self.uplink_tuning_step_text,
            validate='key', 
            validatecommand=(validateFloatCommand, '%d', '%i', '%S', '%P'),
            font=tkFont.Font(size=10))
        tb.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        # Uplink tuning threshold.
        tb = tk.Entry(self.dlg_config_preset,
            width=10,
            textvariable=self.uplink_tune_threshold_text,
            validate='key', 
            validatecommand=(validateFloatCommand, '%d', '%i', '%S', '%P'),
            font=tkFont.Font(size=10))
        tb.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        # Uplink CTCSS tone.
        ctcss_list = list(CTCSS_TONES.keys())
        mnu = tk.OptionMenu(
            self.dlg_config_preset,
            self.uplink_ctcss_text,
            *ctcss_list)
        mnu.config(width=10)
        mnu.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        # Downlink parameter entry.
        row += 1
        col = 0
        lbl = tk.Label(self.dlg_config_preset, 
            text='Downlink:',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        # Downlink frequency.
        tb = tk.Entry(self.dlg_config_preset,
            width=10,
            textvariable=self.downlink_freq_mhz_text,
            validate='key', 
            validatecommand=(validateFloatCommand, '%d', '%i', '%S', '%P'),
            font=tkFont.Font(size=10))
        tb.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        # Downlink Doppler correction enable.
        ckbx = tk.Checkbutton(self.dlg_config_preset, 
            variable=self.downlink_use_corrected,
            command=None,
            onvalue = 1, 
            offvalue = 0)
        ckbx.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=(0, self.PADY))
        col += 1
        
        # Downlink mode.
        mnu = tk.OptionMenu(
            self.dlg_config_preset,
            self.downlink_mode_text,
            *OperatingMode.MODE_LIST)
        mnu.config(width=10)
        mnu.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        # Downlink tuning step.
        tb = tk.Entry(self.dlg_config_preset,
            width=10,
            textvariable=self.downlink_tuning_step_text,
            validate='key', 
            validatecommand=(validateFloatCommand, '%d', '%i', '%S', '%P'),
            font=tkFont.Font(size=10))
        tb.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        # Downlink tuning threshold.
        tb = tk.Entry(self.dlg_config_preset,
            width=10,
            textvariable=self.downlink_tune_threshold_text,
            validate='key', 
            validatecommand=(validateFloatCommand, '%d', '%i', '%S', '%P'),
            font=tkFont.Font(size=10))
        tb.grid(
            row=row, 
            column=col,
            padx=self.PADX,
            pady=self.PADY)
        col += 1
        
        # Button frame for OK/Cancel buttons.
        row += 1
        btn_frm = tk.Frame(self.dlg_config_preset)
        
        # OK button.
        btn_ok = tk.Button(btn_frm, 
            text='OK', 
            width=10, 
            command=self._dlg_config_preset_ok)
        btn_ok.grid(row=0, column=0, padx=6, pady=6)
        
        # Cancel button.
        btn_cancel = tk.Button(btn_frm, 
            text='Cancel', 
            width=10, 
            command=self._dlg_config_preset_cancel)
        btn_cancel.grid(row=0, column=1, padx=6, pady=6)
        
        # Center the buttons at the bottom of the dialog box.
        btn_frm.grid(row=row, column=0, columnspan=7, padx=6, pady=6)
    
        self.dlg_config_preset.grab_set() # Make the dialog modal
        
        # Set the proper window size and center it on the screen.
        set_geometry(self.dlg_config_preset)

    # ------------------------------------------------------------------------
    def _dlg_config_preset_cancel(self):
        """
        Dialog box Cancel button handler.
        """
        self.dlg_config_preset.grab_release()
        self.dlg_config_preset.destroy()
        
    # ------------------------------------------------------------------------
    def _dlg_config_preset_ok(self):
        """
        Dialog box OK button handler.
        """
        self.config.set_preset_name(self.preset_name_text.get())
        self.config.set_sat_name(self.sat_name_text.get())
        self.config.set_file_name(self.tle_file_text.get())
        self.config.set_uplink_freq_mhz(to_float(self.uplink_freq_mhz_text.get()))
        self.config.set_uplink_use_corrected(to_int(self.uplink_use_corrected.get()))
        self.config.set_uplink_mode(self.uplink_mode_text.get())
        self.config.set_uplink_tuning_step(to_float(self.uplink_tuning_step_text.get()))
        self.config.set_uplink_tune_threshold(to_float(self.uplink_tune_threshold_text.get()))
        self.config.set_uplink_ctcss_tone(self.uplink_ctcss_text.get())
        
        self.config.set_downlink_freq_mhz(to_float(self.downlink_freq_mhz_text.get()))
        self.config.set_downlink_use_corrected(to_int(self.downlink_use_corrected.get()))
        self.config.set_downlink_mode(self.downlink_mode_text.get())
        self.config.set_downlink_tuning_step(to_float(self.downlink_tuning_step_text.get()))
        self.config.set_downlink_tune_threshold(to_float(self.downlink_tune_threshold_text.get()))
        self.config.write_config()

        self.dlg_config_preset.grab_release()
        self.dlg_config_preset.destroy()

    # ------------------------------------------------------------------------
    def _validate_float(self, why, where, what, all):
        """
        Validate a floating point number entry.

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
        if (what == '.'):
            if '.' in all[:idx]: return False # Only one occurrence allowed
            else: return True
        return False  # Nothing else allowed


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('DlgConfigPreset test program.')
    globals.init()
    root = tk.Tk()
    dlg = DlgConfigPreset(root, 1)
    root.mainloop()
