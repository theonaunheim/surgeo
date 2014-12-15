import webbrowser

from gui_server import ServerThread, SurgeoHandler


if __name__ == '__main__':
    ServerThread(('localhost', 8001),
                 SurgeoHandler).start()
    webbrowser.open_new('http://localhost:8001/index.html')

