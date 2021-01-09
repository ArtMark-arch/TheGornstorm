class person:
    def __init__(self):
        self.hp = 20
        self.dmg = 4
        self.dmg_armor = 'урон оружия'
        self.ran = 'дальность оружия'
        self.pr_arm = 'защита брони'
        self.speed = 10
        self.aks = 'Аксессуар'

    def move(self):
        pass

    def attack(self, pers):
        self.atc = self.dmg - pers.self.pr
        pers.self.hp = pers.self.hp - self.atc

    def heal(self):
        self.hp += 1 #в 2 секунды, спустя 5 секунд после получения урона, += 1 в секунду спустя 10 секунд после получения урона


class ogr:
    def __init__(self):
        self.hp = 20
        self.dmg = 4
        self.pr = 2
        self.speed = 9
        self.ran = 2

    def move(self):
        pass

    def attack(self, pers):
        self.atc = self.dmg - pers.self.pr_arm
        pers.self.hp = pers.self.hp - self.atc

    def heal(self):
        self.hp += 1  # в 2 секунды, спустя 5 секунд после получения урона, += 1 в секунду спустя 10 секунд после получения урона


class ogr_stone(ogr):
    def __init__(self):
        self.abil = 'с шансом 15% оглушение(заморозка) на 2 секунды'
        self.hp = 20
        self.dmg = 5
        self.pr = 2
        self.speed = 7
        self.ran = 1


class ogr_pois(ogr):
    def __init__(self):
        self.abil = 'с шансом 10% отравление на 3 секунды, 2 жизни(без учёта обычной брони) в секунду'
        self.hp = 20
        self.dmg = 3
        self.pr = 2
        self.speed = 9
        self.ran = 2


class ogr_wat(ogr):
    def __init__(self):
        self.abil = 'с шансом 15% замедление на 4 секунды, 3 пикселя'
        self.hp = 15
        self.dmg = 4
        self.pr = 2
        self.speed = 9
        self.ran = 3