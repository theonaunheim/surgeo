import decimal
import sys
import urllib.request

import surgeo


class PercentageHTTP(object):
    '''This presents a percentage while downloading data.

       PercentageHTTP(url,
                      destination_path,
                      title).start()

    '''

    def __init__(self,
                 url,
                 destination_path,
                 title):
        self.url = url
        self.destination_path = destination_path
        self.title = title
        self.last_written_percentage = 0

    def start(self):
        if not 'http://' in self.url:
            self.url = ''.join(['http://', self.url])
        urllib.request.urlretrieve(self.url,
                                   self.destination_path,
                                   self.graphical_http_func)
        surgeo.adapter.write('\n')

    def graphical_http_func(self,
                            block_count,
                            block_size,
                            total_size):
        percentage = int((decimal.Decimal(block_count) *
                          decimal.Decimal(block_size) /
                          decimal.Decimal(total_size) * 100))
        if percentage > self.last_written_percentage:
            self.last_written_percentage = percentage
            # Kludgy fix to rewrite same line.
            sys.stdout.write('\rDownloading {}: {}%'.format(
                             self.title, self.last_written_percentage))


class PercentageFTP(object):
    '''This should be used when logged into the FTP directory:

       PercentageFTP(ftp_filename,
                     destination_path,
                     ftplib_FTP_instance).start()


    '''
    
    def __init__(self,
                 ftp_filename,
                 destination_path,
                 ftplib_FTP_instance):
        self.filename = ftp_filename
        self.destination_path = destination_path
        self.ftp_instance = ftplib_FTP_instance
        self.file_size = self.ftp_instance.size(self.filename)
        
    def start(self):
        '''Run loop. Majority of work done in iterator.'''
        try:      
            ftp_generator = self.graphical_ftp_gen(self.filename,
                                                   self.file_size,
                                                   self.destination_path,
                                                   self.ftp_instance)
            ftp_generator.send(None)
            self.ftp_instance.retrbinary('RETR ' + self.filename,
                                         lambda block:
                                         ftp_generator.send(block))
        except StopIteration:
            pass
                
    def graphical_ftp_gen(self,
                          ftp_item,
                          ftp_size,
                          destination_path,
                          ftp_instance):
        '''This iterator does the majority of the work.'''
        with open(destination_path, 'wb+') as f:
            downloaded_data = 0
            last_written_percentage = 0
            sys.stdout.write('\rDownloading {}: {}%'.format(ftp_item, str(0)))
            while downloaded_data < ftp_size:
                block = yield
                downloaded_data += len(block)
                percentage = int((float(downloaded_data) /
                                 float(ftp_size)
                                 * 100))
                if percentage > last_written_percentage:
                    try:
                        sys.stdout.write('\rDownloading {}: {}%'.format(
                                     ftp_item, str(percentage)))
                    except (NameError, AttributeError):
                        sys.stdout.write('\rDownloading {}: {}%'.format(
                                         ftp_item, str(percentage)))
                f.write(block)
            sys.stdout.write('\rDownloading {}: {}%\n'.format(
                             ftp_item, str(100)))
