
import os
import urllib.request

def fetch():
    image_destination = os.path.join(os.path.expanduser('~'),
                                     '.surgeo',
                                     'logo.gif')
    logo_link = 'http://i.imgur.com/6OI0Yda.gif?1'
    response = urllib.request.urlretrieve(logo_link,
                                          image_destination)


