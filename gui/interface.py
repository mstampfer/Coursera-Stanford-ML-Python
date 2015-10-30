from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class LoginScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation='vertical'
        self.add_widget(self.titlebar())
        self.add_widget(self.maineditor())
        self.add_widget(self.filebar())

    def titlebar(self):
    	layout=BoxLayout()
    	layout.orientation='horizontal'
    	#submit = Button(text='Submit')
    	#submit.bind(on_press=self.submission)
    	#layout.add_widget(submit)
    	layout.add_widget(Label(text='Excercise1'))
    	layout.add_widget(Label(text='Title'))
    	layout.add_widget(Label(text='Submit'))

    	return layout


    def submission(self,sub):
    	print('The button <%s> is being pressed' % instance.text)
    
    def maineditor(self):
    	layout=BoxLayout()
    	layout.orientation='horizontal'
    	layout.add_widget(Label(text='Code Editor'))
    	layout.add_widget(Label(text='Instructions'))
    	return layout

    def filebar(self):
    	layout=BoxLayout()
    	layout.orientation='horizontal'
    	layout.add_widget(Label(text='File1'))
    	layout.add_widget(Label(text='File2'))
    	layout.add_widget(Label(text='File3'))
    	return layout


class MainApp(App):

    def build(self):
        return LoginScreen()
    def on_pause(self):
    	return True


if __name__ == '__main__':
    MainApp().run()