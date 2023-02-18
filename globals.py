###############################################################################
# globals.py
# Author: Tom Kerr AB3GY
#
# Global objects and data for the pySatCat application.
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
import time

# Tkinter packages.
import tkinter as tk

# Local packages.
from ConfigFile import ConfigFile
from CatControlThread import stop_cat_control_thread
from TrackerThread import stop_tracker_thread

##############################################################################
# Globals.
##############################################################################
APP_NAME = 'pySatCat'
APP_VERSION = '0.1'
APP_COPYRIGHT = '2022'

CAT_ENABLED_BGCOLOR = '#98FB98'  # Background color when CAT control is enabled
CAT_DISABLED_BGCOLOR = '#DDDDDD' # Background color when CAT control is disabled
DISABLED_BGCOLOR = '#EEE8AA'  # Background color for disable text entry widgets
INVIEW_BGCOLOR = '#98FB98'    # Background color for some text boxes when satellite is in view
PRESET_BGCOLOR = '#CCCCCC'    # Preset button normal background color
NUM_PRESETS = 8               # Number of satellite preset buttons
TLE_NUM_GROUPS = 5            # The number of TLE element groups to support

root = None                   # The root window
config = None                 # The config file object
cat_control = None            # The CAT control object
app_menu = None               # The main application menu
widget_desired_freq = None    # The desired frequency GUI widget
widget_corrected_freq = None  # The corrected frequency GUI widget
widget_az_el_range = None     # The Az-El-Range GUI widget
widget_pass_window = None     # The satellite pass table window
widget_sat_info = None        # The satellite pass info summary GUI widget
widget_cat_control = None     # The CAT control GUI widget
widget_countdown = None       # Countdown to next satellite pass GUI widget
window_orbit_map = None       # The satellite orbit map window

preset_list = []              # List of satellite preset objects
tracker_list = []             # List satellite tracker objects
selected_preset = 0           # The currently selected satellite preset

rig_cat = None                    # The rig CAT control object
rig_cat_enabled = False           # Rig CAT control enable/disable flag
rig_cat_uplink_enabled = False    # Rig CAT uplink frequency control enabled flag
rig_cat_uplink_desired = 0.0      # Rig CAT uplink desired frequency
rig_cat_uplink_corrected = 0.0    # Rig CAT uplink corrected frequency
rig_cat_downlink_enabled = False  # Rig CAT downlink frequency control enabled flag
rig_cat_downlink_desired = 0.0    # Rig CAT downlink desired frequency
rig_cat_downlink_corrected = 0.0  # Rig CAT downlink corrected frequency
rig_cat_ok = False                # Rig CAT configured flag
rig_cat_orig_freq = ''            # Rig original frequency upon enable
rig_cat_orig_mode = ''            # Rig original mode upon enable

cat_control_thread_fn = None      # CAT control thread function
cat_control_thread_active = False # CAT control thread active indicator
cat_control_thread_run = False    # CAT control thread start/stop control flag

tracker_thread_fn = None      # Satellite tracking thread function
tracker_thread_active = False # Satellite tracking thread active indicator
tracker_thread_run = False    # Satellite tracking thread start/stop control flag


##############################################################################
# Functions.
##############################################################################

# ------------------------------------------------------------------------
def init():
    """
    Initialize global settings.
    """
    global config

    # Read the configuration file.
    config = ConfigFile()
    config.read()

# ------------------------------------------------------------------------
def init_tk_vars():
    """
    Initialize global Tk variables after root window initialized.
    """
    global root
    
    # Nothing to do.
    pass
    
# ------------------------------------------------------------------------
def close():
    """
    Gracefully persist all settings and shutdown all threads.
    """
    global config
    global cat_control_thread_active
    global tracker_thread_active

    stop_cat_control_thread()
    stop_tracker_thread()
    config.write()
    while tracker_thread_active or cat_control_thread_active:
        time.sleep(0.1)

# ------------------------------------------------------------------------
