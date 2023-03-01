from pyglet.resource import image
from pyglet.image import ImageGrid, Animation


class Image:
    # 人物
    i_stand_right = image("stand.png")
    i_stand_left = i_stand_right.get_transform(flip_x=True)

    stand = [i_stand_left,
             i_stand_right]

    runset = ImageGrid(image("runset.png"), 1, 4)
    i_run_right = runset[0:4]
    i_run_left = list(map(lambda x: x.get_transform(flip_x=True), runset[0:4]))

    run = [i_run_left,
           i_run_right]

    jumpset = ImageGrid(image("jumpset.png"), 1, 2)
    i_jump_right = jumpset[0:2]
    i_jump_left = list(map(lambda x: x.get_transform(flip_x=True), jumpset[0:2]))

    jump = [i_jump_left,
            i_jump_right]

    fallset = ImageGrid(image("fallset.png"), 1, 2)
    i_fall_right = fallset[0:2]
    i_fall_left = list(map(lambda x: x.get_transform(flip_x=True), fallset[0:2]))

    fall = [i_fall_left,
            i_fall_right]

    # 刺
    spike_up = image("spike.png")
    spike_down = spike_up.get_transform(rotate=180)
    spike_right = spike_up.get_transform(rotate=90)
    spike_left = spike_up.get_transform(rotate=270)

    # 溅血特效
    blood = image("blood.png")
