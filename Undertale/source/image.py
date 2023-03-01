from pyglet import resource
from pyglet.image import ImageGrid, load


class Image:
    resource.path.append("../res/image")
    resource.reindex()

    heart = resource.image("heart.png")
    heart_spec = load("../res/image/heart.png")

    sans_lower_part = resource.image("sans_lower_part.png")
    sans_middle_part = resource.image("sans_middle_part.png")
    sans_upper_part = resource.image("sans_upper_part.png")

    bubble = resource.image("bubble.png")

    bone = resource.image("bone2.png")

    attack = ImageGrid(resource.image("attack.png"), 1, 5)




