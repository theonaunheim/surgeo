import decimal
import time
import urllib.request

# Relies heavily on surgeo, but this added for modularity
try:
    import surgeo
except ImportError:
    pass


def graphical_download(url, destination, title='data'):
    if not 'http://' in url:
        ''.join(['http://', url])
    # Subfunction
    def download_bar(block_count, block_size, total_size):
        percentage = int((decimal.Decimal(block_count) *
                          decimal.Decimal(block_size) /
                          decimal.Decimal(total_size) * 100))
        try:
            last_written_percentage
        except NameError:
            last_written_percentage = 0
        if percentage > last_written_percentage:
            try:
                surgeo.redirector.add('\rDownloading {}: {}%'.format(title,
                                      str(percentage)))
            # Relies heavily on surgeo, but this added for modularity
            except (NameError, AttributeError):
                print('\rDownloading {}: {}%'.format(title, str(percentage)))
    urllib.request.urlretrieve(url,
                               destination,
                               download_bar)
    time.sleep(0)

