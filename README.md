# Sublime Text 3 - Visual Changer
[ Sublime Text 3 Plugin ] Allows you to create profiles to change sublime's visual parameters on command

## Installation

* \<Sublime Text Packages folder>  Should be changed to your sublime's Packages folder.

```bash
git clone https://github.com/kivS/Sublime_Text_Visual_Changer.git "<Sublime Text Packages folder>/Visual Changer"
```


## Usage

* The plugin creates a config object in the preferences file like:

```json
"visual_changer":
	{
		"profile_name_1":
		{
			"key": "value"
		},
		"profile_name_2":
		{
			"key": "value"
		},
		"profile_name_3":
		{
			"key": "value"
		}
	}

```

* Example of profile configuration

```json
	"visual_changer":
	{
		"day":
		{
			"color_scheme": "Packages/Colorcoder/ayu-light (Colorcoded).tmTheme",
			"original_color_scheme": "Packages/ayu/ayu-light.tmTheme",
			"theme": "ayu-light.sublime-theme"
		},
		"evening":
		{
			"color_scheme": "Packages/Colorcoder/ayu-mirage (Colorcoded).tmTheme",
			"original_color_scheme": "Packages/ayu/ayu-mirage.tmTheme",
			"theme": "ayu-mirage.sublime-theme"
		},
		"night":
		{
			"color_scheme": "Packages/Colorcoder/ayu-dark (Colorcoded).tmTheme",
			"original_color_scheme": "Packages/ayu/ayu-dark.tmTheme",
			"theme": "ayu-dark.sublime-theme"
		}
	}
 ```
 
 * Profiles can then be changed using the command pallete(ctrl+shift+p) or using key bindings
 
 ###### Setting key binding:
 ```json
 { "keys": ["ctrl+alt+d"], "command": "visual_changer", "args": {"profile_chosen": "day"} }
 ```
 
 ###### Usage example:
 ![Usage Example](https://raw.githubusercontent.com/kivS/Sublime_Text_Visual_Changer/master/example.gif "usage gif")
 
 
 
