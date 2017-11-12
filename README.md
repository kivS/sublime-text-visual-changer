# Sublime Text 3 - Visual Changer
**VisualChanger** is a simple tool that allows you to add profiles that affect settings of the editor and its plugins. 
You can then change between profiles using the command palette or key bindings.


## Usage

*  VisualChanger adds an example configuration in your settings file(Preferences > Settings):

```json
 "visual_changer":
     {
        "profile_name_1":
        {
            "plugins_and_syntax-specific_settings":
            {
            },
            "visual_changer_test": "value 1"
        },
        "profile_name_2":
        {
            "plugins_and_syntax-specific_settings":
            {
            },
            "visual_changer_test": "value 2"
        },
        "profile_name_3":
        {
            "plugins_and_syntax-specific_settings":
            {
            },
            "visual_changer_test": "value 3"
        }
     }


```
* Example of profile configuration
  - You can target the editor, plugins and syntax-specific settings.
  - They keys in `plugins_and_syntax-specific_settings` refer to the name of the setting file used, in this case `PlainTasks` is the name of the setting file for the PlainTasks plugin and `Python` is the name for the Python syntax-specific setting file.

```json
  "visual_changer":{
        "day":
        {
            "color_scheme": "Packages/ayu/ayu-light.tmTheme",
            "original_color_scheme": "Packages/ayu/ayu-light.tmTheme",
            "theme": "ayu-light.sublime-theme",

            "plugins_and_syntax-specific_settings":
            {
                "PlainTasks":
                {
                    "color_scheme": "Packages/PlainTasks/tasks-solarized-light.hidden-tmTheme"
                },

                "Python":{
                    "font_size": 10
                }
            },
        },
        "night":
        {
            "color_scheme": "Packages/ayu/ayu-mirage.tmTheme",
            "original_color_scheme": "Packages/ayu/ayu-mirage.tmTheme",
            "theme": "ayu-mirage.sublime-theme",

            "plugins_and_syntax-specific_settings":
            {
                "PlainTasks":
                {
                    "color_scheme": "Packages/PlainTasks/tasks-eighties-colored.hidden-tmTheme"
                },

                "Python":{
                    "font_size": 15
                }
            }
        }
    }

 ```
 
 * You can change between profiles using the command palette(<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>p</kbd>) or using key bindings
 
 ###### Setting key binding:
 ```json
 { "keys": ["ctrl+alt+d"], "command": "visual_changer", "args": {"profile_chosen": "day"} }
 ```
 

 
