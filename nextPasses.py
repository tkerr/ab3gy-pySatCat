###############################################################################
# nextPasses.py
# Author: Tom Kerr AB3GY
#
# Compute and print the next N passes of an earth-orbiting satellite from an 
# observer location.
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
import getopt
import os
import sys
from datetime import datetime

# Local environment init.
import _env_init

# Local packages.
from src.ConfigFile import ConfigFile
from src.SatelliteTracker import SatelliteTracker


##############################################################################
# Globals.
############################################################################## 
scriptname = os.path.basename(sys.argv[0])
scriptdir  = os.path.split(sys.argv[0])[0]

config  = ConfigFile()
tracker = SatelliteTracker()

PAD = '  '  # Column spacing pad
DWIDTH = 10 # Date column width
TWIDTH = 8  # Time column width
EWIDTH = 6  # Max elevation column width

DFMT = '{:<' + str(DWIDTH) + '}' # Date format string
TFMT = '{:<' + str(TWIDTH) + '}' # Time format string
EFMT = '{:<' + str(EWIDTH) + '}' # Max elevation format string


##############################################################################
# Functions.
############################################################################## 
def print_usage():
    """
    Print a usage statement and exit.
    """
    global scriptname
    print('Usage: ' + scriptname + ' [-ehn] sat tle')
    print('Compute and print the next N passes of an earth-orbiting satellite')
    print('from an observer location.')
    print('sat = The satellite name')
    print('tle = The two-line element (TLE) file to use')
    print('Options: ')
    print('  -e deg = Only print passes with elevation >= deg (default = 0)')
    print('  -h = Print this help message and exit')
    print('  -n N = Compute N number of passes (default = 10)')
    sys.exit(1)

# ------------------------------------------------------------------------
def init_observer():
    """
    Initialize the observer from the configuration file.
    """
    global config
    global tracker
    # Get the observer settings.
    config_changed = False
    section = 'OBSERVER'
    if not config.has_section(section):
        config.add_section(section)
        config_changed = True
    lat_str = config.get(section, 'LAT')
    if (lat_str == ''): 
        print('Observer latitude not found in config file.')
        lat_str = '0.0'
        config.set(section, 'LAT', lat_str)
        config_changed = True
    lon_str = config.get(section, 'LON')
    if (lon_str == ''): 
        print('Observer longitude not found in config file.')
        lon_str = '0.0'
        config.set(section, 'LON', lon_str)
        config_changed = True
    alt_str = config.get(section, 'ALT')
    if (alt_str == ''): 
        print('Observer altitude not found in config file.')
        alt_str = '0'
        config.set(section, 'ALT', alt_str)
        config_changed = True
    if config_changed:
        config.write()
    alt = int(alt_str)
    tracker.set_observer(lat_str, lon_str, alt)
    

##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":

    min_elevation = 0.0
    max_passes = 10
    sat_name = ''
    tle_filename = ''
    
    # Get command line options.
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'e:hn:')
    except (getopt.GetoptError) as err:
        print(str(err))
        sys.exit(1)
        
    for (o, a) in opts:
        if (o == '-e'):
            tmp_e = int(a)
            if (tmp_e > 0) and (tmp_e < 90):
                min_elevation = tmp_e
            else:
                print('Invalid elevation: ' + str(tmp_e))
        elif (o == '-h'):
            print_usage()
        elif (o == '-n'):
            tmp_n = int(a)
            if (tmp_n > 0):
                max_passes = tmp_n
            else:
                print('Invalid number of passes: ' + str(tmp_n))
            
    if (len(args) == 0):
        print('No satellite specified.')
        print_usage()
    if (len(args) < 2):
        print('No TLE file specified.')
        print_usage()
    
    sat_name = str(args[0]).upper().strip()
    tle_filename = str(args[1]).strip()
    
    # Read the configuration file.
    config.read()
    
    # Initialize the observer.
    init_observer()
    
    # Initialize the tracker satellite model.
    tle_path = os.path.join(config.ini_path, 'tle')
    tle_full_path = os.path.join(tle_path, tle_filename)
    ok = tracker.init_sat(sat_name, tle_full_path)
    if not ok:
        sys.exit(1)
    
    # Print the table title.
    print('Satellite: ' + sat_name)
    TITLE = DFMT.format('AOS Date') + PAD \
        + TFMT.format('AOS Time') + PAD \
        + EFMT.format('Max El') + PAD \
        + TFMT.format('LOS Time') + PAD \
        + TFMT.format('View Time')
    print(TITLE)
    
    # Compute the next N passes.
    start_time = ephem.Date(datetime.utcnow())
    for i in range(max_passes):
        (aos_time, aos_az, max_time, max_az, max_el, los_time, los_az) =  tracker.next_pass(start_time)
        start_time = los_time
        if (max_el >= min_elevation):
        
            # Format the pass information.
            at = aos_time.datetime()
            aos_date_str = DFMT.format(at.strftime('%Y-%m-%d'))
            aos_time_str = TFMT.format(at.strftime('%H:%M:%S'))
            max_el_str = EFMT.format(('%0.1f' % max_el))
            lt = los_time.datetime()
            los_time_str = TFMT.format(lt.strftime('%H:%M:%S'))
            
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
            
            # Print the formatted info.
            info = aos_date_str + PAD \
                + aos_time_str + PAD \
                + max_el_str + PAD \
                + los_time_str + PAD \
                + tot_time_str
            print(info)
    print()

