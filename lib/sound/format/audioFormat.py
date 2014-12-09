__author__ = 'ckolek'


class AudioFormat(object):
    def __init__(self, encoding, num_channels, sample_rate, bits_per_sample,
                 frame_rate, frame_size, big_endian, properties=None):
        self.encoding = encoding
        self.num_channels = num_channels
        self.sample_rate = sample_rate
        self.bits_per_sample = bits_per_sample
        self.frame_rate = frame_rate
        self.frame_size = frame_size
        self.big_endian = big_endian
        self.properties = properties if properties else dict()

    def get_encoding(self):
        return self.encoding

    def get_number_of_channels(self):
        return self.num_channels

    def get_sample_rate(self):
        return self.sample_rate

    def get_bits_per_sample(self):
        return self.bits_per_sample

    def get_bytes_per_sample(self):
        return self.bits_per_sample / 8

    def get_frame_rate(self):
        return self.frame_rate

    def get_frame_size(self):
        return self.frame_size

    def is_big_endian(self):
        return self.big_endian

    def get_properties(self):
        return self.properties

    def has_property(self, key):
        return key in self.properties

    def get_property(self, key):
        return self.properties[key]