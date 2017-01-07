import sublime
import sublime_plugin
import json
from pprint import pprint

#Init visual changer checks
init_visual_changer()

# Get visual_changer profiles from user preferences
PROFILES = get_user_preferences().get('visual_changer')



#-------------------------------------------------------------------------------------------------------------------------------

def init_visual_changer(): 
	''' Init configs for the plugin '''

	# Get user preferences 
	user_preferences = get_user_preferences()

	# print("\n"*100)
	# print(user_preferences)

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
		update_user_preferences(user_preferences)

	else:
		buid_commands(user_preferences.get('visual_changer'))

def get_preferences_path():
	return sublime.packages_path()+"/User/Preferences.sublime-settings"


def buid_commands(profiles):
	''' Build commands file based on the profiles set by user '''

	# Path to store commands file
	commands_path = sublime.packages_path()+"/User/VisualChanger.sublime-commands"

	# generate commands file
	generated_commands = [{"caption": "Visual Changer: Set {} Profile".format(profile), "command": "visual_changer", "args": {"profile_chosen": "{}".format(profile)}} for profile in profiles]
	
	# save commands file
	with open(commands_path, 'w') as f:
		f.write(sublime.encode_value(generated_commands, pretty=True))


def get_user_preferences():
	''' Get Json Object of the user preferences file  '''

	preferences_path = get_preferences_path()

	# open preferences file and decode json 
	with open(preferences_path) as f:
		preferences = sublime.decode_value(f.read())
		#pprint(preferences)
	
	return preferences

def update_user_preferences(preferences):
	''' Encode preferences arg JSON object and save it '''

	preferences_path = get_preferences_path()
	
	# Open preferences file and save the updated preferences
	with open(preferences_path, 'w') as f:
		# write encoded pretty json preferences
		f.write(sublime.encode_value(preferences, pretty=True))	
		# re-generate commands file
		buid_commands(preferences.get('visual_changer'))
	

#-------------------------------------------------------------------------------------------------------------------------------

class VisualChangerCommand(sublime_plugin.TextCommand):
	def run(self, edit, profile_chosen):

		preferences = get_user_preferences();
		#print(preferences)
			
		# change current preferences for the ones in the chosen profile
		for val in PROFILES[profile_chosen]:
			# Set preferences values to selected PROFILES
			preferences[val] = PROFILES[profile_chosen][val]

		# Update User preferences
		update_user_preferences(preferences)
		


