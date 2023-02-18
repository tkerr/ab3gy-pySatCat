###############################################################################
# WidgetAzElRange.py
# Author: Tom Kerr AB3GY
#
# WidgetAzElRange class for use with the pySatCat application.
# Provides the Azimuth-Elevation-Range display.
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

##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# WidgetAzElRange class.
##############################################################################
class WidgetAzElRange(object):
    """
    WidgetAzElRange class for use with the pySatCat application.
    Provides the Azimuth-Elevation-Range display.
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
        self.az_text = tk.StringVar(self.frame)
        self.el_text = tk.StringVar(self.frame)
        self.range_text = tk.StringVar(self.frame)
        self.lat_text = tk.StringVar(self.frame)
        self.lon_text = tk.StringVar(self.frame)
        self.sun_text = tk.StringVar(self.frame)
        
        # Text entry widgets.
        self.tb_az = None
        self.tb_el = None
        self.tb_range = None
        self.tb_lat = None
        self.tb_lon = None
        self.tb_sun = None

        self.PADX = 3
        self.PADY = 3
        
        self._widget_init()

    # ------------------------------------------------------------------------
    def clear(self):
        """
        Clear all text entry fields.
        """
        self.az_text.set('0.0')
        self.el_text.set('0.0')
        self.range_text.set('0.0')
        self.lat_text.set('0.0')
        self.lon_text.set('0.0')
        self.sun_text.set('')

    # ------------------------------------------------------------------------
    def set_pass_info(self, az, el, range, lat=None, lon=None, sun=None):
        """
        Set the displayed satellite az-el-range information.
        """
        if az is not None:
            az_str = ('%0.1f' % az)
            self.az_text.set(az_str)
        else:
            self.az_text.set('')
        
        if el is not None:
            el_str = ('%0.1f' % el)
            self.el_text.set(el_str)
        else:
            self.el_text.set('')
        
        if range is not None:
            range_str = ('%0.3f' % range)
            self.range_text.set(range_str)
        else:
            self.range_text.set('')
        
        if lat is not None:
            lat_str = ('%0.3f' % lat)
            self.lat_text.set(lat_str)
        else:
            self.lat_text.set('')
        
        if lon is not None:
            lon_str = ('%0.3f' % lon)
            self.lon_text.set(lon_str)
        else:
            self.lon_text.set('')
        
        if sun is not None:
            sun_str = 'Eclipsed'
            if (sun != 0): sun_str = 'Sunlight'
            self.sun_text.set(sun_str)
        else:
            self.sun_text.set('')

    # ------------------------------------------------------------------------
    def set_bg_color(self, color):
        """
        Set the background color of some information display text boxes.
        """
        self.tb_az.config(disabledbackground=color)
        self.tb_el.config(disabledbackground=color)
        self.tb_range.config(disabledbackground=color)
        self.tb_lat.config(disabledbackground=color)
        self.tb_lon.config(disabledbackground=color)
        self.tb_sun.config(disabledbackground=color)
            
        
    # ------------------------------------------------------------------------
    def _widget_init(self):
        """
        Internal method to create and initialize the UI widget.
        """
        self.clear()
        
        # Azimuth
        lbl = tk.Label(self.frame, 
            text='Azimuth:   ',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=0, 
            column=0,
            padx=self.PADX,
            pady=self.PADY)
        
        self.tb_az = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=9,
            textvariable=self.az_text,
            font=tkFont.Font(size=10))
        self.tb_az.grid(
            row=0, 
            column=1,
            sticky='W',
            padx=(0, self.PADX), 
            pady=self.PADY)
        
        # Elevation
        lbl = tk.Label(self.frame, 
            text='Elevation: ',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=1, 
            column=0,  
            sticky='W', 
            padx=self.PADX,
            pady=self.PADY)
        
        self.tb_el = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=9,
            textvariable=self.el_text,
            font=tkFont.Font(size=10))
        self.tb_el.grid(
            row=1, 
            column=1,
            sticky='W',
            padx=(0, self.PADX), 
            pady=self.PADY)
        
        # Range
        lbl = tk.Label(self.frame, 
            text='Range (km):',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=2, 
            column=0,  
            sticky='W', 
            padx=self.PADX,
            pady=self.PADY)

        self.tb_range = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=9,
            textvariable=self.range_text,
            font=tkFont.Font(size=10))
        self.tb_range.grid(
            row=2, 
            column=1,
            sticky='W',
            padx=(0, self.PADX), 
            pady=self.PADY)
        
        # Latitude
        lbl = tk.Label(self.frame, 
            text='Lat: ',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=0, 
            column=2,
            padx=self.PADX,
            pady=self.PADY)
        
        self.tb_lat = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=9,
            textvariable=self.lat_text,
            font=tkFont.Font(size=10))
        self.tb_lat.grid(
            row=0, 
            column=3,
            sticky='W',
            padx=(0, self.PADX), 
            pady=self.PADY)

        # Longitude
        lbl = tk.Label(self.frame, 
            text='Lon: ',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=1, 
            column=2,
            padx=self.PADX,
            pady=self.PADY)
            
        self.tb_lon = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=9,
            textvariable=self.lon_text,
            font=tkFont.Font(size=10))
        self.tb_lon.grid(
            row=1, 
            column=3,
            sticky='W',
            padx=(0, self.PADX), 
            pady=self.PADY)
        
        # Sunlight
        lbl = tk.Label(self.frame, 
            text='Sun: ',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=2, 
            column=2,
            padx=self.PADX,
            pady=self.PADY)
            
        self.tb_sun = tk.Entry(self.frame,
            state='disabled',
            disabledbackground=globals.DISABLED_BGCOLOR,
            disabledforeground='black',
            width=9,
            textvariable=self.sun_text,
            font=tkFont.Font(size=10))
        self.tb_sun.grid(
            row=2, 
            column=3,
            sticky='W',
            padx=(0, self.PADX), 
            pady=self.PADY)


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('WidgetAzElRange main program not implemented.')
   