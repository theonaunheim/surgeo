import webbrowser

import surgeo.gui.gui_server


if __name__ == '__main__':
    surgeo.gui.gui_server.ServerThread(('localhost', 8001),
                                        surgeo.gui.gui_server.SurgeoHandler)\
                                            .start()
    webbrowser.open_new('http://localhost:8001/index.html')

