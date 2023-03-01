from cocos.actions import MoveBy


class Trap:
    def __init__(self, objects_layer, maplayer):
        all_trap = objects_layer.match(label="trap")
        self.trap_dict = {}
        for trap in all_trap:
            self.trap_dict[trap["index"]] = [maplayer.get_at_pixel(*trap.position), False]

    def update(self, rect):
        # print(self.trap_dict)
        if rect.intersects(self.trap_dict[1][0]):
            self.trap_dict[1][1] = True
        elif rect.intersects(self.trap_dict[2][0]):
            self.trap_dict[2][1] = True
        elif rect.intersects(self.trap_dict[3][0]):
            self.trap_dict[3][1] = True
        elif rect.intersects(self.trap_dict[4][0]):
            self.trap_dict[4][1] = True
        elif rect.intersects(self.trap_dict[5][0]):
            self.trap_dict[5][1] = True

    def touch(self, spikes):
        for order in range(len(self.trap_dict), 0, -1):
            trap = self.trap_dict[order]
            if trap[1]:
                break
        else:
            order = 0
        if order == 1:
            spikes[26].do(MoveBy((0, 100), 2))
        # 剩下的回来做
