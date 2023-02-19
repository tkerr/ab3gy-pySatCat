###############################################################################
# PresetConfiguration.py
# Author: Tom Kerr AB3GY
#
# PresetConfiguration class for use with the pySatCat application.
# Provides a data container and configuration file read/write methods for
# a satellite preset.
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

# Local packages.
import globals
from src.pySatCatUtils import *
from src.ConfigFile import ConfigFile


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# PresetConfiguration class.
##############################################################################
class PresetConfiguration(object):
    """
    PresetConfiguration class for use with the pySatCat application.
    Provides a data container and configuration file read/write methods for
    a satellite preset.
    """
    # ------------------------------------------------------------------------
    def __init__(self, id=0):
        """
        Class constructor.
        
        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        self.id = 0  # Preset configuration ID
        try:
            self.id = int(id)
        except Exception:
            print('Invalid satellite preset ID: ' + str(id))
        
        self.preset_name = ''               # Preset name
        self.sat_name = ''                  # Satellite name
        self.tle_file = ''                  # TLE file name
        self.uplink_freq_mhz = 0.0          # Uplink frequency in MHz
        self.uplink_use_corrected = 0       # Use Doppler corrected frequency if nonzero
        self.uplink_mode = ''               # Uplink transceiver mode
        self.uplink_tuning_step = 0.0       # Uplink tuning step in KHz
        self.uplink_tune_threshold = 0.0    # Uplink tuning threshold in KHz
        self.uplink_ctcss_tone = ''         # Uplink CTCSS tone frequency
        self.downlink_freq_mhz = 0.0        # Downlink frequency in MHz
        self.downlink_use_corrected = 0     # Use Doppler corrected frequency if nonzero
        self.downlink_mode = ''             # Downlink transceiver mode
        self.downlink_tuning_step = 0.0     # Downlink tuning step in KHz
        self.downlink_tune_threshold = 0.0  # Downlink tuning threshold in KHz
        
        self.init()

    # ------------------------------------------------------------------------
    def get_id(self):
        return self.id

    # ------------------------------------------------------------------------
    def set_id(self, val):
        self.id = to_int(val)

    # ------------------------------------------------------------------------
    def get_preset_name(self):
        return self.preset_name

    # ------------------------------------------------------------------------
    def set_preset_name(self, val):
        self.preset_name = str(val)

    # ------------------------------------------------------------------------
    def get_sat_name(self):
        return self.sat_name
    
    # ------------------------------------------------------------------------
    def set_sat_name(self, val):
        self.sat_name = str(val)

    # ------------------------------------------------------------------------
    def get_file_name(self):
        return self.tle_file

    # ------------------------------------------------------------------------
    def set_file_name(self, val):
        self.tle_file = str(val)

    # ------------------------------------------------------------------------
    def get_uplink_freq_mhz(self):
        return self.uplink_freq_mhz

    # ------------------------------------------------------------------------
    def set_uplink_freq_mhz(self, val):
        self.uplink_freq_mhz = to_float(val)
    
    # ------------------------------------------------------------------------
    def get_uplink_use_corrected(self):
        return self.uplink_use_corrected

    # ------------------------------------------------------------------------
    def set_uplink_use_corrected(self, val):
        self.uplink_use_corrected = to_int(val)
    
    # ------------------------------------------------------------------------
    def get_uplink_mode(self):
        return self.uplink_mode

    # ------------------------------------------------------------------------
    def set_uplink_mode(self, val):
        self.uplink_mode = str(val)
    
    # ------------------------------------------------------------------------
    def get_uplink_tuning_step(self):
        return self.uplink_tuning_step

    # ------------------------------------------------------------------------
    def set_uplink_tuning_step(self, val):
        self.uplink_tuning_step = to_float(val)
    
    # ------------------------------------------------------------------------
    def get_uplink_tune_threshold(self):
        return self.uplink_tune_threshold

    # ------------------------------------------------------------------------
    def set_uplink_tune_threshold(self, val):
        self.uplink_tune_threshold = to_float(val)

    # ------------------------------------------------------------------------
    def get_uplink_ctcss_tone(self):
        return self.uplink_ctcss_tone

    # ------------------------------------------------------------------------
    def set_uplink_ctcss_tone(self, val):
        self.uplink_ctcss_tone = str(val)

    # ------------------------------------------------------------------------
    def get_downlink_freq_mhz(self):
        return self.downlink_freq_mhz

    # ------------------------------------------------------------------------
    def set_downlink_freq_mhz(self, val):
        self.downlink_freq_mhz = to_float(val)
    
    # ------------------------------------------------------------------------
    def get_downlink_use_corrected(self):
        return self.downlink_use_corrected

    # ------------------------------------------------------------------------
    def set_downlink_use_corrected(self, val):
        self.downlink_use_corrected = to_int(val)
    
    # ------------------------------------------------------------------------
    def get_downlink_mode(self):
        return self.downlink_mode

    # ------------------------------------------------------------------------
    def set_downlink_mode(self, val):
        self.downlink_mode = str(val)
    
    # ------------------------------------------------------------------------
    def get_downlink_tuning_step(self):
        return self.downlink_tuning_step

    # ------------------------------------------------------------------------
    def set_downlink_tuning_step(self, val):
        self.downlink_tuning_step = to_float(val)
    
    # ------------------------------------------------------------------------
    def get_downlink_tune_threshold(self):
        return self.downlink_tune_threshold

    # ------------------------------------------------------------------------
    def set_downlink_tune_threshold(self, val):
        self.downlink_tune_threshold = to_float(val)
    
    # ------------------------------------------------------------------------
    def init(self):
        globals.config.read(create=False)
        if (self.id > 0):
            section = 'PRESET' + str(self.id)
            if not globals.config.has_section(section):
                globals.config.add_section(section)
            
            self.preset_name = str(globals.config.get(section, 'PRESET_NAME'))
            self.sat_name = str(globals.config.get(section, 'SAT_NAME'))
            self.tle_file = str(globals.config.get(section, 'TLE_FILE'))
            
            self.uplink_freq_mhz = to_float(globals.config.get(section, 'UPLINK_FREQ_MHZ'))
            self.uplink_use_corrected = to_int(globals.config.get(section, 'UPLINK_USE_CORRECTED'))
            self.uplink_mode = str(globals.config.get(section, 'UPLINK_MODE'))
            self.uplink_tuning_step = to_float(globals.config.get(section, 'UPLINK_TUNING_STEP'))
            self.uplink_tune_threshold = to_float(globals.config.get(section, 'UPLINK_TUNE_THRESHOLD'))
            self.uplink_ctcss_tone = str(globals.config.get(section, 'UPLINK_CTCSS_TONE'))
            
            self.downlink_freq_mhz = to_float(globals.config.get(section, 'DOWNLINK_FREQ_MHZ'))
            self.downlink_use_corrected = to_int(globals.config.get(section, 'DOWNLINK_USE_CORRECTED'))
            self.downlink_mode = str(globals.config.get(section, 'DOWNLINK_MODE'))
            self.downlink_tuning_step = to_float(globals.config.get(section, 'DOWNLINK_TUNING_STEP'))
            self.downlink_tune_threshold = to_float(globals.config.get(section, 'DOWNLINK_TUNE_THRESHOLD'))
    
    # ------------------------------------------------------------------------
    def write_config(self):
        if (self.id > 0):
            section = 'PRESET' + str(self.id)
            if not globals.config.has_section(section):
                globals.config.add_section(section)
                
            globals.config.set(section, 'PRESET_NAME', self.preset_name)
            globals.config.set(section, 'SAT_NAME', self.sat_name)
            globals.config.set(section, 'TLE_FILE', self.tle_file)
        
            globals.config.set(section, 'UPLINK_FREQ_MHZ', self.uplink_freq_mhz)
            globals.config.set(section, 'UPLINK_USE_CORRECTED', self.uplink_use_corrected)
            globals.config.set(section, 'UPLINK_MODE', self.uplink_mode)
            globals.config.set(section, 'UPLINK_TUNING_STEP', self.uplink_tuning_step)
            globals.config.set(section, 'UPLINK_TUNE_THRESHOLD', self.uplink_tune_threshold)
            globals.config.set(section, 'UPLINK_CTCSS_TONE', self.uplink_ctcss_tone)
        
            globals.config.set(section, 'DOWNLINK_FREQ_MHZ', self.downlink_freq_mhz)
            globals.config.set(section, 'DOWNLINK_USE_CORRECTED', self.downlink_use_corrected)
            globals.config.set(section, 'DOWNLINK_MODE', self.downlink_mode)
            globals.config.set(section, 'DOWNLINK_TUNING_STEP', self.downlink_tuning_step)
            globals.config.set(section, 'DOWNLINK_TUNE_THRESHOLD', self.downlink_tune_threshold)
        
            globals.config.write()


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('PresetConfiguration test program.')
    globals.init()
    p1 = PresetConfiguration(1)
    p1.set_preset_name('Preset One')
    p1.set_sat_name('My Sat One')
    p1.set_file_name('amateur.txt')
    p1.set_uplink_freq_mhz(145.990)
    p1.write_config()
   