###############################################################################
# WidgetMapPlot.py
# Author: Tom Kerr AB3GY
#
# WidgetMapPlot class for use with the pySatCat application.
# Provides a world map and methods for plotting an observer and satellite track.
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
from datetime import datetime
import ephem
import os

# Matplotlib packages.
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Tkinter packages.
import tkinter as tk
import tkinter.font as tkFont
from tkinter.messagebox import showinfo

# Local packages.
import globals
from pySatCatUtils import *
from SatelliteTracker import SatelliteTracker

##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# WidgetMapPlot class.
##############################################################################
class WidgetMapPlot(object):
    """
    WidgetMapPlot class for use with the pySatCat application.
    Provides a world map and methods for plotting an observer and satellite track.
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
        self.parent = parent    # The parent GUI object
        self.frame = tk.Frame(parent)
        self.img = None         # The map image as a numpy array
        self.fig = None         # The matplotlib figure object
        self.ax = None          # The matplotlib axes object
        self.line1 = None       # Satellite track line 1
        self.line2 = None       # Satellite track line 2
        self.line3 = None       # Satellite track line 3
        self.line4 = None       # Satellite track line 4
        self.sat_marker = None  # Satellite marker
        self.obs_marker = None  # Observer marker
        
        self.mapfile = 'Blue_Marble_2002-1280x640.png'
        self.width = 0        # The map width (X-dimension)
        self.height = 0       # The map height (Y-dimension)
        self.dpi = 80         # Default image DPI
        self.xfactor = 1.0    # Used for scaling lat/lon to image coordinates
        self.yfactor = 1.0    # Used for scaling lat/lon to image coordinates
        self.step = ephem.minute / 2.0
        self.dt = ephem.minute / 6.0
        
        self.label_text = tk.StringVar(self.frame) 
        
        self.tracker = SatelliteTracker()
        
        self._widget_init()

    # ------------------------------------------------------------------------
    def init_satellite(self, sat_name, tle_file):
        """
        Initialize the satellite tracker for the particular satellite.
        """
        file_path = tle_file_path(tle_file)
        self.tracker.init_sat(sat_name, file_path)
        self.label_text.set('Sat Name: ' + sat_name + '  Lat:    Lon:')

    # ------------------------------------------------------------------------
    def read_map(self, filename):
        """
        Read the map file and set its width (X-dimension) and height (Y-dimension).
        """
        ok = False
        width = 0
        height = 0
        file_path = os.path.join(globals.config.ini_path, 'img')
        file_path = os.path.join(file_path, filename)
        try:
            self.img = plt.imread(file_path)
            self.width = self.img.shape[1]
            self.height = self.img.shape[0]
            self.xfactor = self.width / 360.0
            self.yfactor = self.height / -180.0
            ok = True
        except Exception as err:
            print('Error reading ' + str(filename) + ': ' + str(err))
        return ok

    # ------------------------------------------------------------------------
    def set_observer(self, lat, lon, elevation):
        """
        Set the observer location and plot it as a red dot on the map.
        """
        self.tracker.set_observer(lat, lon, elevation)
        (x, y) = self._get_xy(lat, lon)
        if self.obs_marker is not None:
            self.obs_marker.set_data(x, y)
        else:
            self.obs_marker, = self.ax.plot(x, y, 'ro')
        self.canvas.draw()
        self.canvas.flush_events()
    
    # ------------------------------------------------------------------------
    def update_track(self):
        """
        Re-plot the current satellite track.
        """
        if self.tracker.valid:
            (x1, y1, x2, y2, x3, y3, x4, y4) = self._get_track()
            
            if self.line1 is not None:
                self.line1.set_data(x1, y1)
            else:
                self.line1, = self.ax.plot(x1, y1, '-', color='yellow')

            if self.line2 is not None:
                self.line2.set_data(x2, y2)
            else:    
                self.line2, = self.ax.plot(x2, y2, '-', color='yellow')
            
            if self.line3 is not None:
                self.line3.set_data(x3, y3)
            else:    
                self.line3, = self.ax.plot(x3, y3, '-', color='yellow')
            
            if self.line4 is not None:
                self.line4.set_data(x4, y4)
            else:    
                self.line4, = self.ax.plot(x4, y4, '-', color='yellow')
        
            (az, el, range, velocity, lat, lon, sun) = self.tracker.compute(datetime.utcnow())
            (x, y) = self._get_xy(lat, lon)
            if self.sat_marker is not None:
                self.sat_marker.set_data(x, y)
            else:
                self.sat_marker, = self.ax.plot(x, y, 
                    marker='o',
                    color='orange', 
                    markeredgecolor='red',
                    markersize=10)
            
            self.canvas.draw()
            self.canvas.flush_events()
            msg = 'Sat Name: ' + self.tracker.name + \
                '    Lat: ' + ('%0.3f' % lat) + \
                '    Lon: ' + ('%0.3f' % lon)
            self.label_text.set(msg)
        

    # ------------------------------------------------------------------------
    def _update_track_handler(self):
        self.update_track()
        self.frame.after(10000, self._update_track_handler)

    # ------------------------------------------------------------------------
    def _get_track(self):
        """
        Compute the current satellite track.
        """
        # Initialization.
        xlist1 = []
        xlist2 = []
        xlist3 = []
        xlist4 = []
        ylist1 = []
        ylist2 = []
        ylist3 = []
        ylist4 = []
        t1 = 0
        t2 = 0
        t3 = 0
        t_now = ephem.date(datetime.utcnow())
        break_width = self.width * 0.25
        
        # Determine if satellite is headed North or South.
        lat1 = 0
        lat2 = 0
        (az, el, range, velocity, lat1, lon, sun) = self.tracker.compute(t_now)
        (az, el, range, velocity, lat2, lon, sun) = self.tracker.compute(t_now + self.dt)
        dlat = lat2 - lat1
        
        if (dlat < 0.0):
            # Headed South. Plot a max-max track.
            t1 = self._get_prev_max(t_now) - self.step
            t2 = self._get_next_min(t_now)
            t3 = self._get_next_max(t2) + self.step
        else:
            # Headed North. Plot a min-min track.
            t1 = self._get_prev_min(t_now) - self.step
            t2 = self._get_next_max(t_now)
            t3 = self._get_next_min(t2) + self.step

        # Compute the X,Y points for the t1-t3 track.
        last_x = -1000
        idx = 0
        t = t1
        lat_array = []
        lon_array = []
        while (t < t3):
            (az, el, range, velocity, lat, lon, sun) = self.tracker.compute(t)
            (x,y) = self._get_xy(lat, lon)
            
            # Try to avoid drawing a horizontal line across the map.
            # May not always be possible at extreme latitudes.
            # Break into multiple plots if a large horizontal sweep is detected.
            if (last_x < 0): last_x = x
            if (abs(x - last_x) >= break_width): idx += 1
            
            if (idx == 0):
                xlist1.append(x)
                ylist1.append(y)
            elif (idx == 1):
                xlist2.append(x)
                ylist2.append(y)
            elif (idx == 2):
                xlist3.append(x)
                ylist3.append(y)
            else:
                xlist4.append(x)
                ylist4.append(y)
            last_x = x
            t += self.step
        
        return (xlist1, ylist1, xlist2, ylist2, xlist3, ylist3, xlist4, ylist4)

    # ------------------------------------------------------------------------
    def _get_prev_max(self, t):
        """
        Get time of previous maximum latitude.
        """
        lat_max = -99.0
        t_max = 0
        (az, el, range, velocity, lat, lon, sun) = self.tracker.compute(t)
        while (lat > lat_max):
            lat_max = lat
            t_max = t
            t -= self.step
            (az, el, range, velocity, lat, lon, sun) = self.tracker.compute(t)
        #print('prev max: ', ephem.Date(t_max), str(lat_max))
        return t_max

    # ------------------------------------------------------------------------
    def _get_next_max(self, t):
        """
        Get time of next maximum latitude.
        """
        lat_max = -99.0
        t_max = 0
        (az, el, range, velocity, lat, lon, sun) = self.tracker.compute(t)
        while (lat > lat_max):
            lat_max = lat
            t_max = t
            t += self.step
            (az, el, range, velocity, lat, lon, sun) = self.tracker.compute(t)
        #print('next max: ', ephem.Date(t_max), str(lat_max))
        return t_max

    # ------------------------------------------------------------------------
    def _get_prev_min(self, t):
        """
        Get time of previous minimum latitude.
        """
        lat_min = 99.0
        t_min = 0
        (az, el, range, velocity, lat, lon, sun) = self.tracker.compute(t)
        while (lat < lat_min):
            lat_min = lat
            t_min = t
            t -= self.step
            (az, el, range, velocity, lat, lon, sun) = self.tracker.compute(t)
        #print('prev min: ', ephem.Date(t_min), str(lat_min))
        return t_min
    
    # ------------------------------------------------------------------------
    def _get_next_min(self, t):
        """
        Get time of next minimum latitude.
        """
        lat_min = 99.0
        t_min = 0
        (az, el, range, velocity, lat, lon, sun) = self.tracker.compute(t)
        while (lat < lat_min):
            lat_min = lat
            t_min = t
            t += self.step
            (az, el, range, velocity, lat, lon, sun) = self.tracker.compute(t)
        #print('next min: ', ephem.Date(t_min), str(lat_min))
        return t_min

    # ------------------------------------------------------------------------
    def _get_xy(self, lat, lon):
        """
        Convert lat/lon to X,Y coordinates for plotting.
        """
        x = (lon + 180.0) * self.xfactor
        y = (lat - 90.0) * self.yfactor
        return (x, y)
    
    # ------------------------------------------------------------------------
    def _about_map_handler(self):
        """
        Map button handler.
        """
        msg  = 'NASA Visible Earth: Blue Marble: Land Surface, Shallow Water, and Shaded Topography, Public Domain\n'
        msg += 'By NASA’s Terra satellite for the MODIS imageries, combined by Meow.\n'
        msg += 'Credit: NASA Goddard Space Flight Center\n'
        msg += 'For full attribution, see:\n'
        msg += 'https://commons.wikimedia.org/w/index.php?curid=50497070'
        showinfo(
            title='Blue Marble Map Image',
            message=msg)
    
    # ------------------------------------------------------------------------
    def _widget_init(self):
        """
        Internal method to create and initialize the UI widget.
        """
        plt.ion
        self.read_map(self.mapfile)
        
        # Create a label with the satellite name and lat/lon.
        self.label_text.set('Sat Name:    Lat:    Lon:')
        lbl = tk.Label(
            self.frame, 
            textvariable=self.label_text,
            font=tkFont.Font(size=10))
        lbl.grid(row=0, column=0, padx=6, pady=3, sticky='W')
        
        # Create a button for the map attribution.
        btn = tk.Button(
            self.frame,
            text='About...', 
            width=10,
            command=self._about_map_handler)
        btn.grid(row=0, column=1, padx=6, pady=3, sticky='E')
        
        # Create a figure using the map image.
        xsize = self.width / self.dpi
        ysize = self.height / self.dpi
        self.fig = Figure(
            figsize=(xsize, ysize), 
            dpi=self.dpi)
        self.fig.subplots_adjust(0,0,1,1) # This removes the white border around the image
        self.ax = self.fig.add_subplot()
        self.ax.set_axis_off()
        self.ax.imshow(self.img)

        # Place the map image in a Tk canvas.
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        widget = self.canvas.get_tk_widget()
        widget.config(borderwidth=0)
        widget.grid(row=1, column=0, columnspan=2, padx=0, pady=0)
        self.frame.after(1000, self._update_track_handler)


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":

    globals.init()
    root = tk.Tk()
    root.title('WidgetMapPlot test application')
    wmp = WidgetMapPlot(root)
    wmp.frame.grid(row=0, column=0, padx=3, pady=3)
    set_geometry(root)
    wmp.set_observer(40.414554, -79.704017, 347)
    wmp.init_satellite('ISS', 'nasabare.txt')
    root.mainloop()
   