from random import randint, choice


def roll_dice(dice:int) -> int:
    a = []
    for i in range(5):
        a.append(randint(1, dice))
    return choice(a)

def roll_multi_dice(num_rolls:int, dice:int) -> list:
    '''Roll 2x D6 -> [a, b]'''
    rolls = []
    for _ in range(num_rolls):
        rolls.append(roll_dice(dice))
    return rolls


def Roll_Dice(num_rolls:int, dice:int) -> list:
    '''Roll 2d6 -> [a, b]'''
    rolls = []
    for _ in range(num_rolls):
        a = []
        # to add more randness, roll 5x , pick one at rand
        for i in range(5):
            a.append(randint(1, dice))
        rolls.append(choice(a))
    return rolls




if __name__ == '__main__':
    dice = [4, 6, 8, 10, 12, 20]

    print(f'\nSingle:')
    for d in dice:
        print(f'\td{d} [{roll_dice(d)}]')

    print('\nMulti Roll:')
    for d in dice:
        num_rolls = randint(2,4)
        print(f'\t{num_rolls}d{d} -> {roll_multi_dice(num_rolls, d)}')

    print('\nSingle Func Roll:')
    for d in dice:
        num_rolls = randint(2, 4)
        print(f'\t{num_rolls}d{d} -> {Roll_Dice(num_rolls, d)}')
