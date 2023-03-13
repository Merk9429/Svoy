maps = [1, 2, 3,
        4, 5, 6,
        7, 8, 9]

victories = [[0, 1, 2],
             [3, 4, 5],
             [6, 7, 8],
             [0, 3, 6],
             [1, 4, 7],
             [2, 5, 8],
             [0, 4, 8],
             [2, 4, 6]]

def print_maps():
    print("\n")
    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(maps[0], maps[1], maps[2]))
    print('\t_____|_____|_____')

    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(maps[3], maps[4], maps[5]))
    print('\t_____|_____|_____')

    print("\t     |     |")

    print("\t  {}  |  {}  |  {}".format(maps[6], maps[7], maps[8]))
    print("\t     |     |")
    print("\n")

def step_maps(step, symbol):
    ind = maps.index(step)
    maps[ind] = symbol


def get_result():
    win = ""

    for i in victories:
        if maps[i[0]] == "X" and maps[i[1]] == "X" and maps[i[2]] == "X":
            win = "X"
        if maps[i[0]] == "O" and maps[i[1]] == "O" and maps[i[2]] == "O":
            win = "O"

    return win

game_over = False
player1 = True

while game_over == False:

    print_maps()

    if player1 == True:
        symbol = "X"
        step = int(input("Игрок 1, ваш ход: "))
    else:
        symbol = "O"
        step = int(input("Игрок 2, ваш ход: "))

    step_maps(step, symbol)
    win = get_result()
    if win != "":
        game_over = True
    else:
        game_over = False

    player1 = not(player1)

print_maps()
print("Победил", win)