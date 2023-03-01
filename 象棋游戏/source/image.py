from pyglet import resource

class Image:
    resource.path.append("../res/img")
    resource.reindex()

    black_pawn = resource.image("black_pawn.png")
    red_pawn = resource.image("red_pawn.png")

    black_car = resource.image("black_car.png")
    red_car = resource.image("red_car.png")

    black_cannon = resource.image("black_cannon.png")
    red_cannon = resource.image("red_cannon.png")

    black_horse = resource.image("black_horse.png")
    red_horse = resource.image("red_horse.png")

    black_elephant = resource.image("black_elephant.png")
    red_elephant = resource.image("red_elephant.png")

    black_guard = resource.image("black_guard.png")
    red_guard = resource.image("red_guard.png")

    black_king = resource.image("black_king.png")
    red_king = resource.image("red_king.png")
