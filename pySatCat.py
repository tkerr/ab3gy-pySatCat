###############################################################################
# pySatCat.py
# Author: Tom Kerr AB3GY
#
# Amateur radio application to control a transceiver for satellite operation.
# Computes satellite position and applies Doppler shift to uplink and downlink 
# frequencies when the satellite is in view.
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

# Tkinter packages.
import tkinter as tk

# Local environment init.
import _env_init

# Local packages.
import globals
from src.pySatCatUtils import *
from src.AppMenu import AppMenu
from src.CatControlThread import start_cat_control_thread
from src.ConfigFile import ConfigFile
from src.RigCat import update_rig_cat
from src.SatelliteTracker import SatelliteTracker
from src.TrackerThread import start_tracker_thread
from src.WidgetDesiredFrequency import WidgetDesiredFrequency
from src.WidgetCorrectedFrequency import WidgetCorrectedFrequency
from src.WidgetAzElRange import WidgetAzElRange
from src.WidgetSatInfo import WidgetSatInfo
from src.WidgetCatControl import WidgetCatControl
from src.WidgetPresetButton import WidgetPresetButton
from src.WidgetPassWindow import WidgetPassWindow
from src.WidgetCountdown import WidgetCountdown
from src.WidgetClock import WidgetClock


##############################################################################
# Functions.
############################################################################## 


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":

    app_width  = 400
    app_height = 400

    # Print a startup message in the command prompt window.
    print('Starting ' + globals.APP_NAME)
    
    # Initialize the application configuration.
    globals.init()
    
    # Create and initialize the root window.
    globals.root = tk.Tk()
    globals.root.minsize(app_width, app_height)
    globals.root.title(globals.APP_NAME + ' - Python Satellite CAT Control')
    globals.root.protocol("WM_DELETE_WINDOW", lambda: app_close())
    
    # Initialize Tk variables after root window initialized.
    globals.init_tk_vars()
    
    # Create the main menu.
    globals.app_menu = AppMenu(globals.root)
    
    row = 0
    
    # Desired frequency widget.
    globals.widget_desired_freq = WidgetDesiredFrequency(globals.root)
    globals.widget_desired_freq.frame.grid(
        row=row,
        column=0,
        padx=(6, 3),
        pady=3,
        sticky='EW')
    
    # Corrected frequency widget.
    globals.widget_corrected_freq = WidgetCorrectedFrequency(globals.root)
    globals.widget_corrected_freq.frame.grid(
        row=row,
        column=1,
        padx=3,
        pady=3,
        sticky='EW')
    
    # Az-El-Range widget.
    globals.widget_az_el_range = WidgetAzElRange(globals.root)
    globals.widget_az_el_range.frame.grid(
        row=row,
        column=2,
        padx=(3, 6),
        pady=3,
        sticky='EW')

    # Satellite pass info summary.
    row += 1
    globals.widget_sat_info = WidgetSatInfo(globals.root)
    globals.widget_sat_info.frame.grid(
        row=row,
        column=0,
        columnspan=3,
        sticky='EW',
        padx=6,
        pady=3)

    # CAT control status bar.
    row += 1
    globals.widget_cat_control = WidgetCatControl(globals.root)
    globals.widget_cat_control.frame.grid(
        row=row,
        column=0,
        columnspan=3,
        sticky='EW',
        padx=6,
        pady=3)

    summary_window_row = row + 1
    
    # Satellite presets and their associated trackers.
    for i in range(0, globals.NUM_PRESETS):
        row += 1
        
        preset = WidgetPresetButton(globals.root, i+1)
        preset.frame.grid(
            row=row,
            column=0,
            padx=3,
            pady=3)
        if (preset.get_preset_name() == ''):
            preset.set_preset_name('Satellite ' + str(i+1))
        sat_name = preset.config.get_sat_name()
        file_name = preset.config.get_file_name()
        globals.preset_list.append(preset)
        
        tracker = SatelliteTracker()
        if (len(sat_name) > 0) and (len(file_name) > 0):
            file_path = tle_file_path(file_name)
            tracker.init_sat(sat_name, file_path)
        globals.tracker_list.append(tracker)

    globals.widget_pass_window = WidgetPassWindow(globals.root)
    globals.widget_pass_window.frame.grid(row=summary_window_row,
        rowspan = globals.NUM_PRESETS,
        column = 1,
        columnspan = 2,
        sticky='N',
        padx=(3, 6),
        pady=6)
    
    row += 1
    globals.widget_countdown = WidgetCountdown(globals.root)
    globals.widget_countdown.frame.grid(
        row=row,
        column=0, 
        sticky='W',
        padx=3,
        pady=3)
    wc = WidgetClock(globals.root)
    wc.frame.grid(
        row=row,
        column=2, 
        sticky='E',
        padx=3,
        pady=3)

    # Set the proper window size and center it on the screen.
    set_geometry(globals.root)
    
    # Initialize the observer location.
    update_location()

    # Initialize the rig CAT control object.
    update_rig_cat()
    
    # Start the satellite tracking thread.
    start_tracker_thread()
    
    # Start the CAT control thread.
    start_cat_control_thread()

    # Loop forever.
    globals.root.mainloop()
