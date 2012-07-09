#!/usr/bin/env python

# Author: Lenna X. Peterson
# github.com/lennax
# arklenna at gmail dot com

import argparse

from vcf import SampleFilter


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="VCF file to filter")
    parser.add_argument("-f", metavar="filters",
                       help="Comma-separated list of sample indices or names \
                        to filter")
    parser.add_argument("--invert", action="store_true",
                       help="Keep rather than discard the filtered samples")
    parser.add_argument("-o", metavar="outfile",
                       help="File to write out filtered samples")
    # TODO implement quiet (silent if both outfile and filter are specified)
    #parser.add_argument("-q", "--quiet", action="store_true",
                       #help="Less output")

    args = parser.parse_args()

    SampleFilter(infile=args.file, outfile=args.o,
                 filters=args.f, invert=args.invert)
