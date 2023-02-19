###############################################################################
# WidgetSatInfo.py
# Author: Tom Kerr AB3GY
#
# WidgetSatInfo class for use with the pySatCat application.
# Provides the satellite pass summary info display.
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
import ephem
from datetime import datetime

# Tkinter packages.
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

# Local packages.
import globals
from src.pySatCatUtils import *
from src.ConfigFile import ConfigFile
from src.WindowOrbitMap import WindowOrbitMap

##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# WidgetSatInfo class.
##############################################################################
class WidgetSatInfo(object):
    """
    WidgetSatInfo class for use with the pySatCat application.
    Provides the satellite pass summary info display.
    """
    # ------------------------------------------------------------------------
    def __init__(self, parent, showname=True, showlabels=True):
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
        self.showname = showname
        self.showlabels = showlabels
        
        # Text entry variables.
        self.sat_name_text = tk.StringVar(self.frame)
        self.start_date_text = tk.StringVar(self.frame)
        self.aos_time_text = tk.StringVar(self.frame)
        self.aos_az_text = tk.StringVar(self.frame)
        self.max_time_text = tk.StringVar(self.frame)
        self.max_az_text = tk.StringVar(self.frame)
        self.max_el_text = tk.StringVar(self.frame)
        self.los_time_text = tk.StringVar(self.frame)
        self.los_az_text = tk.StringVar(self.frame)
               
        # Text entry boxes.
        self.tb_sat_name = None
        self.tb_start_date = None
        self.tb_aos_time = None
        self.tb_aos_az = None
        self.tb_max_time = None
        self.tb_max_az = None
        self.tb_max_el = None
        self.tb_los_time = None
        self.tb_los_az = None

        self.PADX = 3
        self.PADY = 3
        
        self._widget_init(self.showname, self.showlabels)

    # ------------------------------------------------------------------------
    def clear(self):
        """
        Clear all text entry fields.
        """
        self.sat_name_text.set('')
        self.start_date_text.set('')
        self.aos_time_text.set('')
        self.aos_az_text.set('')
        self.max_time_text.set('')
        self.max_az_text.set('')
        self.max_el_text.set('')
        self.los_time_text.set('')
        self.los_az_text.set('')

    # ------------------------------------------------------------------------
    def get_name(self):
        """
        Get the displayed satellite name in the text box.
        """
        return self.sat_name_text.get()

    # ------------------------------------------------------------------------
    def set_name(self, name):
        """
        Set the displayed satellite name in the text box.
        """
        self.sat_name_text.set(name)

    # ------------------------------------------------------------------------
    def set_pass_info(self, aos_time, aos_az, max_time, max_az, max_el, los_time, los_az):
        """
        Set the displayed satellite pass information.
        """
        dt = aos_time.datetime()
        dt_str = dt.strftime('%Y-%m-%d')
        self.start_date_text.set(dt_str)

        dt_str = dt.strftime('%H:%M:%S')
        self.aos_time_text.set(dt_str)

        az_str = ('%0.1f' % aos_az)
        self.aos_az_text.set(az_str)
        
        dt = max_time.datetime()
        dt_str = dt.strftime('%H:%M:%S')
        self.max_time_text.set(dt_str)
        
        az_str = ('%0.1f' % max_az)
        self.max_az_text.set(az_str)
        
        el_str = ('%0.1f' % max_el)
        self.max_el_text.set(el_str)
        
        dt = los_time.datetime()
        dt_str = dt.strftime('%H:%M:%S')
        self.los_time_text.set(dt_str)

        az_str = ('%0.1f' % los_az)
        self.los_az_text.set(az_str)

    # ------------------------------------------------------------------------
    def set_bg_color(self, color):
        """
        Set the background color of some information display text boxes.
        """
        self.tb_sat_name.config(disabledbackground=color)
        self.tb_start_date.config(disabledbackground=color)
        self.tb_aos_time.config(disabledbackground=color)
        self.tb_aos_az.config(disabledbackground=color)
        self.tb_max_time.config(disabledbackground=color)
        self.tb_max_az.config(disabledbackground=color)
        self.tb_max_el.config(disabledbackground=color)
        self.tb_los_time.config(disabledbackground=color)
        self.tb_los_az.config(disabledbackground=color)
    
    # ------------------------------------------------------------------------
    def _map_btn_handler(self):
        """
        The Map button handler.
        """
        tle_file = ''
        sat_name = self.sat_name_text.get()
        obs_lat = 0.0
        obs_lon = 0.0
        obs_alt = 0.0

        # Get the satellite TLE file from the configuration.
        if (globals.selected_preset > 0):
            section = 'PRESET' + str(globals.selected_preset)
            if globals.config.has_section(section):
                tle_file = globals.config.get(section, 'tle_file')
            
        # Get the observer parameters from the configuration.
        section = 'OBSERVER'
        if globals.config.has_section(section):
            obs_lat = to_float(globals.config.get(section, 'lat'))
            obs_lon = to_float(globals.config.get(section, 'lon'))
            obs_alt = to_float(globals.config.get(section, 'alt'))
        
        # Create the window if it does not exist.
        if globals.window_orbit_map is None:
            globals.window_orbit_map = WindowOrbitMap(globals.root)
        
        # Update the satellite on the map.
        globals.window_orbit_map.map.set_observer(obs_lat, obs_lon, obs_alt)
        if (len(sat_name) > 0) and (len(tle_file) > 0):
            globals.window_orbit_map.map.init_satellite(sat_name, tle_file)
            globals.window_orbit_map.map.update_track()
        
    # ------------------------------------------------------------------------
    def _widget_init(self, showname, showlabels):
        """
        Internal method to create and initialize the UI widget.
        """
        # Control variable initialization.
        self.clear()

        # Row of text boxes containing satellite information.
        row = 0
        col = 0
        
        # Optional header row of labels.
        if showlabels:
            if showname:
                lbl = tk.Label(self.frame, 
                    text='Satellite',
                    font=tkFont.Font(size=10))
                lbl.grid(
                    row=row, 
                    column=col,
                    padx=self.PADX,
                    pady=self.PADY)
                col += 1
        
            lbl = tk.Label(self.frame, 
                text='AOS Date',
                font=tkFont.Font(size=10))
            lbl.grid(
                row=row, 
                column=col,
                padx=self.PADX,
                pady=self.PADY)
            col += 1
        
            lbl = tk.Label(self.frame, 
                text='AOS Time',
                font=tkFont.Font(size=10))
            lbl.grid(
                row=row, 
                column=col,
                padx=self.PADX,
                pady=self.PADY)
            col += 1
        
            lbl = tk.Label(self.frame, 
                text='AOS Az',
                font=tkFont.Font(size=10))
            lbl.grid(
                row=row, 
                column=col,
                padx=self.PADX,
                pady=self.PADY)
            col += 1
        
            lbl = tk.Label(self.frame, 
                text='Max Time',
                font=tkFont.Font(size=10))
            lbl.grid(
                row=row, 
                column=col,
                padx=self.PADX,
                pady=self.PADY)
            col += 1
        
            lbl = tk.Label(self.frame, 
                text='Max Az',
                font=tkFont.Font(size=10))
            lbl.grid(
                row=row, 
                column=col,
                padx=self.PADX,
                pady=self.PADY)
            col += 1
        
            lbl = tk.Label(self.frame, 
                text='Max El',
                font=tkFont.Font(size=10))
            lbl.grid(
                row=row, 
                column=col,
                padx=self.PADX,
                pady=self.PADY)
            col += 1
        
            lbl = tk.Label(self.frame, 
                text='LOS Time',
                font=tkFont.Font(size=10))
            lbl.grid(
                row=row, 
                column=col,
                padx=self.PADX,
                pady=self.PADY)
            col += 1
        
            lbl = tk.Label(self.frame, 
                text='LOS Az',
                font=tkFont.Font(size=10))
            lbl.grid(
                row=row, 
            column=col,
                padx=self.PADX,
                pady=self.PADY)
            row += 1
            #col += 1

        # Text entry fields containing satellite data.
        col = 0
        self.tb_sat_name = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=12,
            textvariable=self.sat_name_text,
            font=tkFont.Font(size=10))
        if showname:
            self.tb_sat_name.grid(
                row=row, 
                column=col,
                padx=self.PADX, 
                pady=(0, self.PADY))
            col += 1

        self.tb_start_date = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=10,
            textvariable=self.start_date_text,
            font=tkFont.Font(size=10))
        self.tb_start_date.grid(
            row=row, 
            column=col,
            padx=(0, self.PADX), 
            pady=(0, self.PADY))
        col += 1
        
        self.tb_aos_time = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=9,
            textvariable=self.aos_time_text,
            font=tkFont.Font(size=10))
        self.tb_aos_time.grid(
            row=row, 
            column=col,
            padx=(0, self.PADX), 
            pady=(0, self.PADY))
        col += 1
        
        self.tb_aos_az = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=8,
            textvariable=self.aos_az_text,
            font=tkFont.Font(size=10))
        self.tb_aos_az.grid(
            row=row, 
            column=col,
            padx=(0, self.PADX), 
            pady=(0, self.PADY))
        col += 1
        
        self.tb_max_time = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=9,
            textvariable=self.max_time_text,
            font=tkFont.Font(size=10))
        self.tb_max_time.grid(
            row=row, 
            column=col,
            padx=(0, self.PADX), 
            pady=(0, self.PADY))
        col += 1
        
        self.tb_max_az = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=8,
            textvariable=self.max_az_text,
            font=tkFont.Font(size=10))
        self.tb_max_az.grid(
            row=row, 
            column=col,
            padx=(0, self.PADX), 
            pady=(0, self.PADY))
        col += 1
        
        self.tb_max_el = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=8,
            textvariable=self.max_el_text,
            font=tkFont.Font(size=10))
        self.tb_max_el.grid(
            row=row, 
            column=col,
            padx=(0, self.PADX), 
            pady=(0, self.PADY))
        col += 1
        
        self.tb_los_time = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=9,
            textvariable=self.los_time_text,
            font=tkFont.Font(size=10))
        self.tb_los_time.grid(
            row=row, 
            column=col,
            padx=(0, self.PADX), 
            pady=(0, self.PADY))
        col += 1
        
        self.tb_los_az = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=8,
            textvariable=self.los_az_text,
            font=tkFont.Font(size=10))
        self.tb_los_az.grid(
            row=row, 
            column=col,
            padx=(0, self.PADX), 
            pady=(0, self.PADY))
        col += 1
        
        # Map display button.
        map_btn = tk.Button(self.frame,
            text='Map', 
            width=7,
            command=self._map_btn_handler)
        map_btn.grid(
            row=row, 
            column=col, 
            padx=self.PADX, 
            pady=(0, self.PADY))

       
##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    # Create and initialize the root window.
    aos = ephem.Date(datetime.now())
    los = ephem.Date(datetime.utcnow())
    root = tk.Tk()
    root.title('WidgetSatInfo test application')
    wsi = WidgetSatInfo(root, True)
    wsi.frame.grid(
        row=0,
        column=0,
        padx=6,
        pady=6)
    wsi.set_name('My Satellite')
    wsi.set_pass_info(
        aos, 
        100.0, 
        aos,
        200.0,
        90.0,
        los,
        300.0)
    root.mainloop()
   