import http.server
import mimetypes
import os
import threading
import webbrowser


class SurgeoHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            f = open(parent_dir + os.sep + self.path, 'rb')
            self.send_response(200)
            specified_type = mimetypes.guess_type(self.path)[0]
            self.send_header('Content-Type',
                             specified_type)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()   
        except IOError:
            self.send_error(404)

    def do_POST(self):
        # Object does not appear to have a bona fide dict.
        for item in self.headers.items():
            if item[0] == 'Content-Length':
                content_length = int(item[1])
                break
        post_data = self.rfile.read(content_length)
        string_list = post_data.decode().split('&')
        data_dict = {item.partition('=')[0]: item.partition('=')[2]
                     for item in string_list}
        return_data = self.process_post_data(data_dict)
        self.wfile.write(return_data)

    def process_post_data(self,
                          data_dictionary):
        pass


class ServerThread(threading.Thread):
    def __init__(self,
                 address_tuple,
                 handler):
        threading.Thread.__init__(self)
        self.server = http.server.HTTPServer(address_tuple,
                                             handler)
        print("ServerThread started. Serving.")
    def run(self):
        self.server.serve_forever()
        

class HTMLCreator(object):

    @staticmethod
    def generate_generic():
        pass

    @staticmethod
    def generate_setup():
        pass

    @staticmethod
    def generate_list_processing():
        pass

    @staticmethod
    def wrap_in_form(html_to_wrap_as_string):
        wrapped_html = ''.join(['<form name="submissionForm">',
                                html_to_wrap_as_string,
                                '</form>',
                                '<button id="submitButton">Enter</button>'])
        return wrapped_html

    @staticmethod
    def tab_create():
        pass

'''
<span>
<button id="genericButton">Generic</button>
<script>
$(document).ready(function(){
    $("#submitButton").click(function(){
        var formArray = $(":input").serializeArray();
        submit(formArray);
    });
});
</script>
<button id="setupButton">Setup</button>

<button id="listButton">List</button>
</span>
</fieldset>
        

      <form name="submissionForm">
            Surname:
            <input type="text" name="Surname">
            <br><br>
            Zip Code:
            <input type="text" name="ZIP">
            <br>
            <select name="model">
                <option value="surgeo">Geocode</option>
                <option value="geocode">Surgei</option>
                <option value="surname">Surname</option>
            </select> 
        </form>
        <button id="submitButton">Enter</button>
'''

