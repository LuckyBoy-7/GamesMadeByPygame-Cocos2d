from cocos.director import director

from game import MyScene, MyLayer


def run_game():
    director.init(
        width=1200,
        height=800
    )

    director.run(MyScene(MyLayer()))


if __name__ == "__main__":
    run_game()