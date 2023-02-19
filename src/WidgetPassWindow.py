###############################################################################
# WidgetPassWindow.py
# Author: Tom Kerr AB3GY
#
# WidgetPassWindow class for use with the pySatCat application.
# Provides a text window for displaying a table of satellite pass info.
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
from datetime import datetime, timedelta

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
# WidgetPassWindow class.
##############################################################################
class WidgetPassWindow(object):
    """
    WidgetPassWindow class for use with the pySatCat application.
    Provides a text window for displaying a table of satellite pass info.
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
        self.frame = None
        
        self.PAD = '  '  # Column spacing pad
        self.SWIDTH = 10 # Satellite name max width
        self.DWIDTH = 10 # Date column width
        self.TWIDTH = 8  # Time column width
        self.EWIDTH = 6  # Max elevation column width
        
        self.SFMT = '{:<' + str(self.SWIDTH) + '}' # Satellite name format string
        self.DFMT = '{:<' + str(self.DWIDTH) + '}' # Date format string
        self.TFMT = '{:<' + str(self.TWIDTH) + '}' # Time format string
        self.EFMT = '{:<' + str(self.EWIDTH) + '}' # Max elevation format string
        
        self.TITLE = self.SFMT.format('Satellite') + self.PAD \
            + self.DFMT.format('AOS Date') + self.PAD \
            + self.TFMT.format('AOS Time') + self.PAD \
            + self.EFMT.format('Max El') + self.PAD \
            + self.TFMT.format('LOS Time') + self.PAD \
            + self.TFMT.format('View Time') + '\n'
        
        self._widget_init()

    # ------------------------------------------------------------------------
    def clear(self):
        """
        Clear all text from the window.
        """
        self.frame.delete('1.0', tk.END)
    
    # ------------------------------------------------------------------------
    def add_pass_info(self, sat_name, aos_time, max_el, los_time):
        """
        Add a satellite pass info row.
        """
        name = self.SFMT.format(sat_name[:self.SWIDTH])  # Pad to width
        
        at = aos_time.datetime()
        aos_date_str = self.DFMT.format(at.strftime('%Y-%m-%d'))
        aos_time_str = self.TFMT.format(at.strftime('%H:%M:%S'))
        max_el_str = self.EFMT.format(('%0.1f' % max_el))
        lt = los_time.datetime()
        los_time_str = self.TFMT.format(lt.strftime('%H:%M:%S'))
        
        # Compute total time in view.
        tt = lt - at
        hours = int(tt.seconds / 3600)
        remain = tt.seconds - (hours * 3600)
        minutes = int(remain / 60)
        remain -= (minutes * 60)
        seconds = remain
        tot_time_str = ('%02d:' % hours) \
            + ('%02d:' % minutes) \
            + ('%02d' % seconds)
        
        
        info = name + self.PAD \
            + aos_date_str + self.PAD \
            + aos_time_str + self.PAD \
            + max_el_str + self.PAD \
            + los_time_str + self.PAD \
            + tot_time_str + '\n'
        self.frame.insert(tk.INSERT, info)
    
    # ------------------------------------------------------------------------
    def init_title(self):
        """
        Clear all text from the window and print the title row.
        """
        self.clear()
        self.frame.insert('1.1', self.TITLE)
  
    # ------------------------------------------------------------------------
    def _widget_init(self):
        """
        Internal method to create and initialize the UI widget.
        """
        my_font = tkFont.Font(family='Courier', size=10)
        
        self.frame = tk.Text(self.parent,
            height = int(2.4 * globals.NUM_PRESETS),
            width = 64,
            font = my_font)
        
        self.init_title()


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":

    sat_name = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    now = ephem.Date(datetime.utcnow())
    el = ephem.degrees(89.9)
    
    globals.init()
    root = tk.Tk()
    root.title('WidgetPassWindow test application')
    pw = WidgetPassWindow(root)
    pw.frame.pack()
    
    for i in range(1, 15, 2):
        name = sat_name[:i]
        pw.add_pass_info(name, now, el, now)
    
    root.mainloop()
   