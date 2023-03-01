from cocos.particle_systems import Explosion, Color
from image import Image


class Broken(Explosion):
    size = 7
    size_var = 0
    start_color = Color(99, 155, 255, 1.0)
    start_color_var = Color(0, 0, 0, 0)
    end_color = Color(0.5, 0.5, 0.5, 0.0)
    end_color_var = Color(0.5, 0.5, 0.5, 0.0)
    def __init__(self, pos):
        super().__init__()

        Broken.texture = Image.heart_spec.get_texture()
        self.total_particles = 1
        self.scale = 10
        self.position = pos

