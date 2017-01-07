import sublime
import sublime_plugin
import json
from pprint import pprint


#-------------------------------------------------------------------------------------------------------------------------------


def get_preferences_path():
	return sublime.packages_path()+"/User/Preferences.sublime-settings"


def get_user_preferences():
	''' Get Json Object of the user preferences file  '''

	preferences_path = get_preferences_path()

	# open preferences file and decode json 
	with open(preferences_path) as f:
		preferences = sublime.decode_value(f.read())
		#pprint(preferences)
	
	return preferences

	

#-------------------------------------------------------------------------------------------------------------------------------


class VisualChangerCommand(sublime_plugin.TextCommand):
	def run(self, edit, profile_chosen):
		preferences = get_user_preferences();
		#print(preferences)
		
		profiles = get_user_preferences().get('visual_changer')

		# change current preferences for the ones in the chosen profile
		for val in profiles[profile_chosen]:
			# Set preferences values to selected PROFILES
			preferences[val] = profiles[profile_chosen][val]

		# Update User preferences
		self.view.run_command('update_user_preferences', {'preferences': preferences })


class initVisualChangerCommand(sublime_plugin.TextCommand):
	def run(self, edit): 
		''' Init configs for the plugin '''

		# Get user preferences 
		user_preferences = get_user_preferences()

		# print("\n"*100)
		#print(user_preferences)

		#If there's no visual_changer key in user_preferences let's put one and some template configs shall we?!!
		if(user_preferences.get('visual_changer', None) == None):
			#print("noh huh")
			# Set default template configs
			user_preferences['visual_changer'] = {
				"profile_name_1":{
					"key": "value"
				},
				"profile_name_2":{
					"key": "value"
				},
				"profile_name_3":{
					"key": "value"
				}

			}

			# Save user preferences
			self.view.run_command('update_user_preferences', {'preferences': user_preferences })

		else:
			self.view.run_command('build_commands', {'profiles': user_preferences.get('visual_changer')})


class BuildCommandsCommand(sublime_plugin.TextCommand):
	def run(self, edit, profiles):
		''' Build commands file based on the profiles set by user '''

		# Path to store commands file
		commands_path = sublime.packages_path()+"/User/VisualChanger.sublime-commands"

		# generate commands file
		generated_commands = [{"caption": "Visual Changer: Set {} Profile".format(profile), "command": "visual_changer", "args": {"profile_chosen": "{}".format(profile)}} for profile in profiles]
		
		# save commands file
		with open(commands_path, 'w') as f:
			f.write(sublime.encode_value(generated_commands, pretty=True))



class UpdateUserPreferencesCommand(sublime_plugin.TextCommand):
	def run(self, edit, preferences):
		''' Encode preferences arg JSON object and save it '''

		preferences_path = get_preferences_path()
		
		# Open preferences file and save the updated preferences
		with open(preferences_path, 'w') as f:
			# write encoded pretty json preferences
			f.write(sublime.encode_value(preferences, pretty=True))	
			# re-generate commands file
			self.view.run_command('build_commands', {'profiles': preferences.get('visual_changer')})
		


class VisualChangerListener(sublime_plugin.EventListener):
	def on_pre_save_async(self, view):
		'''  Check if Preferences file has been saved'''

		# If user saves preferences.sublime-settings then lets update the commands
		if(view.file_name() ==  get_preferences_path()):
			view.run_command('build_commands', {'profiles': get_user_preferences().get('visual_changer')})
