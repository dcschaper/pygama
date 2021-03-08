from ..data_decoder.py import *
from pygama import lgdo

class FCConfigDecoder(DataDecoder):
    """
    Decode FlashCam config data

    Derives from DataDecoder in anticipation of possible future functionality;
    currently DataDecoder interface is not used.

    Typical usage:

    fc_config = FCConfigDecoder.decode_config(fcio)

    Then you just use the fcio_config, which is a lgdo Struct (i.e. a dict)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def decode_config(fcio):
        config_names = [
            'nsamples', # samples per channel
            'nadcs', # number of adc channels
            'ntriggers', # number of triggertraces
            'telid', # id of telescope
            'adcbits', # bit range of the adc channels
            'sumlength', # length of the fpga integrator
            'blprecision', # precision of the fpga baseline
            'mastercards', # number of attached mastercards
            'triggercards', # number of attached triggercards
            'adccards', # number of attached fadccards
            'gps', # gps mode (0: not used, 1: external pps and 10MHz)
        ]
        struct = lgdo.Struct()
        for name in config_names:
            value = np.int32(getattr(fcio, name)) # all config fields are int32
            struct.add_field(name, lgdo.Scalar(value))
        return struct

