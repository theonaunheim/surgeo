import urllib
import http.server
import mimetypes
import os
import threading

import surgeo


class SurgeoHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        path = parent_dir + self.path
        try:
            f = open(path, 'rb')
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
        post_data_as_html = self.rfile.read(content_length).decode()
        post_data_pre_dict = urllib.parse.parse_qs(post_data_as_html)
        post_data_string = post_data_pre_dict['formArray'][0]
        post_data_list = post_data_string.split('&')
        post_data_dict = {item.partition('=')[0]: item.partition('=')[2]
                          for item in post_data_list}
        return_data = self.process_post_data(post_data_dict)
        self.wfile.write(return_data.encode())

    def process_post_data(self,
                          data_dictionary):
        html_result = HTMLCreator.input_command(data_dictionary)
        return html_result


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

    @classmethod
    def input_command(cls,
                      input_dict):
        '''This takes an input dict and invokes function based on template.

        Dict should contain:
        {'command': 'changePage',
         'thisTemplate': 'landing',
         'arguments': 'interactive'}

        '''
        # thisTemplate is what dictates the function used.
        template_name = input_dict['thisTemplate']
        # Get subroutine from template to subroutine dict
        func_to_use = cls.supply_func_from_template(template_name)
        # Run appropriate function with input dict arguments
        func_result = func_to_use(input_dict)
        # Wrap with tabs
        result_with_tabs = cls.wrap_with_tabs(func_result)
        # Wrap subroutine_result in form
        final_result = cls.wrap_in_form(result_with_tabs)
        # Return subroutine result
        return final_result

    @classmethod
    def supply_func_from_template(cls, template_name):
        # Tie specifc templates to functions
        template_to_func_dict = {'interactive': cls.interactive_sub,
                                 'settings': cls.settings_sub,
                                 'landing': cls.landing_sub,
                                 'menu': cls.menu_sub}
        return template_to_func_dict[template_name]

    @classmethod
    def interactive_sub(cls,
                        input_dict):
        pass
        
    @classmethod
    def menu_sub(cls,
                 input_dict):
        pass

    @classmethod
    def landing_sub(cls,
                    input_dict):
        html = 'Data here'
        return html

    @classmethod
    def settings_sub(cls,
                        input_dict):
        pass

    @classmethod
    def wrap_in_form(cls,
                     html_to_wrap_as_string):
        wrapped_html = ''.join(['<div id="presentation_pane" align="center">',
                                '<form name="submissionForm">',
                                html_to_wrap_as_string,
                                '</form>',
                                '<button id="submit_button" onClick="submit()">Enter</button>',
                                '</div>'])
        return wrapped_html

    @classmethod
    def wrap_with_tabs(cls,
                       input_html):
        tab_html = '''<div id="tabs">
   
                          <nav style="display: inline-block;">
                              
                              <li>
                              <a href="javascript:interactive_func()">Interactive</a>
                              </li>
                              
                              <script>
                              function interactive_func() {
                                  $("#submissionForm").replaceWith('<input type="hidden" name="thisTemplate" value="menu">
                                                                    <input type="hidden" name="command" value="changePage">
                                                                    <input type="hidden" name="arguments" value="interactive">
                                  ');
                                  submit();   
                              }
                              </script>
   
                              <li>
                              <a href="javascript:settings_func()">Settings</a>
                              </li>
                              
                              <script>
                              function settings_func() {
                                  $("#submissionForm").replaceWith('<input type="hidden" name="thisTemplate" value="menu">
                                                                    <input type="hidden" name="command" value="changePage">
                                                                    <input type="hidden" name="arguments" value="settings">
                                  ');
                                  submit();   
                              }
                              </script>
   
                              <li>
                              <a href="javascript:csv_func()">CSV</a>
                              </li>

                              <script>
                              function csv_func() {
                                  $("#submissionForm").replaceWith('<input type="hidden" name="thisTemplate" value="menu">
                                                                    <input type="hidden" name="command" value="changePage">
                                                                    <input type="hidden" name="arguments" value="csv">
                                  '); 
                                  submit();  
                              }
                              </script>
   
                          </nav>
                      </div>

                   '''
        # input_html is none
        html_wrapped_with_tabs = ''.join([tab_html,
                                          input_html]) 
        return html_wrapped_with_tabs

