###############################################################################
# DlgConfigTLE.py
# Author: Tom Kerr AB3GY
#
# DlgConfigTLE class for use with the pySatCat application.
# Implements a dialog box for configuring Two Line Element (TLE) data sources.
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
from tkinter import ttk, filedialog

# HTTP packages.
import urllib.request
import urllib.error
import ssl

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
# TleGroupVar class.
##############################################################################
class TleGroupVar(object):
    """
    Container object for TLE element group variables.
    """
    # ------------------------------------------------------------------------
    def __init__(self, root):
        self.url   = tk.StringVar(root)
        self.file  = tk.StringVar(root)


##############################################################################
# DlgConfigTLE class.
##############################################################################
class DlgConfigTLE(object):
    """
    DlgConfigStation class for use with the pySatCat application.
    Implements a dialog box for configuring Two Line Element (TLE) data sources.
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
        self.dlg_config_tle = None  # The dialog box
        self.tle_group_vars = []    # The list of TLE element group variables
        
        # HTTP request variables.
        self._status   = 0   # HTML request status
        self._body     = ''  # HTML response body
        self._info     = ''  # HTML request/response info
        self._reqUrl   = ''  # HTML request URL
        self._rspUri   = ''  # HTML response URL, used to detect redirection
        self._timeout  = 5   # HTML request timeout in seconds
        
        # Initialize the list of TLE element groups.
        for i in range(globals.TLE_NUM_GROUPS):
            self.tle_group_vars.append(TleGroupVar(self.root))
        
        self._dlg_init()

    # ------------------------------------------------------------------------
    def _dlg_init(self):
        """
        Internal method to create and initialize the dialog box.
        """
        # Do not authenticate the SSL certificate, otherwise the HTTP request may fail.
        ssl._create_default_https_context = ssl._create_unverified_context
    
        self.dlg_config_tle = tk.Toplevel(self.root)
        self.dlg_config_tle.title('TLE Element Group Source Configuration')

        # Header row labels.
        ttk.Label(self.dlg_config_tle, text=' ').grid(row=0, column=0, padx=3, pady=3)
        ttk.Label(self.dlg_config_tle, text='URL').grid(row=0, column=1, padx=3, pady=3)
        ttk.Label(self.dlg_config_tle, text='Local File').grid(row=0, column=2, padx=3, pady=3)

        row = 0
        for i in range(globals.TLE_NUM_GROUPS):
            row = i + 1
           
            # Initialize text variables with current configuration.
            section = 'TLE' + str(row)
            self.tle_group_vars[i].url.set(globals.config.get(section, 'URL'))
            self.tle_group_vars[i].file.set(globals.config.get(section, 'FILE'))
           
            # Row number label.
            ttk.Label(self.dlg_config_tle, text=str(row)).grid(row=row, column=0, padx=3, pady=6)

            # Source URL.
            tb = ttk.Entry(self.dlg_config_tle,
                textvariable=self.tle_group_vars[i].url,
                width=50)
            tb.grid(row=row, column=1, padx=3, pady=6)
           
            # Local file name.
            tb = ttk.Entry(self.dlg_config_tle,
                textvariable=self.tle_group_vars[i].file,
                width=15)
            tb.grid(row=row, column=2, padx=3, pady=6)

        # Create a frame to contain the buttons.
        row += 1
        btn_frame = tk.Frame(self.dlg_config_tle)

        # OK button.
        btn_ok = tk.Button(btn_frame, 
            text='OK', 
            width=10, 
            command=self._dlg_config_tle_ok)
        btn_ok.grid(row=0, column=0, sticky='EW', padx=6, pady=6)
        
        # Cancel button.
        btn_cancel = tk.Button(btn_frame, 
            text='Cancel', 
            width=10, 
            command=self.dlg_config_tle.destroy)
        btn_cancel.grid(row=0, column=1, sticky='EW', padx=6, pady=6)
        
        # Update All button.
        btn_update = tk.Button(btn_frame,
            text='Update All',
            width=10,
            command=self._dlg_config_tle_update)
        btn_update.grid(row=0, column=2, sticky='EW', padx=6, pady=6)
        
        # Add the button frame.
        btn_frame.grid(
            row=row, 
            column=0, 
            columnspan=3,
            padx=6,
            pady=6)

        self.dlg_config_tle.grab_set() # Make the dialog modal
        
        # Set the proper window size and center it on the screen.
        set_geometry(self.dlg_config_tle)

    # ------------------------------------------------------------------------
    def _dlg_config_tle_update(self):
        """
        Dialog box Update All button handler.
        """
        status = False
        errmsg = ''
        for i in range(globals.TLE_NUM_GROUPS):
            url = self.tle_group_vars[i].url.get()
            file = self.tle_group_vars[i].file.get()
            if (len(url) > 0):
                print('Updating ' + str(url))
                status = self._http_request(url)
                if status:
                    (status, errmsg) = self._write_tle_file(file, self._body)
                    if status:
                        print('Successfully updated ' + file + '.')
                    else:
                        print('Error writing "' + file + '": ' + errmsg)
                else:
                    print('HTTP request failed for ' + url + ': ' + self._info)

    # ------------------------------------------------------------------------
    def _dlg_config_tle_ok(self):
        """
        Dialog box OK button handler.
        """
        for i in range(globals.TLE_NUM_GROUPS):
            row = i + 1
            section = 'TLE' + str(row)
            if not globals.config.has_section(section):
                globals.config.add_section(section)
            globals.config.set(section, 'URL',  self.tle_group_vars[i].url.get())
            globals.config.set(section, 'FILE', self.tle_group_vars[i].file.get())
        
        # Save parameters to .INI file.
        globals.config.write()

        self.dlg_config_tle.destroy()

    # ------------------------------------------------------------------------    
    def _http_request(self, uri):
        """
        Perform an HTTP request.

        Parameters
        ----------
        uri : str
            The HTTP request URI.
        
        Returns
        -------
        bool : True if request completed successfully, False otherwise.
        """
        ok = False
        self._body = ""
        self._rspUri = uri
        try:
            resp = urllib.request.urlopen(uri, timeout=self._timeout)   # Returns a HTTPResponse object
            self._status = resp.status
            self._info   = resp.info()
            self._rspUri = resp.geturl() # Look for redirection
            self._body   = resp.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            self._status = e.code
            self._info   = e.reason
        except urllib.error.URLError as e:
            self._status = e.errno
            self._info   = str(e.reason) # This could be text or another exception object
        except Exception as e:
            self._status = -1
            self._info   = str(e)
            
        if (self._status == 200): ok = True
        return ok

   # ------------------------------------------------------------------------    
    def _write_tle_file(self, filename, data):
        """
        Write data to a TLE file.

        Parameters
        ----------
        filename : str
            The local filename to write.
        
        body : str
            The file data to write.
        
        Returns
        -------
        (status, errmsg) : tuple
            status : bool : True if file write completed successfully, False otherwise.
            errmsg : str : An error message if the file write failed.
        """
        status = False
        errmsg = ''
        fp = None
        
        # Create the full file path.
        filepath = tle_file_path(filename)
        
        try:
            # Open the file and write the data.
            fp = open(filepath, 'w')
            fp.write(data)
            status = True
        except Exception as err:
            status = False
            errmsg = str(err)
        
        # Close the file.
        try:
            if fp is not None: close(fp)
        except Exception:
            pass

        return (status, errmsg)


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('DlgConfigTLE main program not implemented.')
