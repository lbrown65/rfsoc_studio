__author__ = "David Northcote"
__organisation__ = "The University of Strathclyde"

import os
import xrfclk
import xrfdc
import pynq
import pynq.lib
from .hierarchies import *


class Overlay(Overlay):
    
    def __init__(self, bitfile_name=None, init_rf_clks=True, **kwargs):
        
        if bitfile_name is None:
            this_dir = os.path.dirname(__file__)
            bitfile_name = os.path.join(this_dir, 'bitstream', 'rfsoc_studio.bit')
        
        super().__init__(bitfile_name, **kwargs)
        
        self.init_i2c()

        if init_rf_clks:
            self.init_rf_clks()


    def init_i2c(self):
        """Initialize the I2C control drivers on RFSoC2x2.
        This should happen after a bitstream is loaded since I2C reset
        is connected to PL pins. The I2C-related drivers are made loadable
        modules so they can be removed or inserted.
        """
        module_list = ['i2c_dev', 'i2c_mux_pca954x', 'i2c_mux']
        for module in module_list:
            cmd = "if lsmod | grep {0}; then rmmod {0}; fi".format(module)
            ret = os.system(cmd)
            if ret:
                raise RuntimeError(
                    'Removing kernel module {} failed.'.format(module))

        module_list.reverse()
        for module in module_list:
            cmd = "modprobe {}".format(module)
            ret = os.system(cmd)
            if ret:
                raise RuntimeError(
                    'Inserting kernel module {} failed.'.format(module))
                
                
    def init_rf_clks(self, lmk_freq=122.88, lmx_freq=409.6):
        """Initialise the LMX and LMK clocks for RF-DC operation.
        """
        xrfclk.set_ref_clks(lmk_freq=lmk_freq, lmx_freq=lmx_freq)