###############################################################################
# TrackerThread.py
# Author: Tom Kerr AB3GY
#
# Real-time satellite tracking thread for the pySatCat application.
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
import os
import sys
import threading
import time

# Local packages.
import globals
from pySatCatUtils import *
from SatelliteTracker import SatelliteTracker


##############################################################################
# Globals.
##############################################################################

thread_startup = True
backup_step = ephem.minute * 10.0


##############################################################################
# Functions.
##############################################################################

# ------------------------------------------------------------------------
def tracker_thread():
    """
    Real-time satellite tracking thread.
    Re-computes satellite parameters at periodic intervals.
    """
    global thread_startup
    globals.tracker_thread_active = True
    print('Tracker thread starting.')
    
    # Give the Tk main loop time to start.
    time.sleep(1.0)
    
    while globals.tracker_thread_run:
    
        new_pass = False
        now = ephem.Date(datetime.utcnow())
        
        # Compute next pass information and current parameters.
        for i in range(globals.NUM_PRESETS):
            
            tracker = globals.tracker_list[i]
            if tracker.valid:
                # Set a flag if next pass information has changed.
                if (now > tracker.los_time):
                    tracker.next_pass(now)
                    new_pass = True

                # Compute current satellite parameters.
                (az, el, sat_range, velocity, lat, lon, sun) = tracker.compute(now)
                
                # Change the preset button background if the satellite is in view.
                if (el > 0.0):
                    globals.preset_list[i].set_bg_color(globals.INVIEW_BGCOLOR)
                else:
                    globals.preset_list[i].set_bg_color(globals.PRESET_BGCOLOR)
                
                # Special case at thread startup:
                # If the satellite is currently in view, then the 'next pass' will
                # compute the pass after this.  If this is the case, back up the 
                # time until we get the current pass.
                if thread_startup and (el > 0.0):
                    e = el
                    t = now
                    while (e > 0.0):
                        t -= backup_step
                        tracker.next_pass(t)
                        (x, e, x, x, x, x, x) = tracker.compute(t)

                # Display parameters if this is the selected preset.
                if ((i+1) == globals.selected_preset):
                    globals.widget_az_el_range.set_pass_info(az, el, sat_range, lat, lon, sun)
                    globals.widget_sat_info.set_name(tracker.name)
                    globals.widget_sat_info.set_pass_info(
                        tracker.aos_time, tracker.aos_az,
                        tracker.max_time, tracker.max_az, tracker.max_el,
                        tracker.los_time, tracker.los_az)

                    # Set widget background colors based on satellite in view.
                    bg_color = globals.DISABLED_BGCOLOR
                    if (el > 0.0): bg_color = globals.INVIEW_BGCOLOR
                    globals.widget_az_el_range.set_bg_color(bg_color)
                    globals.widget_sat_info.set_bg_color(bg_color)

                    # Compute Doppler shift.
                    frac = (float(velocity) / 3.0E8)
                    ud = globals.widget_desired_freq.uplink_float()
                    uc = ud * (1.0 + frac)
                    globals.widget_corrected_freq.set_uplink(uc)
                    globals.rig_cat_uplink_corrected = uc
        
                    dd = globals.widget_desired_freq.downlink_float()
                    dc = dd * (1.0 - frac)
                    globals.widget_corrected_freq.set_downlink(dc)
                    globals.rig_cat_downlink_corrected = dc

        # Update the satellite pass window if anything changed.
        if new_pass:
            
            # Step 1: Build a list of satellites to display in the window.
            sat_list = []
            pass_info_list = []
            for i in range(globals.NUM_PRESETS):
                tracker = globals.tracker_list[i]
                if tracker.valid:
                    if tracker.name not in sat_list:
                        sat_list.append(tracker.name)
                        t = (tracker.aos_time, tracker.max_el, tracker.los_time, tracker.name)
                        pass_info_list.append(t)

            # Step 2: Sort the list by AOS time and display it.
            globals.widget_pass_window.init_title()
            sorted_pass_info = sorted(pass_info_list)
            for t in sorted_pass_info:
                    globals.widget_pass_window.add_pass_info(
                        t[3], # Name
                        t[0], # AOS time
                        t[1], # Max El
                        t[2]) # LOS time
            
            # Update countdown timer.
            globals.widget_countdown.set_aos(sorted_pass_info[0][0])

        thread_startup = False
        time.sleep(1.0)
    
    print('Tracker thread exiting.')
    globals.tracker_thread_active = False

# ------------------------------------------------------------------------
def start_tracker_thread():
    """
    Start the real-time satellite tracking thread.
    """
    globals.tracker_thread_run = True
    globals.tracker_thread_fn = threading.Thread(target=tracker_thread)
    globals.tracker_thread_fn.start()

# ------------------------------------------------------------------------
def stop_tracker_thread():
    """
    Stop the real-time satellite tracking thread.
    """
    globals.tracker_thread_run = False

