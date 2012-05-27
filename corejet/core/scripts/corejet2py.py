#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Provides 'corejet2py' entrypoint for creating python test skeletons out of
'corejet.xml'
"""

from __future__ import with_statement

import os
import sys
import argparse
import pkg_resources
import lxml.etree


def main():
    parser = argparse.ArgumentParser(
        description=(u"Generates python test skeletons from CoreJet test "
                     u"report. Selects all scenarios with status 'pending' "
                     u"or 'mismatch' by default."))
    parser.add_argument(
        '--story', nargs="?",
        help=u"select a specific story with the given id")
    parser.add_argument(
        '--all', action='store_const', const=True, default=False,
        help=u"select all scenarios")
    parser.add_argument(
        '--mismatch', action='store_const', const=True, default=False,
        help=u"select only 'mismatch' scenarios")
    parser.add_argument(
        '--pending', action='store_const', const=True, default=False,
        help=u"select only 'pending' scenarios")
    parser.add_argument(
        metavar='corejet.xml', dest='filename', nargs='?',
        default='parts/test/corejet/corejet.xml',
        help=(u"path to CoreJet test report "
              u"(defaults to parts/test/corejet/corejet.xml)"))

    args = parser.parse_args()
    if not os.path.isfile(args.filename):
        sys.exit("%s: %s: No such file or directory"
                 % (sys.argv[0], args.filename))

    # Load the test report
    report_tree = None
    with open(args.filename) as report_file:
        report_tree = lxml.etree.parse(report_file)

    # Filter the test report by the given arguments
    if args.story:
        for story in report_tree.xpath("//story[not(@id='%s')]" % args.story):
            story.getparent().remove(story)
    elif args.all:
        pass
    elif args.pending:
        for scenario in report_tree.xpath('//scenario'):
            if scenario.get('testStatus') != 'pending':
                scenario.getparent().remove(scenario)
    elif args.mismatch:
        for scenario in report_tree.xpath('//scenario'):
            if scenario.get('testStatus') != 'mismatch':
                scenario.getparent().remove(scenario)
    else:
        for scenario in report_tree.xpath('//scenario'):
            if scenario.get('testStatus') not in ['pending', 'mismatch']:
                scenario.getparent().remove(scenario)
    # Filter empty stories
    for story in report_tree.xpath('//story[not(child::scenario)]'):
        story.getparent().remove(story)
    # Filter empty epics
    for epic in report_tree.xpath('//epic[not(child::story)]'):
        epic.getparent().remove(epic)

    # Load the XSLT
    xslt_tree = None
    xslt_path = os.path.join('xslt', 'corejet-to-python.xsl')
    with pkg_resources.resource_stream('corejet.core', xslt_path) as stream:
        xslt_tree = lxml.etree.parse(stream)
    xslt = lxml.etree.XSLT(xslt_tree)

    # Output the transformed results
    print xslt(report_tree)

if __name__ == '__main__':
    main()
