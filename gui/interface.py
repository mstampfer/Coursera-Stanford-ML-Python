import os
import pypandoc
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput
from kivy.uix.label import Label
from kivy.uix.rst import RstDocument
from kivy.uix.textinput import TextInput



class generate_elements():
	def __init__(self, **args):
		pass
		
	def files(self,excercise):
		path = '../'+excercise
		filelist = [c[:-3] for c in os.listdir(path) if c.endswith('.py')]
		# files=[]
		# for ex in filelist:
		# 	files.append(open(path+'/'+ex))
		return filelist
	def manual(self, excercise):
		path = 'res/'+excercise+'/manual.md'
		return pypandoc.convert(path,'rst')

	def readFile(self,excercise,filename):
		path = '../'+excercise+'/'+filename
		f=open(path,'rw')
		return f
		
class MainScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation='vertical'
        self.current_ex = 'ex1'
        self.current_file = 'warmUpExercise.py'
        self.element=generate_elements()
        self.add_widget(self.titlebar())
        self.add_widget(self.maineditor())
        self.add_widget(self.filebar())

    def titlebar(self):
    	layout=BoxLayout(spacing=10)
    	layout.orientation='horizontal'
    	submit = Button(text='Submit',size=(.5,.1))
    	submit.bind(on_press=self.submission)
    	layout.add_widget(Label(text='Excercise1',size=(100,100)))
    	layout.add_widget(Label(text='Title'))
    	layout.add_widget(submit)

    	return layout


    def submission(self,instance):
    	print('The button <%s> is being pressed' % instance.text)

    
    def maineditor(self):
    	layout=BoxLayout()
    	layout.orientation='horizontal'
    	man = self.element.manual(self.current_ex)
    	code = self.element.readFile(self.current_ex,self.current_file)
    	layout.add_widget(CodeInput(text=code.read()))
    	layout.add_widget(RstDocument(text=man))
    	return layout

    def filebar(self,excercise='ex1'):
    	layout=BoxLayout()
    	layout.orientation='horizontal'
    	files = self.element.files(excercise)
    	for f in files:
    		layout.add_widget(Label(text=f))
    	
    	return layout


class MainApp(App):

    def build(self):
    	return MainScreen()
    def on_pause(self):
    	return True


if __name__ == '__main__':
    MainApp().run()