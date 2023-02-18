###############################################################################
# CatControlThread.py
# Author: Tom Kerr AB3GY
#
# Real-time CAT control thread for the pySatCat application.
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
import threading
import time

# Local environment init.
import _env_init

# Local packages.
import globals
from RigCat import *


##############################################################################
# Globals.
##############################################################################
last_preset = 0
last_rig_cat_enabled = False
last_up_freq = 0
last_dn_freq = 0


##############################################################################
# Functions.
##############################################################################

# ------------------------------------------------------------------------
def cat_control_thread():
    """
    Real-time satellite tracking thread.
    Re-computes satellite parameters at periodic intervals.
    """
    global last_preset
    global last_rig_cat_enabled
    global last_up_freq
    global last_dn_freq
    
    globals.cat_control_thread_active = True
    print('CAT control thread starting.')

    # Give the Tk main loop time to start.
    time.sleep(1.0)
    
    while globals.cat_control_thread_run:
        # See if the rig CAT enabled state changed.
        if (last_rig_cat_enabled != globals.rig_cat_enabled):
            #print('last: ' + str(last_rig_cat_enabled) + ' this: ' + str(globals.rig_cat_enabled), flush=True)
            last_preset = 0
            last_up_freq = 0
            last_dn_freq = 0
            #print('rig cat enabled: ' + str(globals.rig_cat_enabled), flush=True)
            if globals.rig_cat_enabled:
                update_rig_cat()
            else:
                close_rig_cat()
            last_rig_cat_enabled = globals.rig_cat_enabled

        if globals.rig_cat_enabled and globals.rig_cat_ok:
        
            # Get presets and convert to Hz.
            if (last_preset != globals.selected_preset):
                last_up_freq = 0
                last_dn_freq = 0
                last_preset = globals.selected_preset
            section = 'PRESET' + str(globals.selected_preset)
            up_tuning_step = to_int(to_float(globals.config.get(section, 'UPLINK_TUNING_STEP')) * 1000.0)
            up_tune_thresh = to_int(to_float(globals.config.get(section, 'UPLINK_TUNE_THRESHOLD')) * 1000.0)
            dn_tuning_step = to_int(to_float(globals.config.get(section, 'DOWNLINK_TUNING_STEP')) * 1000.0)
            dn_tune_thresh = to_int(to_float(globals.config.get(section, 'DOWNLINK_TUNE_THRESHOLD')) * 1000.0)
            #print(up_tuning_step, up_tune_thresh, dn_tuning_step, dn_tune_thresh)
        
            # Get the rig frequency just to see if we're connected.
            resp = globals.rig_cat.ascii_cmd('FREQ', [])
            if (len(resp) > 0) and (resp.isnumeric()):
                globals.widget_cat_control.set_comm_status(True)
            else:
                globals.widget_cat_control.set_comm_status(False)
            #print('resp: ' + str(resp))
            
            # Manage the uplink frequency.
            if globals.rig_cat_uplink_enabled:
                # Use the corrected uplink frequency.
                up_freq = to_int(to_float(globals.rig_cat_uplink_corrected) * 1000000.0)
                if (up_freq > 0) and (up_tuning_step > 0) and (up_tune_thresh > 0):
                    mod = up_freq % up_tuning_step
                    if (mod < up_tune_thresh):
                        up_freq -= mod # Next step down
                    else:
                        up_freq += (up_tuning_step - mod) # Next step up
            else:
                # Use the desired uplink frequency.
                up_freq = to_int(to_float(globals.rig_cat_uplink_desired) * 1000000.0)
            if (up_freq > 0) and (last_up_freq != up_freq):
                # Set the rig frequency.
                resp = globals.rig_cat.ascii_cmd('FREQB', [up_freq])
                #print(up_freq)
                if 'OK' in resp:
                    last_up_freq = up_freq
            
            # Manage the downlink frequency.
            if globals.rig_cat_downlink_enabled:
                # Use the corrected downlink frequency.
                dn_freq = to_int(to_float(globals.rig_cat_downlink_corrected) * 1000000.0)
                if (dn_freq > 0) and (dn_tuning_step > 0) and (dn_tune_thresh > 0):
                    mod = dn_freq % dn_tuning_step
                    if (mod < dn_tune_thresh):
                        dn_freq -= mod
                    else:
                        dn_freq += (dn_tuning_step - mod)
            else:
                # Use the desired downlink frequency.
                dn_freq = to_int(to_float(globals.rig_cat_downlink_desired) * 1000000.0)
            if (dn_freq > 0) and (last_dn_freq != dn_freq):
                # Set the rig frequency.
                resp = globals.rig_cat.ascii_cmd('FREQA', [dn_freq])
                #print(dn_freq)
                if 'OK' in resp:
                    last_dn_freq = dn_freq
        else:
            globals.widget_cat_control.set_comm_status(False)
            
        time.sleep(2.0)
    
    print('CAT control thread exiting.')
    globals.cat_control_thread_active = False
    
# ------------------------------------------------------------------------
def start_cat_control_thread():
    """
    Start the real-time satellite tracking thread.
    """
    globals.cat_control_thread_run = True
    globals.cat_control_thread_fn = threading.Thread(target=cat_control_thread)
    globals.cat_control_thread_fn.start()

# ------------------------------------------------------------------------
def stop_cat_control_thread():
    """
    Stop the real-time satellite tracking thread.
    """
    globals.cat_control_thread_run = False

