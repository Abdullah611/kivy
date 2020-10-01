from kivy.app import App
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.lang import Builder

from jnius import autoclass

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer


Window.size = (360, 600)


SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.oscservice',
    servicename=u'Pong'
)


KV = '''
BoxLayout:
    orientation: 'vertical'
    Label:
        id: mesaj
        pos: 120, 500
        font_size: '30sp'
        text: 'Mesaj bekleniyor..'
    Label:
        id: active
        pos: 120, 300
        font_size: '30sp'
        text: 'Etkin değil.'
    
    Button:
        size: 360, 75
        pos: 0, 80
        text: 'Sunucuya Bağlan'
        on_press: app.start_server()
    Button:
        size: 360, 75
        pos: 0, 0
        text: 'Kapat'
'''





class GUI(App):
    def build(self):
        self.service = None
        # self.start_service()

        self.server = server = OSCThreadServer()
        server.listen(
            address=b'localhost',
            port=3002,
            default=True,
        )

        server.bind(b'/activation', self.isActive)
        server.bind(b'/message', self.display_message)

        self.client = OSCClient(b'localhost', 3000)

        self.root = Builder.load_string(KV)
        return self.root


    def start_server(self):
        if platform == "android":
            service = autoclass(SERVICE_NAME)
            mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
            argument = ''
            service.start(mActivity, argument)
            self.service = service

        if platform in ('linux', 'linux2', 'macos', 'win'):
            from runpy import run_path
            from threading import Thread
            self.service = Thread(
                target=run_path,
                args=['server.py'],
                kwargs={'run_name': '__main__'},
                daemon=True
            )
            self.service.start()




    def isActive(self, act):
        if self.root:
            self.root.ids.active.text = act.decode('UTF-8')

    def display_message(self, message):
        if self.root:
            self.root.ids.mesaj.text = message.decode('UTF-8')






if __name__ == '__main__':
    GUI().run()