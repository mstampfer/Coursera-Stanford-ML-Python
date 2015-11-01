import os
import pypandoc
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput
from kivy.uix.label import Label
from kivy.uix.rst import RstDocument
from kivy.uix.textinput import TextInput
from kivy.metrics import dp


class generate_elements():
	def __init__(self, **args):
		pass
		
	def files(self,excercise):
		path = 'res/'+excercise+'/filelist.txt'
		#filelist = [c[:-3] for c in os.listdir(path) if c.endswith('.py')]
		filehandler = open(path)
		filelist=[]
		while True:
			try:
				filelist.append(filehandler.next())
			except Exception, e:
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
    	submit = Button(text='Submit',size_hint=(0.4,1))
    	run = Button(text='Run',size_hint=(0.4,1))
    	run.bind(on_press=self.run)
    	submit.bind(on_press=self.submission)
    	title = Label(text=self.current_ex,size_hint=(1,1),font_size='35sp')
    	layout.add_widget(run)
    	layout.add_widget(title)
    	layout.add_widget(submit)

    	return layout


    def run(self,instance):
    	print('The button <%s> is being pressed' % instance.text)
    def submission(self,instance):
    	print('The button <%s> is being pressed' % instance.text)

    
    def maineditor(self):
    	layout=BoxLayout()
    	layout.orientation='horizontal'    	
    	man = self.element.manual(self.current_ex)
    	codeFile = self.element.readFile(self.current_ex,self.current_file)
    	code = CodeInput(text=codeFile.read())
    	layout.add_widget(code)
    	layout.add_widget(RstDocument(text=man))
    	return layout

    
    	
    def update_man():
    	pass
    def filebar(self):
    	layout=BoxLayout()
    	layout.orientation='horizontal'
    	files = self.element.files(self.current_ex)
    	for f in files:
    		button = Button(text=f)
    		button.bind(on_press=self.update_code)
    		layout.add_widget(button)
    	
    	return layout

    #Use bind to see how it works
    def update_code(self,instance):
    	if instance.text.endswith('\n'):
    		instance.text=instance.text[:-1]
    	self.current_file = instance.text
    	self.add_widget(self.maineditor())
    	print 'Current file changed to: ', self.current_file


class MainApp(App):

    def build(self):
    	return MainScreen()
    def on_pause(self):
    	return True


if __name__ == '__main__':
    MainApp().run()