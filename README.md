# PyGui
A module based on Tkinter that shows windows constructed from xml

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
``<label font="arial 20">label text</labels>``  

and the font="arial 20" is one of the kwargs of the tkinter.Label object.
Every kwargs of an object should work if you include it like an attribute such as font in the example. Except for the text attribute in the case of Labels and Buttons. Those can be inserted as a child of the Label (as also visible in the example above)

And all the templating stuff from jinja2 effects the templating as well. To learn more about that view the jinja2 documentation.
[jinja2 documentation](https://jinja.palletsprojects.com/en/2.11.x/)

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