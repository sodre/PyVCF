#!/usr/bin/env python
import argparse
import sys
import warnings

from vcf import Reader, Writer
#from parser import Reader, Writer

class SampleFilter(object):
    def __init__(self, infile, outfile=None, filters=None, invert=False):
        # Methods to add to Reader
        def get_filter(self):
            return self._samp_filter

        def set_filter(self, filt):
            self._samp_filter = filt
            if filt:
                self.samples = [val for idx,val in enumerate(self.samples)
                               if idx not in set(filt)]

        def filter_samples(fn):
            """Decorator function to filter sample parameter"""
            def filt(self, samples, *args):
                samples = [val for idx,val in enumerate(samples)
                           if idx not in set(self.sample_filter)]
                return fn(self, samples, *args)
            return filt

        # Add property to Reader for filter list
        Reader.sample_filter = property(get_filter, set_filter)
        # Modify Reader._parse_samples to filter samples
        Reader._parse_samples = filter_samples(Reader._parse_samples)
        self.parser = Reader(filename=infile)
        # Store initial samples and indices
        self.samples = self.parser.samples
        self.smp_idx = dict([(v,k) for k,v in enumerate(self.samples)])
        # Properties for filter/writer
        self.outfile = outfile
        self.invert = invert
        self.filters = filters
        if filters is not None:
            self.set_filters()
            if outfile is not None:
                self.write()
        else:
            print "Samples:"
            for idx, val in enumerate(self.samples):
                print "{0}: {1}".format(idx, val)

    def set_filters(self, filters=None, invert=False):
        """Convert filters from string to list of indices, set on Reader"""
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

        # `sample_filter` setter updates `samples`
        self.parser.sample_filter = filters
        print "Keeping these samples:", self.parser.samples

    def write(self, outfile=None):
        if outfile is not None:
            self.outfile = outfile
        writer = Writer(open(self.outfile, "w"), self.parser)
        print "Writing to '{0}'".format(self.outfile)
        for row in self.parser:
            writer.write_record(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str,
                       help="VCF file to filter")
    parser.add_argument("-f", "--filter", type=str,
                       help="Comma-separated list of sample indices or names to filter")
    parser.add_argument("--invert", action="store_true",
                       help="Keep rather than discard the filtered samples")
    parser.add_argument("-o", "--outfile", type=str,
                       help="File to write out filtered samples")
    # TODO implement quiet (silent if both outfile and filter are specified)
    parser.add_argument("-q", "--quiet", action="store_true",
                       help="Less output")

    args = parser.parse_args()

    SampleFilter(args.file, args.outfile, args.filter, args.invert)
