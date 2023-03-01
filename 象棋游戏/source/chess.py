from cocos.sprite import Sprite

from image import Image
from point import Point


class Chess(Sprite):
    def __init__(self, pos: Point, name, camp):  # camp阵营
        if camp == "red":
            super().__init__(eval("Image.red_" + name))
        else:
            super().__init__(eval("Image.black_" + name))

        self.camp = camp
        self.name = name
        self.pos = pos
        self.grid_size, self.origin = self.pos.grid_size, self.pos.origin

        self.position = pos.real_pos
        self.rect = self.get_rect()

    def move(self, rect, all_chess, mode):
        self.rect = rect
        self.pos.update(rect)
        self.position = self.pos.real_pos
        if mode == "eat":
            for ces in all_chess:
                if ces.pos == self.pos and ces.camp != self.camp:  # 位置相同, 且是敌军
                    ces.kill()
                    all_chess.remove(ces)
                    break

    def __repr__(self):
        return f"{self.name} -> {self.camp}"


class Pawn(Chess):
    def __init__(self, pos, camp):
        super().__init__(pos, "pawn", camp)

    def check_valid(self, x, y, all_chess):
        if y > 9 or y < 0 or x < 0 or x > 8:  # 是否越界
            return False
        for ces in all_chess:
            if ces != self:
                if ces.pos.pos == (x, y) and ces.camp == self.camp:
                    return False
        return True

    def try_move(self, all_chess):
        if self.camp == "black":
            if self.pos.y < 5:
                if self.check_valid(self.pos.x, self.pos.y + 1, all_chess):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, self.pos.y + 1)
            else:
                if self.check_valid(self.pos.x, self.pos.y + 1, all_chess):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, self.pos.y + 1)
                if self.check_valid(self.pos.x - 1, self.pos.y, all_chess):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 1, self.pos.y)
                if self.check_valid(self.pos.x + 1, self.pos.y, all_chess):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 1, self.pos.y)
        else:
            if self.pos.y > 4:
                if self.check_valid(self.pos.x, self.pos.y - 1, all_chess):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, self.pos.y - 1)
            else:
                if self.check_valid(self.pos.x, self.pos.y - 1, all_chess):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, self.pos.y - 1)
                if self.check_valid(self.pos.x - 1, self.pos.y, all_chess):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 1, self.pos.y)
                if self.check_valid(self.pos.x + 1, self.pos.y, all_chess):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 1, self.pos.y)


class Car(Chess):
    def __init__(self, pos, camp):
        super().__init__(pos, "car", camp)

    def check_valid(self, x, y, all_chess):
        if y > 9 or y < 0 or x < 0 or x > 8:  # 是否越界
            return False
        for ces in all_chess:
            if ces != self:
                if ces.pos.pos == (x, y) and ces.camp == self.camp:
                    return False
        return True

    def blocked(self, all_chess, x, y):
        for ces in all_chess:
            if ces != self:
                if ces.pos.pos == (x, y):
                    return True
        return False

    def try_move(self, all_chess):
        for x in range(self.pos.x - 1, -1, -1):
            if self.check_valid(x, self.pos.y, all_chess):
                if not self.blocked(all_chess, x + 1, self.pos.y):  # +1延迟判断block
                    yield Point(self.pos.grid_size, self.pos.origin, x, self.pos.y)
                else:
                    break
        for x in range(self.pos.x + 1, 9):
            if self.check_valid(x, self.pos.y, all_chess):
                if not self.blocked(all_chess, x - 1, self.pos.y):
                    yield Point(self.pos.grid_size, self.pos.origin, x, self.pos.y)
                else:
                    break
        for y in range(self.pos.y + 1, 10):
            if self.check_valid(self.pos.x, y, all_chess):
                if not self.blocked(all_chess, self.pos.x, y - 1):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, y)
                else:
                    break
        for y in range(self.pos.y - 1, -1, -1):
            if self.check_valid(self.pos.x, y, all_chess):
                if not self.blocked(all_chess, self.pos.x, y + 1):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, y)
                else:
                    break


