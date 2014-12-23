import webbrowser

import gui_server


if __name__ == '__main__':
    gui_server.ServerThread(('localhost', 8001),
                            gui_server.SurgeoHandler).start()
    webbrowser.open_new('http://localhost:8001/index.html')

