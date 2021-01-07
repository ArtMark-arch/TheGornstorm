class person:
    def __init__(self):
        self.hp = 20
        self.dmg = 1
        self.dmg_armor = 'урон оружия'
        self.ran = 'дальность оружия'
        self.pr = 0
        self.pr_arm = 'защита брони'
        self.speed = 10
        self.aks = 'Аксессуар'


class ogr:
    def __init__(self):
        self.hp = 20
        self.dmg = 4
        self.pr = 2
        self.speed = 9
        self.ran = 2


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