class Cannon(Chess):
    def __init__(self, pos, camp):
        super().__init__(pos, "cannon", camp)

    def check_valid(self, x, y, all_chess):
        if y > 9 or y < 0 or x < 0 or x > 8:  # 是否越界
            return False
        for ces in all_chess:
            if ces != self:
                if ces.pos.pos == (x, y) and ces.camp == self.camp:
                    return False
        return True

    def blocked(self, all_chess, x, y):
        for ces in all_chess:
            # print(ces.pos.pos, (x, y), ces.pos.pos==(x, y),ces, self, ces == self)
            if ces != self:
                if ces.pos.pos == (x, y):
                    return True
        return False

    def is_enemy(self, all_chess, x, y):
        for ces in all_chess:
            if ces.pos.pos == (x, y):
                if ces.camp == self.camp:
                    return False
                return True

    # 找到隔山打牛的对象
    def find_enemy(self, all_chess):
        count = 0
        for x in range(self.pos.x - 1, -1, -1):
            if self.blocked(all_chess, x, self.pos.y):
                count += 1
                if count == 2:
                    if self.is_enemy(all_chess, x, self.pos.y):
                        yield Point(self.pos.grid_size, self.pos.origin, x, self.pos.y)
                    break
        count = 0
        for x in range(self.pos.x + 1, 9, 1):
            if self.blocked(all_chess, x, self.pos.y):
                count += 1
                if count == 2:
                    if self.is_enemy(all_chess, x, self.pos.y):
                        yield Point(self.pos.grid_size, self.pos.origin, x, self.pos.y)
                    break
        count = 0
        for y in range(self.pos.y + 1, 10):
            if self.blocked(all_chess, self.pos.x, y):
                count += 1
                if count == 2:
                    if self.is_enemy(all_chess, self.pos.x, y):
                        yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, y)
                    break
        count = 0
        for y in range(self.pos.y - 1, -1, -1):
            if self.blocked(all_chess, self.pos.x, y):
                count += 1
                if count == 2:
                    if self.is_enemy(all_chess, self.pos.x, y):
                        yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, y)
                    break

    def try_move(self, all_chess):
        for x in reversed(range(self.pos.x)):
            if self.check_valid(x, self.pos.y, all_chess):  # 这个位置可以吃或走
                if not self.blocked(all_chess, x, self.pos.y):
                    yield Point(self.pos.grid_size, self.pos.origin, x, self.pos.y)
                else:  # 挡到了就不要再往下找了
                    break
            else:  # 如果只有一个break无法保证, 100%break, 挡住的那颗棋子会漏过去(我是sb)
                break
        for x in range(self.pos.x + 1, 9):
            if self.check_valid(x, self.pos.y, all_chess):
                if not self.blocked(all_chess, x, self.pos.y):
                    yield Point(self.pos.grid_size, self.pos.origin, x, self.pos.y)
                else:
                    break
            else:
                break
        for y in range(self.pos.y + 1, 10):
            if self.check_valid(self.pos.x, y, all_chess):
                if not self.blocked(all_chess, self.pos.x, y):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, y)
                else:
                    break
            else:
                break
        for y in reversed(range(self.pos.y)):
            if self.check_valid(self.pos.x, y, all_chess):
                if not self.blocked(all_chess, self.pos.x, y):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, y)
                else:
                    break
            else:
                break
        for route in self.find_enemy(all_chess):
            yield route


