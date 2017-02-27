from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

# Declare all application screens.
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class GameScreen(Screen):
    pass

class RulesScreen(Screen):
    pass


class ReversiApp(App):
    def start_single_player(self):
        self.root.current = 'game'
    def start_two_players(self):
        self.root.current = 'game'

    def end_game(self):
        self.root.current = 'menu'

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(RulesScreen(name='rules'))
        return sm

if __name__ == '__main__':
    ReversiApp().run()