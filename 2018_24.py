from codecs import open
import operator


class Group:
    def __init__(self, no, units, hitpoints, attack, attacktype, initiative, weakness, immunities):
        self.id = no
        self.units = units
        self.hitpoints = hitpoints
        self.attack = attack
        self.attacktype = attacktype
        self.weakness = weakness
        self.immunities = immunities
        self.initiative = initiative
        self.alive = True
        self.eff_power = units * attack
        self.target = None

    def get_attacked(self, attacker):
        if attacker.attacktype in self.immunities:
            damage = 0
        else:
            damage = attacker.units * attacker.attack

        if attacker.attacktype in self.weakness:
            damage *= 2

        self.units -= damage//self.hitpoints

        self.eff_power = self.units * self.attack

        if self.units < 1:
            self.alive = False

    def get_damage(self, target):
        if self.attacktype in target.immunities:
            return 0
        else:
            damage = self.units * self.attack
            if self.attacktype in target.weakness:
                damage *= 2
            return damage

    def select_target(self, targets):
        damages = []
        for target in targets:
            damages.append(self.get_damage(target))

        sub_targets = []
        for index, dmg in enumerate(damages):
            if dmg == max(damages):
                sub_targets.append(index)

        if len(sub_targets) == 0:
            return None
        if len(sub_targets) == 1:
            return targets.pop(sub_targets[0])
        else:
            # print(self.id)
            # print(sub_targets)
            sub_targets = [targets[i] for i in sub_targets]
            sub_targets.sort(key=operator.attrgetter('eff_power', 'initiative'), reverse=True)
            # for i, thing in enumerate(sub_targets):
            #     print(i, thing.id, thing.eff_power, thing.initiative)
            # print(sub_targets[0].id)
            targets.remove(sub_targets[0])
            # exit()
            return sub_targets[0]

    def act(self):
        if self.target is not None:
            self.target.get_attacked(self)


def parse_lines(lines, key):
    key = key + "_"
    unes = []
    no = 0
    for group in lines:
        group = group.split(" ")

        units = int(group[0])
        hp = int(group[4])
        attack = int(group[len(group) - 6])
        attack_type = group[len(group) - 5]
        initiative = int(group[len(group) - 1])

        immunities = {}
        weakness = {}

        group = " ".join(group[7:len(group) - 11])
        group = group[1:len(group) - 1].replace(",", "")
        group = [item.strip().split(" ") for item in group.split(";")]

        for item in group:
            if "immune" in item:
                immunities = set(item[2:])
            if "weak" in item:
                weakness = set(item[2:])
        #print(key + str(no + 1),units * attack,  units, hp, attack, attack_type, initiative, weakness, immunities)
        unes.append(Group(key + str(no + 1), units, hp, attack, attack_type, initiative, weakness, immunities))
        no += 1

    return unes


def parse_input(file_name):
    with open(file_name) as file:
        text = [line.strip() for line in file.readlines()]

    if "Immune" in text[0]:
        first = 1
    else:
        first = 2

    for index, line in enumerate(text[1:]):
        if "Immune" in line or "Infection" in line:
            if first == 1:
                return text[1:index], text[index + 2:]
            else:
                return text[index + 2:], text[1:index]


immune, infection = parse_input("G:\\24daysofcode\\input_22.txt")

immune_group = parse_lines(immune, "IMM")
infection_group = parse_lines(infection, "INF")


while len(immune_group) > 0 and len(infection_group) > 0:
    immune_group.sort(key=operator.attrgetter('eff_power', 'initiative'), reverse=True)
    infection_group.sort(key=operator.attrgetter('eff_power', 'initiative'), reverse=True)

    immune_select = immune_group[:]
    infection_select = infection_group[:]

    for attacker in immune_group:
        attacker.target = attacker.select_target(infection_select)

    for attacker in infection_group:
        attacker.target = attacker.select_target(immune_select)

    combine = immune_group + infection_group
    combine.sort(key=operator.attrgetter('initiative'), reverse=True)

    print("-----------------------")
    for attacker in combine:
        if attacker.target is not None:
            print(attacker.id, "attacks", attacker.target.id, "killing", attacker.get_damage(attacker.target)//attacker.target.hitpoints, attacker.target.hitpoints, attacker.get_damage(attacker.target))
        else:
            print(attacker.id)
        if attacker.alive:
            attacker.act()

    immune_group = [group for group in immune_group if group.alive is True]
    infection_group = [group for group in infection_group if group.alive is True]
    combine = immune_group + infection_group

    #exit()

sum = 0
for survivor in combine:
    print(survivor.id, survivor.units)
    sum += survivor.units

print("\nPart 1:",sum)

# 684
# 3029
# 80
# 1020 moet 1019
# 5779 moet 5775
# 114
# 3883
# 87 moet 83
# 7975
# 25


# 22667 is so close
# 22676 is correct
# 23247 too high