class Horse(Chess):
    def __init__(self, pos, camp):
        super().__init__(pos, "horse", camp)

    def check_valid(self, x, y, all_chess):
        if y > 9 or y < 0 or x < 0 or x > 8:  # 是否越界
            return False
        for ces in all_chess:
            if ces != self:
                if ces.pos.pos == (x, y) and ces.camp == self.camp:
                    return False
        return True

    def blocked(self, all_chess, delta_x, delta_y):
        for ces in all_chess:
            if ces != self:
                if ces.pos.pos == (self.pos.x + delta_x, self.pos.y + delta_y):
                    return True
        return False

    def try_move(self, all_chess):
        if self.check_valid(self.pos.x + 1, self.pos.y + 2, all_chess):
            if not self.blocked(all_chess, 0, 1):
                yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 1, self.pos.y + 2)
        if self.check_valid(self.pos.x + 2, self.pos.y + 1, all_chess):
            if not self.blocked(all_chess, 1, 0):
                yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 2, self.pos.y + 1)
        if self.check_valid(self.pos.x + 2, self.pos.y - 1, all_chess):
            if not self.blocked(all_chess, 1, 0):
                yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 2, self.pos.y - 1)
        if self.check_valid(self.pos.x + 1, self.pos.y - 2, all_chess):
            if not self.blocked(all_chess, 0, -1):
                yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 1, self.pos.y - 2)
        if self.check_valid(self.pos.x - 1, self.pos.y - 2, all_chess):
            if not self.blocked(all_chess, 0, -1):
                yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 1, self.pos.y - 2)
        if self.check_valid(self.pos.x - 2, self.pos.y - 1, all_chess):
            if not self.blocked(all_chess, -1, 0):
                yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 2, self.pos.y - 1)
        if self.check_valid(self.pos.x - 2, self.pos.y + 1, all_chess):
            if not self.blocked(all_chess, -1, 0):
                yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 2, self.pos.y + 1)
        if self.check_valid(self.pos.x - 1, self.pos.y + 2, all_chess):
            if not self.blocked(all_chess, 0, 1):
                yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 1, self.pos.y + 2)


class Elephant(Chess):
    def __init__(self, pos, camp):
        super().__init__(pos, "elephant", camp)

    def check_valid(self, x, y, all_chess, camp):
        if camp == "black":
            if y > 4 or y < 0 or x < 0 or x > 8:  # 是否越界
                return False
        else:
            if y < 5 or y > 9 or x < 0 or x > 8:  # 是否越界
                return False
        for ces in all_chess:
            if ces != self:
                if ces.pos.pos == (x, y) and ces.camp == self.camp:
                    return False
        return True

    def blocked(self, all_chess, delta_x, delta_y):
        for ces in all_chess:
            if ces != self:
                if ces.pos.pos == (self.pos.x + delta_x, self.pos.y + delta_y):
                    return True
        return False

    def try_move(self, all_chess):
        if self.camp == "black":
            if self.pos.y < 5:
                if self.check_valid(self.pos.x + 2, self.pos.y + 2, all_chess, "black"):
                    if not self.blocked(all_chess, 1, 1):
                        yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 2, self.pos.y + 2)
                if self.check_valid(self.pos.x - 2, self.pos.y + 2, all_chess, "black"):
                    if not self.blocked(all_chess, -1, 1):
                        yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 2, self.pos.y + 2)
                if self.check_valid(self.pos.x + 2, self.pos.y - 2, all_chess, "black"):
                    if not self.blocked(all_chess, 1, -1):
                        yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 2, self.pos.y - 2)
                if self.check_valid(self.pos.x - 2, self.pos.y - 2, all_chess, "black"):
                    if not self.blocked(all_chess, -1, -1):
                        yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 2, self.pos.y - 2)
        else:
            if self.pos.y > 4:
                if self.check_valid(self.pos.x + 2, self.pos.y + 2, all_chess, "red"):
                    if not self.blocked(all_chess, 1, 1):
                        yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 2, self.pos.y + 2)
                if self.check_valid(self.pos.x - 2, self.pos.y + 2, all_chess, "red"):
                    if not self.blocked(all_chess, -1, 1):
                        yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 2, self.pos.y + 2)
                if self.check_valid(self.pos.x + 2, self.pos.y - 2, all_chess, "red"):
                    if not self.blocked(all_chess, 1, -1):
                        yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 2, self.pos.y - 2)
                if self.check_valid(self.pos.x - 2, self.pos.y - 2, all_chess, "red"):
                    if not self.blocked(all_chess, -1, -1):
                        yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 2, self.pos.y - 2)


