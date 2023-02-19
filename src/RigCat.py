###############################################################################
# RigCat.py
# Author: Tom Kerr AB3GY
#
# CAT control object for the pySatCat application.
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

# Local environment init.
import _env_init

# Local packages.
import globals
from src.pySatCatUtils import *
from src.ConfigFile import ConfigFile
from src.WidgetCatControl import WidgetCatControl

# All the PyRigCat classes.
from PyRigCat.PyRigCat import *
from PyRigCat.PyRigCat_ft817 import PyRigCat_ft817
from PyRigCat.PyRigCat_ft991 import PyRigCat_ft991
from PyRigCat.PyRigCat_ic7000 import PyRigCat_ic7000


##############################################################################
# Globals.
##############################################################################

# Dictionary of CTCSS tones for satellites that require them.
# Key = tone frequency, value = CAT control parameter
CTCSS_TONES = {
    'OFF':'0',
    '67.0':'670',   '69.3':'693',   '71.9':'719',   '74.4':'744',   '77.0':'770',
    '79.7':'797',   '82.5':'825',   '85.4':'854',   '88.5':'885',   '91.5':'915',
    '94.8':'948',   '97.4':'974',   '100.0':'1000', '103.5':'1035', '107.2':'1072',
    '110.9':'1109', '114.8':'1148', '118.8':'1188', '123.0':'1230', '127.3':'1273',
    '131.8':'1318', '136.5':'1365', '141.3':'1413', '146.2':'1462', '151.4':'1514',
    '156.7':'1567', '159.8':'1598', '162.2':'1622', '165.5':'1655', '167.9':'1679',
    '171.3':'1713', '177.3':'1773', '179.9':'1799', '183.5':'1835', '186.2':'1862',
    '189.9':'1899', '192.8':'1928', '196.6':'1966', '199.5':'1995', '203.5':'2035',
    '206.5':'2065', '210.7':'2107', '218.1':'2181', '225.7':'2257', '229.1':'2291',
    '233.6':'2336', '241.8':'2418', '250.3':'2503', '254.1':'2541'}

##############################################################################
# Functions.
##############################################################################

# ------------------------------------------------------------------------
def close_rig_cat():
    """
    Close the rig CAT object.
    """
    #print('close_rig_cat enter', flush=True)
    if globals.rig_cat_ok:
        globals.rig_cat_ok = False
        if globals.rig_cat is not None:
            on_disable_rig_cat()
            globals.rig_cat.close()
    #print('close_rig_cat exit', flush=True)

# ------------------------------------------------------------------------
def update_rig_cat():
    """
    Get CAT control parameters from the config file and update the rig CAT object.
    """
    #print('update_rig_cat enter', flush=True)
    section = 'CAT'
    rig = str(globals.config.get(section, 'RIG'))
    port = str(globals.config.get(section, 'PORT'))
    baud = str(globals.config.get(section, 'BAUD'))
    data = str(globals.config.get(section, 'DATA'))
    parity = str(globals.config.get(section, 'PARITY'))
    stop = str(globals.config.get(section, 'STOP'))

    globals.widget_cat_control.set_rig_name(rig)
    init_cat_control(rig, port, baud, data, parity, stop)
    
    if (globals.rig_cat_ok):
        on_enable_rig_cat()
        on_preset_change()
    #print('update_rig_cat exit', flush=True)

