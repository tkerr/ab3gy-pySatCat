###############################################################################
# ConfigFile.py
# Author: Tom Kerr AB3GY
#
# ConfigFile class.
# Implements a .INI configuration file for saving/restoring configuration
# parameters. File format is similar to Microsoft Windows .INI files.
# Parameters are stored in sections as key/value pairs.
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
import sys
import configparser
import datetime

# Local packages.


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################


##############################################################################
# ConfigFile class.
##############################################################################
class ConfigFile(object):
    """
    ConfigFile class.
    Implements a .INI configuration file for saving/restoring configuration
    parameters. File format is similar to Microsoft Windows .INI files.
    Parameters are stored in sections as key/value pairs.
    """
    
    # ------------------------------------------------------------------------
    def __init__(self):
        """
        Class constructor.
    
        Parameters
        ----------
        None.
        
        Returns
        -------
        None.
        """
        # The .INI file should be in the same directory as the application script.
        self.ini_path = os.path.dirname(os.path.realpath(sys.argv[0]))

        # Get the basename of the .INI file from the script name.
        scriptname = os.path.basename(sys.argv[0])
        self.ini_base = os.path.splitext(scriptname)[0]

        # Construct the full .INI file name.
        self.ini_ext = '.ini'
        self.ini_file = os.path.join(self.ini_path, self.ini_base + self.ini_ext)
        
        # The configuration file parser object.
        self.config = configparser.ConfigParser()

    # ------------------------------------------------------------------------
    def get(self, section, key):
        """
        Get the specified parameter from the specified section.
        
        Parameters
        ----------
        section : str
            The config file section name.
        key : str
            The parameter key.
        
        Returns
        -------
        value : str
            The parameter value as a string if found, or an empty string 
            if not found.
        """
        value = ''
        try:
            value = str(self.config[str(section)][str(key)])
        except Exception as err:
            #print(str(err))
            pass
        return value
    
    # ------------------------------------------------------------------------
    def set(self, section, key, value):
        """
        Set the specified parameter value in the specified section.
        Note that the write() method must be called to save the parameter
        to the config file.
        
        Parameters
        ----------
        section : str
            The config file section name.
        key : str
            The parameter key.
        value : object
            The parameter value.  Attempts to convert to a string.
        
        Returns
        -------
        None.
        """
        try:
            self.config.set(str(section), str(key), str(value))
        except Exception as err:
            print(str(err))
            pass

    # ------------------------------------------------------------------------
    def has_section(self, section):
        """
        Return True if the specified section exists, False otherwise.
        
        Parameters
        ----------
        section : str
            The config file section name.

        Returns
        -------
        True if the section exists, False otherwise.
        """
        found = (str(section) in self.config.sections())
        return found

    # ------------------------------------------------------------------------
    def add_section(self, section):
        """
        Add the specified section to the config file.
        Note that the write() method must be called to save the section
        to the config file.
        
        Parameters
        ----------
        section : str
            The config file section name.

        Returns
        -------
        None.
        """
        try:
            self.config.add_section(str(section))
        except Exception as err:
            print(str(err))
            pass
    
    # ------------------------------------------------------------------------
    def read(self, create=True):
        """
        Read the .INI file and get the config parameters.
        Optionally create the file if it does not exist (default = create it).
        
        Parameters
        ----------
        create = bool
            Optional flag to create the config file if it does not exist.
            Default = create it.
        
        Returns
        -------
        (status, err_msg) : tuple
            status : bool
                True if config file read was successful, False otherwise.
            err_msg : str
                Error message if an error occurred.
        """
        status = False
        err_msg = ''

        # See if the config file exists.
        if os.path.isfile(self.ini_file):
            try:
                self.config.read(self.ini_file)
                status = True
            except Exception as err:
                status = False
                err_msg = str(err)
        elif create:
            # .INI file does not exist.
            # Create it.
            (status, err_msg) = self._create()
            if status:
                (status, err_msg) = self.write()
        return (status, err_msg)

    # ------------------------------------------------------------------------
    def write(self):
        """
        Write parameters to the .INI file.  Will create it if it does not exist.
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        (status, err_msg) : tuple
            status : bool
                True if config file write was successful, False otherwise.
            err_msg : str
                Error message if an error occurred.
        """
        status = True
        err_msg = ''
        file_out = None
        
        # See if the config file exists.
        if not os.path.isfile(self.ini_file):
            (status, err_msg) = self._create()
            if not status:
                return (status, err_msg)

        # Write the file.
        try:
            file_out = open(self.ini_file, 'w')
            self.config.write(file_out)
            status = True
        except Exception as err:
            status = False
            err_msg = str(err)
        self._close(file_out)
        
        return (status, err_msg)
        
    # ------------------------------------------------------------------------
    def _close(self, file):
        """
        Close the .INI file.  
        All errors are ignored.
        
        Parameters
        ----------
        file : an open file object.
        
        Returns
        -------
        None.
        """
        try:
            file.close()
        except Exception:
            pass

    # ------------------------------------------------------------------------
    def _create(self):
        """
        Create an empty .INI file.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        (status, err_msg) : tuple
            status : bool
                True if config file creation was successful, False otherwise.
            err_msg : str
                Error message if an error occurred.
        """
        status = False
        err_msg = ''
        file_in = None
        try:
            file_in = open(self.ini_file, 'w')
            status = True
        except Exception as err:
            err_msg = str(err)
            
        self._close(file_in)
        return (status, err_msg)


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    
    status = ''
    errmsg = ''
    section = 'DATE-TIME'
    my_config = ConfigFile()
    print('INI file: ' + my_config.ini_file)
    
    (status, errmsg) = my_config.read()
    if not status:
        print('Error reading ' + my_config.ini_file + ': ' + errmsg)
    
    # Print the config file section names.
    print('Config file sections: ', end='')
    print(my_config.config.sections())
    
    # Get stored date and time.
    config_date = my_config.get(section, 'DATE')
    print('Stored date: "' + config_date + '"')
    config_time = my_config.get(section, 'TIME')
    print('Stored time: "' + config_time + '"')
    
    # Get current date and time.
    now = datetime.datetime.now()
    config_date = str(now.year) + ('-%02d' % now.month) + ('-%02d' % now.day)
    print('New date: ' + config_date)
    config_time = ('%02d' % now.hour) + (':%02d' % now.minute) + (':%02d' % now.second)
    print('New time: ' + config_time)
    
    # Update the config file.
    if not my_config.has_section(section):
        print('Creating section "' + section + '"')
        my_config.add_section(section)
    my_config.set(section, 'DATE', config_date)
    my_config.set(section, 'TIME', config_time)
    (status, errmsg) = my_config.write()
    if not status:
        print('Error writing ' + my_config.ini_file + ': ' + errmsg)
