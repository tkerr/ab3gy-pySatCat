###############################################################################
# WidgetClock.py
# Author: Tom Kerr AB3GY
#
# WidgetClock class for use with the pySatCat application.
# Provides a UTC date/time display.
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

# Tkinter packages.
import tkinter as tk
import tkinter.font as tkFont

# Local packages.


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# WidgetClock class.
##############################################################################
class WidgetClock(object):
    """
    WidgetClock class for use with the pySatCat application.
    Provides a UTC date/time display.
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
        self.frame = tk.Frame(parent)
        self.clock = None
        self.time_text = tk.StringVar(self.frame) 
        self._widget_init()

    # ------------------------------------------------------------------------
    def update(self):
        """
        Update the date and time.
        """
        now = datetime.utcnow()
        time_str = now.strftime('%Y-%m-%d %H:%M:%S UTC')
        self.time_text.set(time_str)
        self.clock.after(1000, self.update)

    # ------------------------------------------------------------------------
    def _widget_init(self):
        """
        Internal method to create and initialize the UI widget.
        """
        self.clock = tk.Label(
            self.frame, 
            textvariable=self.time_text,
            font=tkFont.Font(size=10))
        self.clock.grid(
            row=0, 
            column=0,
            padx=3,
            pady=3)
        self.clock.after(1000, self.update)
        


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":

    root = tk.Tk()
    root.title('WidgetClock test application')
    wc = WidgetClock(root)
    wc.window.pack()
    root.mainloop()
   