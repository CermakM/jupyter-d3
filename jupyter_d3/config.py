# jupyter-d3
# Copyright 2019 Marek Cermak <macermak@redhat.com>

"""Default configuration for d3 module."""

from collections import namedtuple


_DEFAULT_CONFIG = {
    'warnings': False,
    'd3': 'https://d3js.org/d3.v5.min',
    'd3_hierarchy': 'https://d3js.org/d3-hierarchy.v1.min',
}

DefaultD3Config = namedtuple('DefaultConfig', _DEFAULT_CONFIG.keys())

defaults = DefaultD3Config(**_DEFAULT_CONFIG)
"""Default configuration for d3."""
