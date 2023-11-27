import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox


class VPNApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Add the existing widgets
        self.vpn_button = Button(text='Connect VPN', on_press=self.connect_vpn)
        self.status_label = Label(text='VPN Status: Not Connected')
        self.layout.add_widget(self.vpn_button)
        self.layout.add_widget(self.status_label)

        # Add the new widgets
        self.login_page = BoxLayout(orientation='vertical')

        self.username_label = Label(text='Username:')
        self.username_input = TextInput(text='')

        self.password_label = Label(text='Password:')
        self.password_input = TextInput(text='', password=True)

        self.remember_me_checkbox = CheckBox()  # Remove the 'text' keyword argument

        self.login_page.add_widget(self.username_label)
        self.login_page.add_widget(self.username_input)
        self.login_page.add_widget(self.password_label)
        self.login_page.add_widget(self.password_input)
        self.login_page.add_widget(self.remember_me_checkbox)

        self.layout.add_widget(self.login_page)

        return self.layout

    def connect_vpn(self, instance):
        process = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE)
        output, err = process.communicate()
        print(output.decode('utf-8'))

        # Define the OpenVPN configuration file path
        config_file_path = '/path/to/config/file.ovpn'

        # Get the username and password
        username = self.username_input.text
        password = self.password_input.text

        # Check if the user wants to remember the credentials
        remember_me = self.remember_me_checkbox.active

        # Start the OpenVPN client in a background process
        if remember_me:
            # Save the credentials
            self.save_credentials(username, password)

            process = subprocess.Popen(['openvpn', config_file_path, '--username',
                                        username, '--password', password], stdout=PIPE, stderr=PIPE)
        else:
            process = subprocess.Popen(['openvpn', config_file_path],
                                       stdout=PIPE, stderr=PIPE)

        # Capture the output of the OpenVPN client
        stdout, stderr = process.communicate()

        # Check if the VPN connection was successful
        if 'Initialization Sequence Completed' in stdout:
            self.status_label.text = 'VPN Status: Connected'
        else:
            self.status_label.text = f'VPN Status: Error - {stderr}'

    def save_credentials(self, username, password):
        # Open the preferences file
        preferences = open('preferences.ini', 'w')

        # Write the username
        preferences.write('username = {}\n'.format(username))

        # Write the password
        preferences.write('password = {}\n'.format(password))

        # Close the preferences file
        preferences.close()


if __name__ == '__main__':
    VPNApp().run()
