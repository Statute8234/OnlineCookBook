from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast
# ----------------------
from pymongo import MongoClient
import bcrypt, secrets
import string
import re
# pymongo database
client = MongoClient("mongodb://localhost:27017")
db = client.neuraldb
users = db.users
# bcrypt
def generate_random_username(length=8):
    return ''.join(secrets.choice(string.ascii_letters) for _ in range(length))

def generate_random_password(length=12):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(password_characters) for _ in range(length))

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(password, hashed_password):
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    except:
        return password == hashed_password
# db options
def AddUser(Username, Email, Full_Name):
    password = generate_random_username()
    user_data = {'Username': Username, 'Email': Email, 'Full Name': Full_Name, 'Password': password}
    users.insert_one(user_data)

def FindUser(input_value, search_key='Username'):
    query = {search_key: input_value}
    person = users.find_one(query)
    return person

def EditPerson(Username, full_name, edit_info_name, new_info):
    query = {'Username': Username, "Full Name": full_name}
    update_result = users.update_many(query, {'$set': {edit_info_name: new_info}})

def PrintDataBase():
    cursor = users.find()
    for user in cursor:
        print(user)
# show notification
def show_notification(check):
    if not(check):
        toast('Sorry, Somthing has gone wrong')
    else:
        toast('Success')
# app
class LogInScreen(Screen):
    def check_input(self):
        self.LoginUsername_input = self.ids.username_input
        self.LoginPassword_input = self.ids.text_field
        self.LoginUsername = self.LoginUsername_input.text
        self.LoginPassword = self.LoginPassword_input.text

        if (len(self.LoginUsername) >= self.LoginUsername_input.max_text_length) or (len(self.LoginPassword) >= self.LoginPassword_input.max_text_length):
            show_notification(False)
        elif (bool(re.search(r"\s", self.LoginUsername))):
            show_notification(False)
        elif not self.LoginUsername or not self.LoginPassword:
            show_notification(False)
        elif any(char in string.punctuation for char in self.LoginUsername):
            show_notification(False)
        else:
            user = FindUser(input_value=self.LoginUsername, search_key='Username')
            if user and verify_password(self.LoginPassword, user.get('Password', '')):
                show_notification(True)
            else:
                show_notification(False)
        self.clear()
                
    def clear(self):
        self.LoginUsername_input.text = ""
        self.LoginPassword_input.text = ""

class ForgotPasswordScreen(Screen):
    def check_input(self):
        self.email_input = self.ids.email_input
        self.password_input = self.ids.text_field
        self.confirm_input = self.ids.confirm_field
        self.ForgotEmail = self.email_input.text
        self.ForgotPassword = self.password_input.text
        self.ForgotConfirm = self.confirm_input.text
        
        if (len(self.ForgotEmail) >= self.email_input.max_text_length) or (len(self.ForgotPassword) >= self.password_input.max_text_length) or (len(self.ForgotConfirm) >= self.confirm_input.max_text_length):
            show_notification(False)
        elif self.ForgotPassword != self.ForgotConfirm:
            show_notification(False)
        else:
            user = FindUser(input_value=self.ForgotEmail, search_key='Email')
            if not user:
                show_notification(False)
            else:
                new_hashed_password = hash_password(self.ForgotPassword)
                EditPerson(user['Username'], user['Full Name'], "Password", new_hashed_password)
                show_notification(True)
        self.clear()
        
    def clear(self):
        self.email_input.text = ""
        self.password_input.text = ""
        self.confirm_input.text = ""

class SignUpScreen(Screen):
    def check_input(self):
        self.firstName_input = self.ids.firstName_input
        self.lastName_input = self.ids.lastName_input
        self.email_input = self.ids.email_input
        self.password_input = self.ids.text_field

        self.SignupFirstName = self.firstName_input.text
        self.SignupLastName = self.lastName_input.text
        self.SignupEmail = self.email_input.text
        self.SignupPassword = self.password_input.text

        if (len(self.SignupFirstName) >= self.firstName_input.max_text_length) or (len(self.SignupLastName) >= self.lastName_input.max_text_length) or (len(self.SignupEmail) >= self.email_input.max_text_length) or (len(self.SignupPassword) >= self.password_input.max_text_length):
            show_notification(False)
        elif FindUser(input_value=self.SignupEmail,search_key='Email'):
            show_notification(False)
        else:
            user = FindUser(input_value=self.SignupEmail, search_key='Email')
            if not user:
                full_name = self.SignupFirstName + "_" + self.SignupLastName
                AddUser(generate_random_username(),self.SignupEmail,full_name)
                show_notification(True)
        self.clear()
        
    def clear(self):
        self.firstName_input.text = ""
        self.lastName_input.text = ""
        self.email_input.text = ""
        self.password_input.text = ""
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
