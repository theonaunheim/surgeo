
import os
import time
import urllib.request

def fetch():
    image_destination = os.path.join(os.path.expanduser('~'),
                                     '.surgeo',
                                     'logo.gif')
    logo_link = 'http://i.imgur.com/6OI0Yda.gif?1'
    response = urllib.request.urlretrieve(logo_link,
                                          image_destination,
                                          reporthook)

def reporthook(block_count, block_size, total_size):
    time.sleep(0)
    
    

