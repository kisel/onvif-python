import onvif
from onvif import ONVIFCamera

# disable events as they might restart buggy cameras
class ONVIFCamera(onvif.ONVIFCamera):
    def create_events_service(self, transport=None):
        raise RuntimeError("Events disabled - they can crash buggy cameras")

def print_help(filename):
    print(open('docs/' + filename, 'r', encoding='utf8').read())

def tips():
    print_help('tips.txt')

def snip():
    print_help('snip.md')

def docs():
    print_help('docs.md')

tips()

