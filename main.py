from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import pyopenvpn


class VPNApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        self.connect_button = Button(
            text='Connect VPN', on_press=self.connect_vpn)

        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.connect_button)

        return self.layout

    def connect_vpn(self, instance):

        # Récupérer les informations de l'utilisateur
        username = self.username_input.text
        password = self.password_input.text

        # Paramètres du serveur OpenVPN
        host = 'your_openvpn_server_host'
        port = 443  # Le port peut varier en fonction de la configuration

        # Création d'un client OpenVPN

        vpn = pyopenvpn.Openvpn(host, port)

        # Connexion au serveur OpenVPN
        try:
            vpn.connect(username, password)
            print("Connexion VPN établie !")
        except Exception as e:
            print("Erreur lors de la connexion au VPN :", e)


if __name__ == '__main__':
    VPNApp().run()
