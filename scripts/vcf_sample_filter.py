#!/usr/bin/env python
import sys
import warnings

from vcf import Reader, Writer
#from parser import Reader, Writer

class SampleFilter(object):
    def __init__(self, infile, outfile, filters=None, **kwarg):
        self.parser = Reader(filename=infile)
        self.samples = self.parser.samples
        self.smp_idx = dict([(v,k) for k,v in enumerate(self.samples)])
        self.outfile = outfile
        if filters is not None:
            self.set_filters(filters, **kwarg)
            self.write()
        else:
            print "Samples:"
            for idx, val in enumerate(self.list_samples()):
                print "{0}: {1}".format(idx, val)

    def list_samples(self):
        return self.samples

    def set_filters(self, filters, invert=False, **kwarg):
        filt_l = filters.split(",")
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

        if invert:
            filters = set(xrange(len(self.samples))).difference(filters)

        self.parser.set_sample_filter(filters)

    def write(self):
        #writer = Writer(stream=self.outfile, template=self.parser)
        test_row = self.parser.next()
        print test_row.samples

if __name__ == "__main__":
    # TODO implement argparse
    if len(sys.argv) < 4:
        print "Usage: script.py infile outfile [filt1,filt2]"
        if len(sys.argv) < 3:
            raise SystemExit

    filt = SampleFilter(*sys.argv[1:])
    print "now invert:"
    filt2 = SampleFilter(*sys.argv[1:], invert=True)
