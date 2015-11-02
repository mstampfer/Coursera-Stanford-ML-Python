import os
import pypandoc
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput
from kivy.uix.label import Label
from kivy.uix.rst import RstDocument
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.splitter import Splitter
from kivy.uix.popup import Popup
from kivy.clock import Clock
from functools import partial
from kivy.animation import Animation


class generate_elements():
	def __init__(self, **args):
		pass
		
	
	def read_token(self,instance):
		path = '../'+instance.current_ex+'/token.txt'
		try:
			credentials = open(path)
			instance.email = credentials.readline()[:-1]
			instance.token = credentials.readline()[:-1]
			return True
		except Exception, e:
			return False

			
	
	def files(self,excercise):
		path = 'res/'+excercise+'/filelist.txt'
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

	def writeFile(self,excercise,filename):
		path = '../'+excercise+'/'+filename
		f=open(path,'w')
		return f
		
	def readFile(self,excercise,filename):
		path = '../'+excercise+'/'+filename
		f=open(path,'r')
		return f.read()
		
class MainScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation='vertical'
        self.current_ex = 'ex1'
        self.current_file = 'warmUpExercise.py'
        self.element=generate_elements()
        #popup = Popup(title='CourseraApp', content=Label(text='Hello World'),size_hint=(0.6, 0.35))
        #popup.open()
        #sleep(10)
        #popup.dismiss()
        
        self.draw_screen()


    def draw_screen(self):
    	self.add_widget(self.titlebar())
    	self.add_widget(self.maineditor())
    	self.add_widget(self.filebar())
    	
    def titlebar(self):
    	layout=BoxLayout(padding='2sp',size_hint=(1,None),height='65sp')
    	layout.orientation='horizontal'

    	#credentials = self.accept_credentials()
    	self.submit_popup = Popup(title='Enter credentials',content=self.accept_credentials(),size_hint=(0.6, 0.35))        
    	#credentials.children[1].bind(on_press=self.submit_popup.dismiss)
    	
    	submit = Button(text='Submit',size_hint=(0.4,1))    	
    	if self.element.read_token(self):
        	submit.bind(on_press=partial(self.submit_assignment))
        else:
           	submit.bind(on_press=self.submit_popup.open)
    	
    	run = Button(text='Run',size_hint=(0.4,1))
    	run.bind(on_press=self.run)

    	ex_dropdown = Spinner(text='Select Exercise',size_hint=(1,1))
    	ex_dropdown.values = os.listdir('./res/')
    	ex_dropdown.bind(text=self.updateExercise)

    	layout.add_widget(run)
    	layout.add_widget(ex_dropdown)
    	layout.add_widget(submit)

    	return layout


    def accept_credentials(self):
    	main_layout= BoxLayout(padding='2sp')
    	main_layout.orientation='vertical'
    	layout=GridLayout(padding='2sp',size_hint=(1,None))
    	layout.cols=2
    	layout.add_widget(Label(text='Email id:'))
    	email = TextInput(multiline=False)
    	layout.add_widget(email)
    	token = TextInput(multiline=False)
    	layout.add_widget(Label(text='Submission Token:'))
    	layout.add_widget(token)
    	main_layout.add_widget(layout)
    	submit = Button(text='Submit')
    	submit.bind(on_press=partial(self.submit_assignment,email,token))
    	main_layout.add_widget(submit)
    	return main_layout
   	
    def submit_assignment(self,*largs):
        if len(largs)>1:
    		email = largs[0].text
    		token = largs[1].text
    	else:
    		email=self.email
    		token=self.token    		

    	print 'Email',email
    	print 'Token', token
    	self.submit_popup.dismiss()
    	#TODO:submission call

    def updateExercise(self,spinner,text):
    	self.current_ex=text
    	current_file = self.element.files(self.current_ex)[0]
    	if current_file.endswith('\n'):
    		current_file=current_file[:-1]
    	self.current_file= current_file
    	self.clear_widgets()
    	self.draw_screen()
    	print 'Current Exercise changed to: ', self.current_ex



    def run(self,instance):
    	#TODO: Display output in popup
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
    	code = CodeInput(text=codeFile)
    	code.bind(focus =self.schedule_reload)
    	splitter = Splitter()
    	if layout.orientation == 'vertical':
    		splitter.sizable_from='bottom'
    	else:
    		splitter.sizable_from='right'
    	splitter.add_widget(code)
    	layout.add_widget(splitter)

    	layout.add_widget(RstDocument(text=man))
    	return layout

    def updateAssignment(self,assignment,*largs):
    	try:
    		if not self.element.readFile(self.current_ex,self.current_file)==assignment.text:
    			filehandler = self.element.writeFile(self.current_ex,self.current_file)
    			filehandler.write(assignment.text)
		    	#print 'INFO: Autosaved'
    	except Exception, e:
    		raise e
    		#self.show_error(e)


    def schedule_reload(self,instance,value):
        self.callback = partial(self.updateAssignment,instance)
        if value:
        	#Schedule Update
        	Clock.schedule_interval(self.callback,5)
        else:
        	#TODO:Unsceduling not working properly. Autosave feature cannot be turned off automatically
        	Clock.unschedule(self.callback)
        	self.updateAssignment(instance)
        	#Update now
            
    
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

    def show_error(self, e):
    	print 'Error',str(e)
        info_label = Label(text=str(e))
        #self.anim = Animation(top=190.0, opacity=1, d=2) +\
        #    Animation(top=190.0, d=3) +\
        #    Animation(top=0, opacity=0, d=2)
        anim = Animation(x=10,y=10)
        anim.start(info_label)



class CourseraApp(App):

    def build(self):
    	return MainScreen()
    def on_pause(self):
    	return True


if __name__ == '__main__':	
	CourseraApp().run()
