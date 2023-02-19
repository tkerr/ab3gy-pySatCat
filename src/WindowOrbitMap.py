###############################################################################
# WindowOrbitMap.py
# Author: Tom Kerr AB3GY
#
# WindowOrbitMap class for use with the pySatCat application.
# Implements a window for displaying the satellite orbit map.
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

# Local packages.
import globals
from src.pySatCatUtils import *
from src.WidgetMapPlot import WidgetMapPlot

##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################


##############################################################################
# WindowOrbitMap class.
##############################################################################
class WindowOrbitMap(object):
    """
    WindowOrbitMap class for use with the pySatCat application.
    Implements a window for displaying the satellite orbit map.
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
        self.root = root  # The root window
        self.frame = tk.Toplevel(self.root)
        self.map = None  # The WidgetMapPlot object
        self._window_init()

    # ------------------------------------------------------------------------
    def _window_init(self):
        """
        Internal method to create and initialize the window.
        """
        self.frame.title('Satellite Orbit Map')
        self.map = WidgetMapPlot(self.frame)
        self.map.frame.grid(row=0, column=0, padx=3, pady=3)
        self.frame.protocol("WM_DELETE_WINDOW", lambda: self._window_close())
        set_geometry(self.frame)

    # ------------------------------------------------------------------------
    def _window_close(self):
        """
        Close the window.
        """
        globals.window_orbit_map = None
        self.frame.destroy()


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('WindowOrbitMap main program not implemented.')