# ------------------------------------------------------------------------
def init_cat_control(rig, port, baud, data, parity, stop):
    """
    Initialize the rig CAT control object.
    """
    #print('init_cat_control enter', flush=True)
    close_rig_cat()
    if not globals.rig_cat_enabled: 
        return
        
    rig = rig.upper()
    #print(rig, port, baud, data, parity, stop)
    
    # Select the specified rig CAT object.
    if (rig == 'FT-817'):
        globals.rig_cat = PyRigCat_ft817()
    elif (rig == 'FT-991'):
        globals.rig_cat = PyRigCat_ft991()
    elif (rig == 'IC-7000'):
        globals.rig_cat = PyRigCat_ic7000()
    else:
        print ('Rig: ' + rig + ' not supported.')
        return
    
    # Convert parameters to types expected by the PyRigCat classes.
    baud_t = int(baud)
    data_t = Datasize.EIGHT
    parity_t = Parity.NONE
    stop_t = Stopbits.ONE
    
    if (data == '5'): data_t = Datasize.FIVE
    elif (data == '6'): data_t = Datasize.SIX
    elif (data == '7'): data_t = Datasize.SEVEN
    
    if (parity == 'EVEN'): parity_t = Parity.EVEN
    elif (parity == 'ODD'): parity_t = Parity.ODD
    
    if (stop == '1.5'): stop_t = Stopbits.ONE_POINT_FIVE
    elif (stop == '2'): stop_t = Stopbits.TWO
    
    # Configure the serial port.
    config_ok = globals.rig_cat.config_port(
        port=port, 
        baudrate=baud_t,
        datasize=data_t,
        parity=parity_t,
        stopbits=stop_t,
        read_timeout=0.5)
    
    if config_ok:
        globals.rig_cat.init_rig()
        globals.rig_cat_orig_freq = ''
        globals.rig_cat_orig_mode = ''
        freq = globals.rig_cat.ascii_cmd('FREQ', [])
        if freq.isnumeric():
            globals.rig_cat_orig_freq = freq
        mode = globals.rig_cat.ascii_cmd('MODE', [])
        if OperatingMode.is_valid(mode):
            globals.rig_cat_orig_mode = mode
        globals.rig_cat_ok = True
    else:
        print('Serial port configuration error.')
    #print('init_cat_control exit', flush=True)

# ------------------------------------------------------------------------
def on_enable_rig_cat():
    """
    Perform CAT configuration when rig becomes enabled.
    """
    #print('on_enable_rig_cat', flush=True)
    section = 'CAT'
    ena_split = str(globals.config.get(section, 'ON_ENABLE_SPLIT'))
    if (ena_split == '1'):
        globals.rig_cat.ascii_cmd('SPLIT', ['ON'])

# ------------------------------------------------------------------------
def on_preset_change():
    """
    Perform CAT configuration when the satellite preset changes.
    """
    #print('on_preset_change enter', flush=True)
    if globals.rig_cat_enabled:
        if (globals.selected_preset > 0):
            ena_mode = str(globals.config.get('CAT', 'ON_ENABLE_MODE'))
            section = 'PRESET' + str(globals.selected_preset)
            mode_d = globals.config.get(section, 'DOWNLINK_MODE')
            mode_u = globals.config.get(section, 'UPLINK_MODE')
            tone_u = globals.config.get(section, 'UPLINK_CTCSS_TONE')
            if (ena_mode == '1'):
                if (len(mode_d) > 0):
                    globals.rig_cat.ascii_cmd('MODEA', [mode_d])
                if (len(mode_u) > 0):
                    globals.rig_cat.ascii_cmd('MODEB', [mode_u])
                if (len(tone_u) > 0) and (tone_u != 'OFF'):
                    tone_arg = CTCSS_TONES[tone_u]
                    globals.rig_cat.ascii_cmd('TONE', ['ENC', tone_arg])
    #print('on_preset_change exit', flush=True)

# ------------------------------------------------------------------------
def on_disable_rig_cat():
    """
    Perform CAT configuration when rig becomes disabled.
    """
    #print('on_disable_rig_cat enter', flush=True)
    section = 'CAT'
    dis_split = str(globals.config.get(section, 'ON_DISABLE_SPLIT'))
    dis_mode  = str(globals.config.get(section, 'ON_DISABLE_MODE'))
    dis_ctcss = str(globals.config.get(section, 'ON_DISABLE_CTCSS'))
    
    if (dis_split == '1'):
        globals.rig_cat.ascii_cmd('SPLIT', ['OFF'])
    
    if (dis_mode == '1'):
        if (len(globals.rig_cat_orig_freq) > 0):
            globals.rig_cat.ascii_cmd('FREQ', [globals.rig_cat_orig_freq])
        if (len(globals.rig_cat_orig_mode) > 0):
            globals.rig_cat.ascii_cmd('MODE', [globals.rig_cat_orig_mode])
    
    if (dis_ctcss == '1'):
        globals.rig_cat.ascii_cmd('TONE', ['OFF'])
    #print('on_disable_rig_cat exit', flush=True)

