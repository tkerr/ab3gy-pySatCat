###############################################################################
# WidgetPresetButton.py
# Author: Tom Kerr AB3GY
#
# WidgetPresetButton class for use with the pySatCat application.
# Provides a preset button for selecting a satellite + communication mode.
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

# Tkinter packages.
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

# Local packages.
import globals
from pySatCatUtils import *
from DlgConfigPreset import DlgConfigPreset
from PresetConfiguration import PresetConfiguration
from RigCat import on_preset_change
from SatelliteTracker import SatelliteTracker


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# WidgetPresetButton class.
##############################################################################
class WidgetPresetButton(object):
    """
    WidgetPresetButton class for use with the pySatCat application.
    Provides a preset button for selecting a satellite + communication mode.
    """
    # ------------------------------------------------------------------------
    def __init__(self, parent, id):
        """
        Class constructor.
        
        Parameters
        ----------
        parent : Tk object
            The parent object containing the widget
        id : int
            The preset button ID

        Returns
        -------
        None.
        """
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.button = None
        self.id = 0
        self.button_text = tk.StringVar(self.frame)

        try:
            self.id = int(id)
        except Exception:
            print('Invalid satellite preset ID: ' + str(id))
            self.id = 0
            
        self.config = PresetConfiguration(self.id)

        self.PADX = 3
        self.PADY = 3
        
        self._widget_init()

    # ------------------------------------------------------------------------
    def get_preset_name(self):
        """
        Get the preset button name text.
        """
        return self.config.get_preset_name()

    # ------------------------------------------------------------------------
    def set_preset_name(self, text):
        """
        Set the preset button name text.
        """
        name = str(text)
        self.config.set_preset_name(name)
        self.button_text.set(name)
        self.config.write_config()

    # ------------------------------------------------------------------------
    def get_id(self):
        """
        Get the preset button ID.
        """
        return self.config.get_id()

    # ------------------------------------------------------------------------
    def set_bg_color(self, color):
        """
        Set the preset button background color.
        """
        self.button.config(bg=color)
        
    # ------------------------------------------------------------------------
    def _widget_init(self):
        """
        Internal method to create and initialize the UI widget.
        """
        
        # Get button name from preset configuration.
        name = self.config.get_preset_name()
        self.button_text.set(name)
        
        self.button = tk.Button(self.frame,
            width=15,
            textvariable=self.button_text,
            command=self._on_left_click,
            font=tkFont.Font(size=10))
        self.button.bind('<Button-3>', self._on_right_click)
        self.button.grid(
            row=0,
            column=0,
            padx=self.PADX,
            pady=self.PADY)
        self.set_bg_color(globals.PRESET_BGCOLOR)

    # ------------------------------------------------------------------------
    def _on_left_click(self):
        """
        Preset button left click handler.
        """
        globals.selected_preset = self.get_id()
        #print('Clicked ' + self.button_text.get())
        #print('Preset ID: ' + str(self.get_id()))
        
        # Clear existing fields.
        globals.widget_desired_freq.clear()
        globals.widget_corrected_freq.clear()
        globals.widget_az_el_range.clear()
        globals.widget_sat_info.clear()
        
        # Update the desired frequency.
        ul = self.config.get_uplink_freq_mhz()
        globals.widget_desired_freq.set_uplink(ul)
        dl = self.config.get_downlink_freq_mhz()
        globals.widget_desired_freq.set_downlink(dl)
        
        # Update the corrected frequency checkboxes.
        globals.widget_corrected_freq.set_uplink_corrected_enable(
            self.config.get_uplink_use_corrected())
        globals.widget_corrected_freq.set_downlink_corrected_enable(
            self.config.get_uplink_use_corrected())
        
        # Update the rig configuration.
        on_preset_change()

    # ------------------------------------------------------------------------
    def _on_right_click(self, event):
        """
        Preset button right click handler.
        """
        
        # Open the configuration dialog window and wait for it to complete.
        dlg = DlgConfigPreset(self.parent, self.config)
        self.frame.wait_window(dlg.dlg_config_preset)
        
        # Update button name from preset configuration.
        preset_name = self.config.get_preset_name()
        if (len(preset_name) > 0):
            self.button_text.set(preset_name)
        
        # Update the satellite tracker for this preset.
        sat_name = self.config.get_sat_name()
        file_name = self.config.get_file_name()
        if (len(sat_name) > 0) and (len(file_name) > 0):
            file_path = tle_file_path(file_name)
            globals.tracker_list[self.id - 1].init_sat(sat_name, file_path)


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    globals.init()
    root = tk.Tk()
    root.title('WidgetPresetButton test application')
    wmb1 = WidgetPresetButton(root, id=1)
    wmb1.frame.grid(
        row=0,
        column=0,
        padx=6,
        pady=6)
    wmb1.set_bg_color(globals.INVIEW_BGCOLOR)
    wmb2 = WidgetPresetButton(root, id=2)
    wmb2.frame.grid(
        row=1,
        column=0,
        padx=6,
        pady=6)
    print('WMB1 button ID:   ' + str(wmb1.get_id()))
    print('WMB1 button name: ' + wmb1.get_preset_name())
    print('WMB2 button ID:   ' + str(wmb2.get_id()))
    print('WMB2 button name: ' + wmb2.get_preset_name())
    root.mainloop()
   