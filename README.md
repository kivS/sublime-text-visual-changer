# Sublime Text 3 - Visual Changer
VisualChanger is a simple tool that allows you to add profiles that affect settings of the editor and its plugins. 
You can then change between profiles using the command palette or key bindings.


## Usage

*  VisualChanger adds an example configuration in your settings file(Preferences > Settings):

```json
 "visual_changer":
     {
        "profile_name_1":
        {
            "plugins":
            {
            },
            "visual_changer_test": "value 1"
        },
        "profile_name_2":
        {
            "plugins":
            {
            },
            "visual_changer_test": "value 2"
        },
        "profile_name_3":
        {
            "plugins":
            {
            },
            "visual_changer_test": "value 3"
        }
     }


```

* Example of profile configuration

```json
  "visual_changer":{
        "day":
        {
            "color_scheme": "Packages/ayu/ayu-light.tmTheme",
            "original_color_scheme": "Packages/ayu/ayu-light.tmTheme",
            "theme": "ayu-light.sublime-theme",

            "plugins":
            {
                "PlainTasks":
                {
                    "color_scheme": "Packages/PlainTasks/tasks-solarized-light.hidden-tmTheme"
                }
            },
        },
        "night":
        {
            "color_scheme": "Packages/ayu/ayu-mirage.tmTheme",
            "original_color_scheme": "Packages/ayu/ayu-mirage.tmTheme",
            "theme": "ayu-mirage.sublime-theme",

            "plugins":
            {
                "PlainTasks":
                {
                    "color_scheme": "Packages/PlainTasks/tasks-eighties-colored.hidden-tmTheme"
                }
            }
        }
    }

 ```
 
 * Profiles can then be changed using the command pallete(ctrl+shift+p) or using key bindings
 
 ###### Setting key binding:
 ```json
 { "keys": ["ctrl+alt+d"], "command": "visual_changer", "args": {"profile_chosen": "day"} }
 ```
 

 
