from pyglet import resource
from pyglet.image import ImageGrid


class Image:
    resource.path.append("../res/image")
    resource.reindex()

    background = resource.image("background.png")
    cloud = resource.image("cloud.png")

    score = ImageGrid(resource.image("score.png"), 1, 10)

    dinosaur_run_set = ImageGrid(resource.image("dinosaur_run_set2.png"), 1, 7)
    dinosaur_run_right = dinosaur_run_set[3:5]
    dinosaur_run_left = list(map(lambda x: x.get_transform(flip_x=True), dinosaur_run_right))
    dinosaur_run = [dinosaur_run_left,
                    dinosaur_run_right]

    dinosaur_squat_set = ImageGrid(resource.image("dinosaur_squat_set1.png"), 1, 2)
    dinosaur_squat_right = dinosaur_squat_set
    dinosaur_squat_left = list(map(lambda x: x.get_transform(flip_x=True), dinosaur_squat_right))
    dinosaur_squat = [dinosaur_squat_left,
                      dinosaur_squat_right]

    # 小鸟图片
    bird_left = ImageGrid(resource.image("bird_set.png"), 1, 2)
    bird_right = list(map(lambda x: x.get_transform(flip_x=True), bird_left))
    bird_fly = [bird_left,
                bird_right]
