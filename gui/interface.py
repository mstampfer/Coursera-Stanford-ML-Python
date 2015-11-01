import os
import pypandoc
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput
from kivy.uix.label import Label
from kivy.uix.rst import RstDocument
from kivy.uix.textinput import TextInput
#from kivy.metrics import dp
from kivy.uix.spinner import Spinner
from kivy.uix.splitter import Splitter


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
        self.draw_screen()

    def draw_screen(self):
    	self.add_widget(self.titlebar())
    	self.add_widget(self.maineditor())
    	self.add_widget(self.filebar())
    	
    def titlebar(self):
    	layout=BoxLayout(padding='2sp',size_hint=(1,None),height='65sp')
    	layout.orientation='horizontal'

    	submit = Button(text='Submit',size_hint=(0.4,1))
    	submit.bind(on_press=self.submission)
    	
    	run = Button(text='Run',size_hint=(0.4,1))
    	run.bind(on_press=self.run)

    	ex_dropdown = Spinner(text='Welcome',size_hint=(1,1))
    	ex_dropdown.values = os.listdir('./res/')
    	ex_dropdown.bind(text=self.updateExercise)

    	#title = Label(text=self.current_ex,size_hint=(1,1),font_size='35sp')

    	layout.add_widget(run)
    	layout.add_widget(ex_dropdown)
    	layout.add_widget(submit)

    	return layout


    def updateExercise(self,spinner,text):
    	self.current_ex=text
    	spinner.text=text
    	current_file = self.element.files(self.current_ex)[0]
    	if current_file.endswith('\n'):
    		current_file=current_file[:-1]
    	self.current_file= current_file
    	self.clear_widgets()
    	self.draw_screen()
    	print('The spinner', spinner, 'have text', text)
    	print 'Current file changed to: ', self.current_ex



    def run(self,instance):
    	print('The button <%s> is being pressed' % instance.text)
    def submission(self,instance):
    	print('The button <%s> is being pressed' % instance.text)

    
    def maineditor(self):
    	layout=BoxLayout()
    	#reactive layout not working

    	if self.width < self.height:
    		layout.orientation='vertical'   
    	else:
    		layout.orientation='horizontal'
    	#self.bind(self.current_ex=self.update_currentFile) 	
    	man = self.element.manual(self.current_ex)
    	codeFile = self.element.readFile(self.current_ex,self.current_file)
    	code = CodeInput(text=codeFile.read())
    	splitter = Splitter()
    	if layout.orientation == 'vertical':
    		splitter.sizable_from='bottom'
    	else:
    		splitter.sizable_from='right'
    	splitter.add_widget(code)
    	layout.add_widget(splitter)

    	layout.add_widget(RstDocument(text=man))
    	return layout

    
    	
    
    def filebar(self):
    	layout=BoxLayout(padding='2sp',size_hint=(1,None),height='100sp')
    	layout.orientation='horizontal'
    	files = self.element.files(self.current_ex)
    	for f in files:
    		button = Button(text=f)
    		button.bind(on_press=self.update_currentFile)
    		layout.add_widget(button)
    	
    	return layout

    #Use bind to see how it works
    def update_currentFile(self,instance):
    	if instance.text.endswith('\n'):
    		instance.text=instance.text[:-1]
    	self.current_file = instance.text    	
    	self.clear_widgets()
    	self.draw_screen()
    	print 'Current file changed to: ', self.current_file


class MainApp(App):

    def build(self):
    	return MainScreen()
    def on_pause(self):
    	return True


if __name__ == '__main__':
    MainApp().run()