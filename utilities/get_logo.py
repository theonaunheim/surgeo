
import os
import urllib.request

def fetch():
    image_destination = os.path.join(os.path.expanduser('~'),
                                     '.surgeo',
                                     'logo.jpg')
    logo_link = ('https://docs.google.com/uc?export=download&'
                 'id=0B7gDDyKBmu83OWROOXBCYjkzNWc')
    response = urllib.request.urlretrieve(logo_link,
                                          image_destination)


