from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from firebase import firebase
from kivy.core.window import Window
import os
import subprocess

Window.size = (300, 550)

# Initialize Firebase
firebase = firebase.FirebaseApplication('https://loginsample-54673-default-rtdb.asia-southeast1.firebasedatabase.app/', None)

kv_string = """
<LoginScreen>:
    MDLabel:
        text: "Adaptofit"
        font_size: "48dp"
        halign: "center"
        color: [1, 0.337, 0.137, 1]
        pos_hint: { 'center_y':.8}
    MDTextField:
        id: username_input
        hint_text: "Username"
        icon_right: 'account'
        font_size: "20dp"
        size_hint_x: .85
        pos_hint: {'center_x':.5, 'center_y':.65}
    MDTextField:
        id: password_input
        hint_text: "Password"
        icon_right: 'eye'
        font_size: "20dp"
        size_hint_x: .85
        pos_hint: {'center_x':.5, 'center_y':.5}
        password: True
    BoxLayout:
        size_hint: .85, None
        height: "30dp"
        pos_hint: {'center_x':.5, 'center_y':.4}
        MDCheckbox:
            id: show_password_checkbox
            size_hint: None, None
            width: "30dp"
            height: "30dp"
            pos_hint: {'center_x':.5, 'center_y':.5}
            on_press:
                password_input.password = False if password_input.password else True
        MDLabel:
            text: "[ref=Show Password]Show Password[/ref]"
            markup: True
            pos_hint: {'center_x':.5, 'center_y':.5}
            orientation: 'vertical'
            valign: 'middle'
            halign: 'left'
            on_ref_press:
                show_password_checkbox.active = not show_password_checkbox.active
    BoxLayout:
        padding: dp(30)
        size_hint: None, None
        height: "30dp"
        width: "250dp"
        pos_hint: {'center_x':.5, 'center_y':.15}
        orientation: 'vertical'
        spacing: "15dp"
        MDFlatButton:
            text: "Login"
            size_hint_x: 1
            md_bg_color: "FF5623"
            on_press: app.login()
        MDFlatButton:
            text: "Sign up"
            size_hint_x: 1
            theme_text_color: "Custom"  
            text_color: 1, 0.337, 0.137, 1 
            line_color: 1, 0.337, 0.137, 1 
"""

class LoginScreen(Screen):
    pass

class TestApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"   
        self.theme_cls.primary_palette = "Blue" 
        Builder.load_string(kv_string)
        self.sm = ScreenManager()
        self.login_screen = LoginScreen(name='login')
        self.sm.add_widget(self.login_screen)
        return self.sm

    def login(self):
        username = self.sm.get_screen('login').ids.username_input.text
        password = self.sm.get_screen('login').ids.password_input.text
        if self.authenticate_user(username, password):
            print("Login successful")
            self.start_application()
        else:
            print("Login failed")

    def authenticate_user(self, username, password):
        # Query Firebase to check if the provided username exists
        result = firebase.get('/users', None)
        if result is not None:
            for key, value in result.items():
                if value.get('Email') == username and value.get('Password') == password:
                    return True
        print("Invalid username or password")
        return False

    def start_application(self):
        current_dir = os.path.dirname(__file__)
        dashboard_path = os.path.join(current_dir, "dashboard.py")
        subprocess.run(["python", dashboard_path])
        # Switch to a new screen and remove the login screen
        self.sm.switch_to(self.sm.get_screen('dashboard'))
        self.sm.remove_widget(self.login_screen)

if __name__ == "__main__":
    TestApp().run()
