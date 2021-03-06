#!/usr/bin/env python

# Copyright 2014 Philipp Winter <phw@nymity.ch>
#
# This file is part of exitmap.
#
# exitmap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# exitmap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with exitmap.  If not, see <http://www.gnu.org/licenses/>.

"""
This module attempts to fetch a simple web page.  If this succeeds, we know
that the relay (probably) has enough file descriptors.
"""

import re
import urllib2

import log

logger = log.get_logger()

destinations = [("people.torproject.org", 443)]


def probe(exit_fpr, _):
    """
    Tries to fetch a simple web page and warns us if it doesn't work.
    """

    exit_url = "<https://atlas.torproject.org/#details/%s>" % exit_fpr

    expected = "This file is to check if your exit relay has enough file " \
               "descriptors to fetch it."

    logger.debug("Probing exit relay %s." % exit_url)

    data = None
    try:
        data = urllib2.urlopen("https://people.torproject.org/~phw/test_file",
                               timeout=10).read()
    except Exception as err:
        logger.warning("urllib2.urlopen for %s says: %s." % (exit_url, err))
        return

    if not data:
        logger.warning("Exit relay %s did not return data." % exit_url)
        return

    data = data.strip()

    if not re.match(expected, data):
        logger.warning("Got unexpected response from %s: %s." %
                       (exit_url, data))
    else:
        logger.debug("Exit relay %s worked fine." % exit_url)


def main():
    """
    Entry point when invoked over the command line.
    """

    probe("dummy", None)

    return 0

if __name__ == "__main__":
    exit(main())
