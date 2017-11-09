import sublime
import sublime_plugin


# -------------------------------------------------------------------------------------------------------------------------------
# 'Constants'

PREFERENCES_PATH = None
# Path to store commands file
COMMANDS_FILE_PATH = None


# -------------------------------------------------------------------------------------------------------------------------------
# Helper functions


def _get_user_preferences():
    ''' Get Json Object of the user preferences file  '''

    # open preferences file and decode json
    with open(PREFERENCES_PATH) as f:
        preferences = sublime.decode_value(f.read())
        # pprint(preferences)

    return preferences


def _build_commands(profiles):
    ''' Build commands file based on the profiles set by user '''

    if profiles is None:
        return

    # generate commands file
    generated_commands = [_build_command_dict(profile) for profile in profiles]

    # save commands file
    with open(COMMANDS_FILE_PATH, 'w') as f:
        f.write(sublime.encode_value(generated_commands, pretty=True))


def _update_user_preferences(preferences):
    ''' Replace the original user preferences file with newest one '''

    # Open preferences file and save the updated preferences
    with open(PREFERENCES_PATH, 'w') as f:
        # write encoded pretty json preferences
        f.write(sublime.encode_value(preferences, pretty=True))
        # re-generate commands file
        _build_commands(preferences.get('visual_changer'))


def _build_command_dict(profile):
    return {
        "caption": "Visual Changer: Set %s Profile" % profile,
        "command": "visual_changer",
        "args": {"profile_chosen": "%s" % profile}
    }


def _update_plugins_settings(profile):
    ''' Replace plugin user preferences with ones from the selected profile '''
    plugins = profile.get('plugins', list())

    # no plugins to process.. bye!
    if(len(plugins) == 0):
        return

    for plugin in plugins:
        # load settings object for specific plugin
        plugin_settings_file = '%s.sublime-settings' % plugin
        # load plugin user preferences in memory
        plugin_settings = sublime.load_settings(plugin_settings_file)

        for key in plugins[plugin]:
            val = plugins.get(plugin).get(key)
            # replace plugin settings with ones from the profile
            plugin_settings.set(key, val)

        # commit changes for plugin
        sublime.save_settings(plugin_settings_file)


# -------------------------------------------------------------------------------------------------------------------------------
# Program init


def plugin_loaded():
    ''' Init plugin '''

    global PREFERENCES_PATH, COMMANDS_FILE_PATH

    PREFERENCES_PATH = sublime.packages_path() + "/User/Preferences.sublime-settings"
    COMMANDS_FILE_PATH = sublime.packages_path() + "/User/VisualChanger.sublime-commands"

    # Get user preferences
    user_preferences = _get_user_preferences()

    # If there's no visual_changer key in user_preferences lets put one and add some template configs as well
    if(user_preferences.get('visual_changer') is None):
        # Set default template configs
        user_preferences['visual_changer'] = {

            "profile_name_1": {

                "visual_changer_test": "value 1",

                "plugins": {

                }
            },
            "profile_name_2": {

                "visual_changer_test": "value 2",

                "plugins": {

                }
            },
            "profile_name_3": {

                "visual_changer_test": "value 3 ",

                "plugins": {

                }
            }

        }

        # Save modified user preferences
        _update_user_preferences(user_preferences)


class VisualChangerCommand(sublime_plugin.TextCommand):
    def run(self, edit, profile_chosen):
        ''' Given a profile name lets replace the base preferences with the ones in the profile '''

        preferences = _get_user_preferences()
        # print(preferences)

        profiles = preferences.get('visual_changer')

        # change current preferences for the ones in the chosen profile
        for val in profiles[profile_chosen]:
            # ignore plugins inside profiles
            if(val == 'plugins'):
                continue
            preferences[val] = profiles[profile_chosen][val]

        # replaces preferences for specific plugin
        _update_plugins_settings(profiles[profile_chosen])

        # Update User preferences
        _update_user_preferences(preferences)


class VisualChangerListener(sublime_plugin.EventListener):
    def on_pre_save_async(self, view):
        '''  Rebuild commands file if preferences file has been updated '''

        # If user saves preferences.sublime-settings then lets update the commands
        if(view.file_name().__contains__('Preferences.sublime-settings')):
            _build_commands(_get_user_preferences().get('visual_changer'))
