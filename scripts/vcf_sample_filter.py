#!/usr/bin/env python
import sys
import warnings

from vcf import Reader, Writer
#from parser import Reader, Writer

class SampleFilter(object):
    def __init__(self, infile, outfile=None, filters=None, invert=False):
        self.parser = Reader(filename=infile)
        self.samples = self.parser.samples
        self.smp_idx = dict([(v,k) for k,v in enumerate(self.samples)])
        self.outfile = outfile
        self.invert = invert
        self.filters = filters
        if filters is not None:
            self.set_filters()
            if outfile is not None:
                self.write()
        else:
            print "Samples:"
            for idx, val in enumerate(self.list_samples()):
                print "{0}: {1}".format(idx, val)

    def list_samples(self):
        return self.samples

    def set_filters(self, filters=None, invert=False):
        if filters is not None:
            self.filters = filters
        if invert:
            self.invert = invert
        filt_l = self.filters.split(",")
        filt_s = set(filt_l)
        if len(filt_s) < len(filt_l):
            warnings.warn("Non-unique filters, ignoring", RuntimeWarning)
        def filt2idx(item):
            """Convert filter to valid sample index"""
            try:
                item = int(item)
            except ValueError:
                # not an idx, check if it's a value
                return self.smp_idx.get(item)
            else:
                # is int, check if it's an idx
                if item < len(self.samples):
                    return item
        filters = set(filter(lambda x: x is not None, map(filt2idx, filt_s)))
        if len(filters) < len(filt_s):
            # TODO print the filters that were ignored
            warnings.warn("Invalid filters, ignoring", RuntimeWarning)

        if self.invert:
            filters = set(xrange(len(self.samples))).difference(filters)

        # sample_filter is a property that updates parser.samples
        self.parser.sample_filter = filters
        print "Keeping these samples:", self.parser.samples

    def write(self, outfile=None):
        if outfile is not None:
            self.outfile = outfile
        writer = Writer(open(self.outfile, "w"), self.parser)
        for row in self.parser:
            writer.write_record(row)

if __name__ == "__main__":
    # TODO implement argparse
    if len(sys.argv) < 4:
        print "Usage: script.py infile outfile [filt1,filt2]"
        if len(sys.argv) < 3:
            raise SystemExit

    filt = SampleFilter(*sys.argv[1:])
    #print "now invert:"
    #filt2 = SampleFilter(*sys.argv[1:], invert=True)
    #print "now sequential:"
    #filt3 = SampleFilter(sys.argv[1])
    #if len(sys.argv) > 3:
        #filt3.set_filters(sys.argv[3])
        #filt3.write(sys.argv[2])
