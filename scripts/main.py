"""
Parses settings.conf and provides top-level script
"""

from ConfigParser import SafeConfigParser

def main(argv):
    conf = parse_settings('settings-example.conf')

def parse_settings(settings):
    _params = SafeConfigParser(allow_no_value=True)
    _params.read(settings)
