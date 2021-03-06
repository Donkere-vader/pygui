# PyGui
A module that generates Tkinter windows from XML with jinja2 templating.

## Disclaimer
This is a very simple module. If you need very fine control or very special functions of tkinter this module will probably not work for you.

If you really like what I made (which i obviously hope) and you really want a certain function. Either request it or make it yourself and make a pull request.

## Installation
Install my xmlparser from [the repo](https://www.github.com/donkere-vader/xmlparser#installation)

Then move the pygui folder into ur modules folder
(on linux this would result in: ``/usr/lib/python3.8/pygui``)

## Requirements
this script requires the XMLParser I also wrote.

Please install that first.  
See its [repo](https://www.github.com/donkere-vader/xmlparser#installation) for the instructions

It also uses the jinja2 template module so if you've used Flask this should be very easy.

## Usage

### Project structure
Create a *templates* folder in the run environment.
The *templates* folder should contain a *windows* and a *components* folder. like so:
```
static/
    # here go the style sheets
templates/
    components/
        # here go the component .xml files
    windows/
        # here go the window .xml files
```

### How to template
Templating is done in XML (vert similar to HTML).
every tkinter object is a tag.
for example a tkinter label would be defined like so:  
```xml
<label font="arial 20">label text</labels>
```  

and the font="arial 20" is one of the kwargs of the tkinter.Label object.
Every kwargs of an object should work if you include it like an attribute such as font in the example. Except for the text attribute in the case of Labels and Buttons. Those can be inserted as a child of the Label (as also visible in the example above)

And all the templating stuff from jinja2 effects the templating as well. To learn more about that view the jinja2 documentation:
[jinja2 documentation](https://jinja.palletsprojects.com/en/2.11.x/)

#### Templating global variables
If you want to set global variables for within the templating. If you are for example going to use a particullar function a lot you can make it a global variable like so:

```py
global_var = "I'm going to be used a lot"

PyGui.set_globals(global_var=global_var)
```

Calling this function will not change anything about global variables set earlier. Only when you give them the same name, it will be overwritten.

### Make a window
To make a new window create a .xml file in the *templates/windows/* folder.

An example window could be:

### main.xml:
```xml
<root title="Tk window title" geometry="500x500" bg="red">
    <label>
        {{ custom_var }}
    </label>
    <frame row="1">
        <_labels text1="hello" text2="world!" />
    </frame>
</root>
```

### Make a component
Creating a component is almost the same a creating a window.
But this time place the .xml in the *templates/components/* folder.

An example component could be:

### labels.xml
```xml
<frame>
    <label font="arial 20" fg="red" bg="black" column="0">
        {{ text1 }}
    </label>
    <label font="arial 20" fg="green" bg="yellow" column="1">
        {{ text2 }}
    </label>
</frame>
```

### Python
So now we get to actually creating the windows.

this script would show the window *templates/windows/main.xml*
```py
from pygui import PyGui

pygui = PyGui(__name__)

window = pygui.construct('main')
window.show()
```

To pass variables or functions or classes into the jinja2 templating for usage in the template simply do:
```py
window = pygui.construct('main', custom_var='this will be displayed in the template')
```

### images
U can use images as follows:

```py
<image image="images/test.jpg" height="200" />
```

when using the height or width attribute the aspect ratio will stay the same

u can also use the size attribute (or width and height attributes) to force a aspect ratio change

``size="200x200"`` This would force the image to be 200x200
(WIDTHxHEIGHT)

### Input
You can get input in a one-line entry or a multiline text widget.

```xml
<entry id="entry">
    Placeholder text goes here
</entry>
<text id="text">
    Placeholder text for text widget
</text>
```

Getting and setting of the values is inspired by jQuery.
You get values from a entry by calling the ``.val()`` function on an entry or text widget. And settings is done with ``.val('new value')``  

All items are located in the window.items dictionary.

So for example getting the value from the entry above would look like so:

```py
entry_value = window.get_item("entry").val()
```

Spinbox should also work

### Menu
A program menu (with the 'File' and 'Edit' options for example) is also possible with tkinter and this module.

```xml
<root title="Test window" bg="grey22">
    <menu>
        <menu>
            File
            <command command="print('opening file...')">open</command>
        </menu>
    </menu>
</root>
```

Result:  
![The menu in action](https://github.com/donkere-vader/pygui/blob/master/github/images/menu_example.png?raw=true)

### Style sheets
You can make a stylesheet like this:
```json
{
    ".button": {
        "bg": "red"
    },
    "#fuck": {
        "fg": "orange"
    }
}
```
And you need to place it in a static/ folder in the project root.

Then in the xml file you can specify the style sheet in the root tag like so:
```xml
<root title="window title" style="style_sheet_name">
    <frame>
        <button id="fuck" command="print(1)" width="10" height="10" class="button">test</button>
    </frame>
</root>
```
You can add classes and id's to the tags to give them the styling. See the xml and json example above. They go together.
