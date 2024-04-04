from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast
# ----------------------
class ForgotPasswordScreen(Screen):
    pass

class SignUpScreen(Screen):
    pass

class LogInScreen(Screen):
    pass

# windows
class WindowManager(ScreenManager):
    pass

# main
class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        self.WM = WindowManager()
        self.WM.add_widget(LogInScreen(name='LogInScreen'))
        return Builder.load_file('main.kv')
    
if __name__ == '__main__':
    Window.size = (360, 640)
    MainApp().run()