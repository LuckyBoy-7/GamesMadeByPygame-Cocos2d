from pyglet.resource import media
from pyglet import resource
import pyglet.media


class Sound:
    resource.path.append("../res/sound")
    resource.reindex()

    beef = media("beef.mp3", streaming=False)
    bread = media("bread.mp3", streaming=False)
    butter = media("butter.mp3", streaming=False)
    cucumber = media("cucumber.mp3", streaming=False)
    onion = media("onion.mp3", streaming=False)
    over = media("over.mp3", streaming=False)
    tomato = media("tomato.mp3", streaming=False)
    tomato_jam = media("tomato_jam.mp3", streaming=False)
    vegetable = media("vegetable.mp3", streaming=False)
    beginning = media("beginning.mp3", streaming=False)