class Guard(Chess):
    def __init__(self, pos, camp):
        super().__init__(pos, "guard", camp)

    def check_valid(self, x, y, all_chess, camp):
        if camp == "black":
            if y > 2 or y < 0 or x < 3 or x > 5:  # 是否越界
                return False
        else:
            if y < 7 or y > 9 or x < 3 or x > 5:  # 是否越界
                return False
        for ces in all_chess:
            if ces != self:
                if ces.pos.pos == (x, y) and ces.camp == self.camp:
                    return False
        return True

    def try_move(self, all_chess):
        if self.camp == "black":
            if self.pos.y < 3:
                if self.check_valid(self.pos.x + 1, self.pos.y + 1, all_chess, "black"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 1, self.pos.y + 1)
                if self.check_valid(self.pos.x - 1, self.pos.y + 1, all_chess, "black"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 1, self.pos.y + 1)
                if self.check_valid(self.pos.x + 1, self.pos.y - 1, all_chess, "black"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 1, self.pos.y - 1)
                if self.check_valid(self.pos.x - 1, self.pos.y - 1, all_chess, "black"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 1, self.pos.y - 1)
        else:
            if self.pos.y > 6:
                if self.check_valid(self.pos.x + 1, self.pos.y + 1, all_chess, "red"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 1, self.pos.y + 1)
                if self.check_valid(self.pos.x - 1, self.pos.y + 1, all_chess, "red"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 1, self.pos.y + 1)
                if self.check_valid(self.pos.x + 1, self.pos.y - 1, all_chess, "red"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 1, self.pos.y - 1)
                if self.check_valid(self.pos.x - 1, self.pos.y - 1, all_chess, "red"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 1, self.pos.y - 1)


class King(Chess):
    def __init__(self, pos, camp):
        super().__init__(pos, "king", camp)

    def check_valid(self, x, y, all_chess, camp):
        if camp == "black":
            if y > 2 or y < 0 or x < 3 or x > 5:  # 是否越界
                return False
        else:
            if y < 7 or y > 9 or x < 3 or x > 5:  # 是否越界
                return False
        for ces in all_chess:
            if ces != self:
                if ces.pos.pos == (x, y) and ces.camp == self.camp:
                    return False
        return True

    def try_move(self, all_chess):
        if self.camp == "black":
            if self.pos.y < 3:
                if self.check_valid(self.pos.x, self.pos.y + 1, all_chess, "black"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, self.pos.y + 1)
                if self.check_valid(self.pos.x, self.pos.y - 1, all_chess, "black"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, self.pos.y - 1)
                if self.check_valid(self.pos.x + 1, self.pos.y, all_chess, "black"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 1, self.pos.y)
                if self.check_valid(self.pos.x - 1, self.pos.y, all_chess, "black"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 1, self.pos.y)
        else:
            if self.pos.y > 6:
                if self.check_valid(self.pos.x, self.pos.y + 1, all_chess, "red"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, self.pos.y + 1)
                if self.check_valid(self.pos.x, self.pos.y - 1, all_chess, "red"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, self.pos.y - 1)
                if self.check_valid(self.pos.x + 1, self.pos.y, all_chess, "red"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x + 1, self.pos.y)
                if self.check_valid(self.pos.x - 1, self.pos.y, all_chess, "red"):
                    yield Point(self.pos.grid_size, self.pos.origin, self.pos.x - 1, self.pos.y)
        for route in self.judge_fly_king(all_chess):
            yield route

    def judge_fly_king(self, all_chess):
        if self.camp == "black":
            name = None
            for y in range(self.pos.y, 10):
                for ces in all_chess:
                    if ces != self:
                        if ces.pos.pos == (self.pos.x, y):
                            name = ces.name
                            break
                else:
                    continue
                break
            if name == "king":
                yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, y)

        else:
            name = None
            for y in reversed(range(self.pos.y)):
                for ces in all_chess:
                    if ces != self:
                        if ces.pos.pos == (self.pos.x, y):
                            name = ces.name
                            break
                else:
                    continue
                break
            if name == "king":
                yield Point(self.pos.grid_size, self.pos.origin, self.pos.x, y)
