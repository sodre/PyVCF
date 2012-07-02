#!/usr/bin/env python
import sys

import vcf
#from parser import Reader, Writer

class SampleFilter(object):
    def __init__(self, infile, outfile, arg=None):
        self.parser = Reader(filename=infile)
        self.samples = self.parser.samples
        self.outfile = outfile
        if arg is not None:
            self.set_filters(arg)
            self.write()
        else:
            print "Samples:"
            for idx, val in enumerate(self.list_samples()):
                print "{0}: {1}".format(idx, val)

    def list_samples(self):
        return self.samples

    def set_filters(self, filters, invert=False):
        filters = filters.split(",")
        if invert:
            #filters = 
            pass

        self.parser.set_sample_filter(filters)

    def write(self):
        #writer = Writer(stream=self.outfile, template=self.parser)
        test_row = self.parser.next()
        print test_row.samples

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage: script.py infile outfile [filt1,filt2]"
        if len(sys.argv) < 3:
            raise SystemExit

    filt = SampleFilter(*sys.argv[1:])
