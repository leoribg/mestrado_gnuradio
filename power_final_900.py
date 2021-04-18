#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.8.2.0

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import filerepeater
import limesdr
import time


class power_final(gr.top_block):

    def __init__(self, bw=50000, center_freq=902200000, filename='/home/leo/mestrado/teste.txt', samp_rate=1000000):
        gr.top_block.__init__(self, "Not titled yet")

        ##################################################
        # Parameters
        ##################################################
        self.bw = bw
        self.center_freq = center_freq
        self.filename = filename
        self.samp_rate = samp_rate

        ##################################################
        # Blocks
        ##################################################
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                bw/2,
                bw/10,
                firdes.WIN_HAMMING,
                6.76))
        self.limesdr_source_0 = limesdr.source('', 0, '')


        self.limesdr_source_0.set_sample_rate(samp_rate)


        self.limesdr_source_0.set_center_freq(center_freq, 0)

        self.limesdr_source_0.set_bandwidth(100e3, 0)


        self.limesdr_source_0.set_digital_filter(samp_rate, 0)


        self.limesdr_source_0.set_gain(20, 0)


        self.limesdr_source_0.set_antenna(255, 0)


        self.limesdr_source_0.calibrate(2.5e6, 0)
        self.high_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.high_pass(
                1,
                samp_rate,
                bw/2,
                bw/10,
                firdes.WIN_HAMMING,
                6.76))
        self.filerepeater_VectorToTxtFile_0 = filerepeater.VectorToTxtFile(filename, 1, 1, samp_rate, '', True, 0.01, 2, False)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(50000, 20e-6, 4000, 1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.filerepeater_VectorToTxtFile_0, 0))
        self.connect((self.high_pass_filter_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.limesdr_source_0, 0), (self.high_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0, 0))


    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.high_pass_filter_0.set_taps(firdes.high_pass(1, self.samp_rate, self.bw/2, self.bw/10, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.bw/2, self.bw/10, firdes.WIN_HAMMING, 6.76))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.limesdr_source_0.set_center_freq(self.center_freq, 0)

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.high_pass_filter_0.set_taps(firdes.high_pass(1, self.samp_rate, self.bw/2, self.bw/10, firdes.WIN_HAMMING, 6.76))
        self.limesdr_source_0.set_digital_filter(self.samp_rate, 0)
        self.limesdr_source_0.set_digital_filter(self.samp_rate, 1)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.bw/2, self.bw/10, firdes.WIN_HAMMING, 6.76))




def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--bw", dest="bw", type=eng_float, default="100.0k",
        help="Set bw [default=%(default)r]")
    parser.add_argument(
        "--center-freq", dest="center_freq", type=eng_float, default="902.2M",
        help="Set center_freq [default=%(default)r]")
    parser.add_argument(
        "--filename", dest="filename", type=str, default='/home/leo/mestrado/teste.txt',
        help="Set /home/leo/mestrado/teste.txt [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default="1.0M",
        help="Set samp_rate [default=%(default)r]")
    return parser


def main(top_block_cls=power_final, options=None):
    if options is None:
        options = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")
    tb = top_block_cls(bw=options.bw, center_freq=options.center_freq, filename=options.filename, samp_rate=options.samp_rate)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        print("Closing in 5 seconds ...")
        time.sleep(5)
        sys.exit(0) 
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
