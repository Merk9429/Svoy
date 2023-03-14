maps = [1, 2, 3,
        4, 5, 6,
        7, 8, 9]

#Для постановки знаков в ячейки будем использовать ряд цифр от 1 до 9

def draw_maps(maps):
    print("\n")
    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(" " if type(maps[0]) == int else maps[0],
                                        " " if type(maps[1]) == int else maps[1],
                                        " " if type(maps[2]) == int else maps[2]))
    print('\t_____|_____|_____')

    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(" " if type(maps[3]) == int else maps[3],
                                        " " if type(maps[4]) == int else maps[4],
                                        " " if type(maps[5]) == int else maps[5]))
    print('\t_____|_____|_____')

    print("\t     |     |")

    print("\t  {}  |  {}  |  {}".format(" " if type(maps[6]) == int else maps[6],
                                        " " if type(maps[7]) == int else maps[7],
                                        " " if type(maps[8]) == int else maps[8]))
    print("\t     |     |")
    print("\n")


def take_input(player_one):
    valid = False
    while not valid:
        player_two = input("Куда поставим " + player_one + "? ")
        try:
            player_two = int(player_two)
        except ValueError:
            print("Некорректный ввод. Вы уверены, что ввели число?")
            continue
        if 1 <= player_two <= 9:
            if str(maps[player_two - 1]) not in "XO":
                maps[player_two - 1] = player_one
                valid = True
            else:
                print("Эта клетка уже занята!")
        else:
            print("Некорректный ввод. Введите число от 1 до 9.")


def result_win(maps):
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for each in win_coord:
        if maps[each[0]] == maps[each[1]] == maps[each[2]]:
            return maps[each[0]]
    return False


def main(maps):
    counter = 0
    win = False
    while not win:
        draw_maps(maps)
        if counter % 2 == 0:
            take_input("X")
        else:
            take_input("O")
        counter += 1

        tmp = result_win(maps)
        if tmp:
            print(tmp, "Выиграл!")
            win = True
            break
        if counter == 9:
            print("Ничья!")
            break
    draw_maps(maps)


main(maps)

input("Нажмите Enter для выхода!")