import sublime
import sublime_plugin


# -------------------------------------------------------------------------------------------------------------------------------
# 'Constants'

# Path to store commands file
COMMANDS_FILE_PATH = None

PLUGINS_AND_SYNTAX_KEY = 'plugins_and_syntax-specific_settings'


# -------------------------------------------------------------------------------------------------------------------------------
# Helper functions


def _get_user_preferences():
    ''' Get Json Object of the user preferences file  '''

    preferences = sublime.load_settings('Preferences.sublime-settings')
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

    sublime.save_settings('Preferences.sublime-settings')

    # re-generate commands file
    _build_commands(preferences.get('visual_changer'))


def _build_command_dict(profile):
    return {
        "caption": "Visual Changer: Set %s Profile" % profile,
        "command": "visual_changer",
        "args": {"profile_chosen": "%s" % profile}
    }


def _update_plugins_and_syntax_settings(profile):
    ''' Replace plugin & syntax-specific user preferences with ones from the selected profile '''
    plugins_and_syntaxes = profile.get(PLUGINS_AND_SYNTAX_KEY, list())

    # no item to process.. bye!
    if(len(plugins_and_syntaxes) == 0):
        return

    for item in plugins_and_syntaxes:
        # load settings object for specific syntax or plugin
        item_settings_file = '%s.sublime-settings' % item

        # if settings file doesn't exist lets stop here.
        try:
            throwabit = sublime.load_resource('Packages/User/%s' % item_settings_file)
        except IOError:
            sublime.error_message('Setting file for: [ %s ] does not exist. Check your VisualChanger settings' % item)
            continue
        else:
            del(throwabit)

        # load user preferences in memory
        item_settings = sublime.load_settings(item_settings_file)

        for key in plugins_and_syntaxes[item]:
            val = plugins_and_syntaxes.get(item).get(key)
            # replace plugin settings with ones from the profile
            item_settings.set(key, val)

        # commit changes for item
        sublime.save_settings(item_settings_file)


# -------------------------------------------------------------------------------------------------------------------------------
# Program init


def plugin_loaded():
    ''' Init plugin '''

    global COMMANDS_FILE_PATH

    COMMANDS_FILE_PATH = sublime.packages_path() + "/User/VisualChanger.sublime-commands"

    # Get user preferences
    user_preferences = _get_user_preferences()

    # If there's no visual_changer key in user_preferences lets put one and add some template configs as well
    if(user_preferences.get('visual_changer') is None):
        # Set default template configs
        default_template = {

            "profile_name_1": {

                "visual_changer_test": "value 1",

                PLUGINS_AND_SYNTAX_KEY: {

                }
            },
            "profile_name_2": {

                "visual_changer_test": "value 2",

                PLUGINS_AND_SYNTAX_KEY: {

                }
            },
            "profile_name_3": {

                "visual_changer_test": "value 3",

                PLUGINS_AND_SYNTAX_KEY: {

                }
            }

        }
        user_preferences.set('visual_changer', default_template)

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
            # ignore plugins & syntax specific settings inside profiles
            if(val == PLUGINS_AND_SYNTAX_KEY):
                continue
            preferences.set(val, profiles[profile_chosen][val])

        # replaces preferences for specific plugin and syntax settings
        _update_plugins_and_syntax_settings(profiles[profile_chosen])

        # Update User preferences
        _update_user_preferences(preferences)


class VisualChangerListener(sublime_plugin.EventListener):
    def on_pre_save_async(self, view):
        '''  Rebuild commands file if preferences file has been updated '''

        # If user saves preferences.sublime-settings then lets update the commands
        if('Preferences.sublime-settings' in view.file_name()):
            _build_commands(_get_user_preferences().get('visual_changer'))
