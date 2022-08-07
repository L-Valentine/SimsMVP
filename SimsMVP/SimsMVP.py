from termcolor import cprint
from random import randint


######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умирает от депрессии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:
    money = 0
    food = 0
    cat_food = 0
    fur_coat = 0

    def __init__(self):
        self.money = 100
        self.food = 50
        self.cat_food = 30
        self.dirt = 0

    def __str__(self):
        return 'В доме денег осталось {}, еды осталось {}, кошачьей еды осталось {}, грязи {}'.format(
            self.money, self.food, self.cat_food, int(self.dirt))


class Human:

    def __init__(self):
        self.name = None
        self.house = None
        self.fullness = 30
        self.happiness = 100

    def __str__(self):
        return '{} сытость {} счастья {}'.format(self.name, self.fullness, self.happiness)

    def eat(self):
        if self.house.food >= 30:
            House.food += 30
            cprint('{} поел'.format(self.name), color='yellow')
            self.fullness += 30
            self.house.food -= 30
        else:
            cprint('{} нет еды'.format(self.name), color='red')
            self.fullness -= 5

    def pet_the_cat(self):
        cprint('{} гладил кота'.format(self.name), color='green')
        self.fullness -= 5
        self.happiness += 5

    def act(self):
        self.house.dirt += 2.5
        if self.house.dirt > 90:
            self.happiness -= 10
        if self.fullness <= 0:
            cprint('{} умер от голода...'.format(self.name), color='red')
            return False
        if self.happiness < 10:
            cprint('{} умер от депрессии...'.format(self.name), color='red')
            return False
        if self.fullness < 20:
            self.eat()
            return False
        return True


class Husband(Human):

    def __init__(self, name, house):
        super().__init__()
        self.name = name
        self.house = house

    def __str__(self):
        return super().__str__()

    def act(self):
        if super().act():
            dice = randint(1, 6)
            if self.happiness <= 20:
                self.gaming()
            elif self.house.money < 500:
                self.work()
            elif dice == 1:
                self.work()
            elif dice == 2:
                self.eat()
            elif dice == 3:
                self.pet_the_cat()
            else:
                self.gaming()

    def work(self):
        House.money += 150
        cprint('{} сходил на работу'.format(self.name), color='green')
        self.house.money += 150
        self.fullness -= 10

    def gaming(self):
        cprint('{} играл в WoT'.format(self.name), color='green')
        self.fullness -= 10
        self.happiness += 20


class Wife(Human):

    def __init__(self, name, house):
        super().__init__()
        self.name = name
        self.house = house

    def __str__(self):
        return super().__str__()

    def act(self):
        if super().act():
            dice = randint(1, 6)
            if self.house.food < 20:
                self.shopping()
            elif self.happiness < 30 and self.house.money >= 350:
                self.buy_fur_coat()
            elif self.house.dirt > 100:
                self.clean_house()
            elif dice == 1:
                self.eat()
            elif dice == 2 and self.house.dirt > 99:
                self.clean_house()
            elif dice == 2:
                self.pet_the_cat()
            else:
                self.shopping()

    def shopping(self):
        cprint('{} сходила в магазин'.format(self.name), color='yellow')
        self.house.money -= 60
        self.house.food += 50
        self.house.cat_food += 10
        self.fullness -= 10

    def buy_fur_coat(self):
        House.fur_coat += 1
        cprint('{} купила шубу'.format(self.name), color='magenta')
        self.house.money -= 350
        self.fullness -= 10
        self.happiness += 60

    def clean_house(self):
        cprint('{} прибрала дом'.format(self.name), color='blue')
        self.house.dirt -= randint(10, 100)
        self.fullness -= 10


######################################################## Часть вторая
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов


class Cat:

    def __init__(self, name, house):
        self.name = name
        self.house = house
        self.fullness = 30

    def __str__(self):
        return '{} сытость {}'.format(self.name, self.fullness)

    def act(self):
        if self.fullness <= 0:
            cprint('{} умер от голода...'.format(self.name), color='red')
            return
        if self.fullness < 20:
            self.eat()
            return
        dice = randint(1, 5)
        if dice == 1:
            self.sleep()
        elif dice == 2:
            self.eat()
        else:
            self.soil()

    def eat(self):
        if self.house.food >= 10:
            House.cat_food += 10
            cprint('{} поел'.format(self.name), color='yellow')
            self.fullness += 20
            self.house.food -= 10
        else:
            cprint('{} нет еды'.format(self.name), color='red')
            self.fullness -= 5

    def sleep(self):
        cprint('{} поспал'.format(self.name), color='green')
        self.fullness -= 10

    def soil(self):
        cprint('{} подрал обои'.format(self.name), color='magenta')
        self.fullness -= 10
        self.house.dirt += 10


######################################################## Часть третья
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда ==100 ;)

class Child(Human):

    def __init__(self, name, house):
        super().__init__()
        self.name = name
        self.house = house
        self.happiness = 100

    def __str__(self):
        return super().__str__()

    def act(self):
        if self.fullness <= 0:
            cprint('{} умер от голода...'.format(self.name), color='red')
            return
        if self.fullness < 20:
            self.eat()
            return
        dice = randint(1, 4)
        if dice == 1:
            self.eat()
        elif dice == 2:
            self.sleep()
        else:
            self.sleep()

    def eat(self):
        if self.house.food >= 10:
            House.food += 10
            cprint('{} поел'.format(self.name), color='cyan')
            self.fullness += 10
            self.house.food -= 10
        else:
            cprint('{} нет еды'.format(self.name), color='red')
            self.fullness -= 5

    def sleep(self):
        cprint('{} поспал'.format(self.name), color='magenta')


######################################################## Action!

home = House()
serge = Husband(name='Сережа', house=home)
masha = Wife(name='Маша', house=home)
kolya = Child(name='Коля', house=home)
murzik = Cat(name='Мурзик', house=home)

for day in range(365):
    cprint('================== День {} =================='.format(day), color='red')
    serge.act()
    masha.act()
    kolya.act()
    murzik.act()
    cprint(serge, color='cyan')
    cprint(masha, color='cyan')
    cprint(kolya, color='cyan')
    cprint(murzik, color='cyan')

print('Заработано за год денег:', House.money)
print('Съедено за год еды:', House.food)
print('Съедено за год кошачьей еды:', House.cat_food)
print('Куплено за год шуб:', House.fur_coat)
