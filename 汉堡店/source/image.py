from pyglet import resource


class Image:
    resource.path.append("../res/image")
    resource.reindex()

    beef = resource.image("beef.png")
    butter = resource.image("butter.png")
    onion = resource.image("onion.png")
    tomato = resource.image("tomato.png")
    tomato_jam = resource.image("tomato_jam.png")
    vegetable = resource.image("vegetable.png")
    bottom_bread = resource.image("bottom_bread.png")
    top_bread = resource.image("top_bread.png")
    cucumber = resource.image("cucumber.png")

