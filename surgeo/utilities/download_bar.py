import decimal
import urllib.request

# Relies heavily on surgeo, but this added for modularity
try:
    import surgeo
except ImportError:
    pass


def graphical_http_download(url, destination, title='data'):
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


def graphical_ftp_download(ftp_item,
                           ftp_size,
                           destination_path,
                           ftp_instance):
    '''Needs to be cwd'd into the correct directory.'''
    # TODO ... this is awful code wrapped around retrbinary. Write ground up.
    # First open file
    write_file = open(destination_path, 'wb+')

    def callback(block,
                 ftp_item,
                 ftp_size,
                 destination_path):
        global downloaded
        percentage = int(decimal.Decimal(downloaded) /
                         decimal.Decimal(ftp_size) * 100)
        try:
            last_written_percentage
        except NameError:
            last_written_percentage = 0
        if percentage > last_written_percentage:
            try:
                surgeo.redirector.add('\rDownloading {}: {}%'.format(ftp_item,
                                      str(percentage)))
            # Relies heavily on surgeo, but this added for modularity
            except (NameError, AttributeError):
                print('\rDownloading {}: {}%'.format(ftp_item,
                                                     str(percentage)))
        write_file.write(block)
    ftp_instance.retrbinary('RETR ' + ftp_item,
                            lambda block: callback(block,
                                                   ftp_item,
                                                   ftp_size,
                                                   destination_path))
    write_file.close()

