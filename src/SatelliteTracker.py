###############################################################################
# SatelliteTracker.py
# Author: Tom Kerr AB3GY
#
# SatelliteTracker class for use with the pySatCat application.
# Provides methods and data for tracking earth-orbit satellites.
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
import ephem
import traceback
from datetime import datetime
import math

# Local packages.


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# SatelliteTracker class.
##############################################################################
class SatelliteTracker(object):
    """
    SatelliteTracker class for use with the pySatCat application.
    Provides methods and data for tracking earth-orbit satellites.
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
        self.model = None
        self.name = ''
        self.observer = ephem.Observer()
        self.tle_filename = ''
        self.valid = False
        
        # Next pass information.
        self.aos_time = ephem.Date(0)
        self.aos_az = ephem.degrees(0)
        self.max_time = ephem.Date(0)
        self.max_az = ephem.degrees(0)
        self.max_el = ephem.degrees(0)
        self.los_time = ephem.Date(0)
        self.los_az = ephem.degrees(0)
        
        self.F = 0.00335281066474748071984552861852 # WGS-84 Earth flattening factor (1/298.257223563)
        self.FLATTEN = 1.0 / ((1.0 - self.F)**2)

    # ----------------------------------------------------------------------------    
    def _print_msg(self, msg):
        """
        Print a formatted message with traceback to calling method/function.

        Parameters
        ----------
        msg : str
            The message text to print.
        
        Returns
        -------
        None
        """
        cl = type(self).__name__                         # This class name
        fn = str(traceback.extract_stack(None, 2)[0][2]) # Calling function name
        print(cl + '.' + fn + ': ' + msg)
    
    # ------------------------------------------------------------------------
    def set_observer(self, lat, lon, elevation):
        """
        Set the observer location.
        """
        try:
            self.observer.lat = lat
            self.observer.lon = lon
            self.observer.elevation = elevation
        except Exception as err:
            self._print_msg(str(err))

    # ------------------------------------------------------------------------
    def init_sat(self, name, filename=None):
        """
        Initialize a satellite model.
        
        Parameters
        ----------
        name : str
            The name of the satellite to initialize.
            
        filename : str
            Optional name of the TLE element group file containing
            the satellite.

        Returns
        -------
            True if initialization successful, False otherwise.
        """
        self.valid = False
        tle_found = False
        tle_read = False
        if filename is not None: self.set_tle_filename(filename)

        self.name = name.strip().upper()
        line1 = ''
        line2 = ''
        
        # Iterate through the file to get the TLE data.
        try:
            with open(self.tle_filename, 'r') as file:
                for line in file:
                    line_new = line.strip().upper()
                    if line_new.startswith('0'):  # 3le format
                        line_new = line_new[2:]
                    if (len(line_new) > 0):
                        # Shift the file lines.
                        sat_name = line1
                        line1 = line2
                        line2 = line_new
                        if (self.name == sat_name):
                            if line1.startswith('1'):
                                if line2.startswith('2'):
                                    tle_found = True
                                    break
        except Exception as err:
            self._print_msg(str(err))
        
        # Initialize the satellite model.
        try:
            self.model = ephem.readtle(self.name, line1, line2)
            tle_read = True
        except Exception as err:
            self._print_msg(str(err))
        
        self.valid = tle_found and tle_read
        if not self.valid:
            self._print_msg('Unable to initialize satellite model for ' + self.name)
        return self.valid

    # ------------------------------------------------------------------------
    def set_tle_filename(self, filename):
        """
        Set the TLE element group filename.
        """
        self.tle_filename = filename

    # ------------------------------------------------------------------------
    def sat_list_from_file(self, filename):
        """
        Open a TLE element group file and build a list of satellite names
        from it.
        
        Parameters
        ----------
        filename : str
            The name of the TLE element group file.

        Returns
        -------
        sat_list : list
            A list of satellite names as strings.
        """
        sat_list = []
        self.set_tle_filename(filename)
        
        line1 = ''
        line2 = ''
        
        # Iterate through the file.
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line_new = line.strip().upper()
                    if line_new.startswith('0'):  # 3le format
                        line_new = line_new[2:]
                    if (len(line_new) > 0):
                        # Shift the file lines.
                        name = line1
                        line1 = line2
                        line2 = line_new
                        if line1.startswith('1'):
                            if line2.startswith('2'):
                                sat_list.append(name)
        except Exception as err:
            self._print_msg(str(err))
        return sat_list
    
    # ------------------------------------------------------------------------
    def compute(self, date_time=None):
        """
        Compute the next set of satellite parameters.
        """
        az = ephem.degrees(0)
        el = ephem.degrees(0)
        range = 0.0
        velocity = 0.0
        
        if date_time is None:
            self.observer.date = datetime.utcnow()
        else:
            self.observer.date = date_time

        if self.valid:
            try:
                # Convert angles from radians to degrees.
                # Convert range to km.
                self.model.compute(self.observer)
                az = math.degrees(self.model.az)
                el = math.degrees(self.model.alt)
                range = self.model.range / 1000.0
                velocity = self.model.range_velocity
                # Comparison to N2YO.com and other models indicates that flattening
                # is already taken into account in the computation.
                #x1 = math.tan(self.model.sublat)
                #x2 = math.atan(self.FLATTEN * x1)
                #lat = math.degrees(x2)
                lat = math.degrees(self.model.sublat)
                lon = math.degrees(self.model.sublong)
                sun = 1
                if self.model.eclipsed: sun = 0
            except Exception as err:
                self._print_msg(str(err))
        
        return (az, el, range, velocity, lat, lon, sun)

    # ------------------------------------------------------------------------
    def next_pass(self, date_time=None):
        """
        Compute the next pass informaton.
        date_time is expected to be an ephem.Date object
        """
        if date_time is not None:
            self.observer.date = date_time
        
        if self.valid:
            try:
                # The next_pass() method gets most of the info.
                # Convert angles from radians to degrees.
                info = self.observer.next_pass(self.model)
                self.aos_time = info[0]
                self.aos_az = math.degrees(info[1])
                self.max_time = info[2]
                self.max_el = math.degrees(info[3])
                self.los_time = info[4]
                self.los_az = math.degrees(info[5])
            
                # Calculate azimuth and max elevation.
                self.observer.date = self.max_time
                self.model.compute(self.observer)
                self.max_az = math.degrees(self.model.az)

            except Exception as err:
                self._print_msg(str(err))

        return (self.aos_time, self.aos_az, self.max_time, self.max_az, 
            self.max_el, self.los_time, self.los_az)
 
 
##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('SatelliteTracker main program not implemented.')
   