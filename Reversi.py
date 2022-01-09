import random

'''
Reversi
8*8
Blank = -1
A = 0
B = 1
Always in the order of (y,x)
'''


def is_in_board(y, x):
    return (y >= 0 and y <= 7 and x >= 0 and x <= 7)


def count_stones(board, turn):
    count = 0
    for y in board:
        for x in y:
            if x == turn:
                count += 1
    return count


def list_of_definite_stones(board, turn):
    way_of_reference_point_Y = [  0,  0,  7,  7,  0,  0,  7,  7 ]
    way_of_reference_point_X = [  0,  7,  0,  7,  0,  7,  0,  7 ]
    way_of_moving_Y =          [  1,  0, -1,  0,  0,  1,  0, -1 ]
    way_of_moving_X =          [  0, -1,  0,  1,  1,  0, -1,  0 ]
    
    definite_stone_list = [[ False for _ in range(8)] for _ in range(8)]

    for i, (re_point_Y, re_point_X, wy, wx) in enumerate(zip(way_of_reference_point_Y, way_of_reference_point_X, way_of_moving_Y, way_of_moving_X)):
        if board[re_point_Y][re_point_X] != turn:
            continue

        k = 7
        wky = way_of_moving_Y[(i + 4) % 8]
        wkx = way_of_moving_X[(i + 4) % 8]
        
        for s in range(8):
            n = 1
            y = re_point_Y + s*wky
            x = re_point_X + s*wkx
            if not is_in_board(y, x):
                break
            while board[y][x] == turn and k >= n:
                definite_stone_list[y][x] = True
                y += wy
                x += wx
                n += 1
                if not is_in_board(y, x):
                    break
            if n == 0:
                break
    
    return definite_stone_list


def count_definite_stones(board, turn):
    tmp = list_of_definite_stones(board, turn)
    count = 0

    for y in range(8):
        for x in range(8):
            if tmp[y][x]:
                count += 1
    
    return count

def can_move_search(board, y, x, turn, dirY, dirX):
    flag1 = False
    flag2 = False

    y += dirY
    x += dirX

    while is_in_board(y, x):
        if board[y][x] == 1 - turn:
            flag1 = True
        elif board[y][x] == turn:
            flag2 = True
            break
        elif board[y][x] == -1:
            break
        y += dirY
        x += dirX

    return flag1 and flag2


def can_move(board, y, x, turn):
    if board[y][x] != -1:
        return False
    
    way_of_moving_Y = [ -1, -1,  0,  1,  1,  1,  0, -1 ]
    way_of_moving_X = [  0,  1,  1,  1,  0, -1, -1, -1 ]

    for wy, wx in zip(way_of_moving_Y, way_of_moving_X):
        if (can_move_search(board, y, x, turn, wy, wx)):
            return True
    
    return False


def move(board, str_y, str_x, turn):
    y = int(str_y)
    x = int(str_x)

    way_of_moving_Y = [ -1, -1,  0,  1,  1,  1,  0, -1 ]
    way_of_moving_X = [  0,  1,  1,  1,  0, -1, -1, -1 ]
    
    board[y][x] = turn
    for wy, wx in zip(way_of_moving_Y, way_of_moving_X):
        if (can_move_search(board, y, x, turn, wy, wx)):
            y += wy
            x += wx

            while board[y][x] != turn:
                if board[y][x] == 1 - turn:
                    board[y][x] = turn
                y += wy
                x += wx
            
            y = int(str_y)
            x = int(str_x)
    
    return board


def random_computer(board, turn):
    tmpY = []
    tmpX = []

    for y in range(8):
        for x in range(8):
            if can_move(board, y, x, turn):
                tmpY.append(y)
                tmpX.append(x)
    
    i = random.randrange(0, len(tmpY))

    return str(tmpY[i]) + str(tmpX[i])


def is_pass(board, turn):#パスならばTrue
    for y in range(8):
        for x in range(8):
            if can_move(board, y, x, turn):
                return True
    return False


def is_finished(board): #終了しないならばTrue
    for turn in range(2):
        if is_pass(board, turn):
            return True
    return False


def print_board(board, turn, hints):
    print('┌───┬───┬───┬───┬───┬───┬───┬───┬───┐')
    print('│ \ │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │')

    for y in range(8):
        print('├───┼───┼───┼───┼───┼───┼───┼───┼───┤')
        print('│ ' + str(y), end = ' │')
        for x in range(8):
            print(
                ' * ' if (hints and can_move(board, y, x, turn)) else 
                '   ' if board[y][x] == -1 else 
                ' A ' if board[y][x] == 0 else ' B '
                , end='│')
        print()
    
    print('└───┴───┴───┴───┴───┴───┴───┴───┴───┘')


def ask(board, turn):
    while True:
        try:
            answer = input('A>' if turn == 0 else 'B> ')
            answer = int(answer)
            if can_move(board, int(str(answer)[0]), int(str(answer)[1]), turn):
                return str(answer)
            print('You cannot put a stone in its place.')
        except:
            if (answer in 'hint'):
                print('System> Okay, I understand.')
                print_board(board, turn, True)
            else:
                print('Do not enter anything other than numbers.')


def question(text):
    while True:
        answer = input(text + '(1 if yes, 0 if no)> ')
        if answer in ['1', '0']:
            return (True if (answer == '1') else False)
        print('Enter 0 or 1.')


def main():
    #盤面作成
    board = [[ -1 for _ in range(8) ] for _ in range(8)]
    board[3][3] = 1
    board[3][4] = 0
    board[4][3] = 0
    board[4][4] = 1

    print('===REVERSI===')
    mode1 = question('Do you want to show hints?')
    turn = 0

    print_board(board, turn, mode1)
    print('A : 2\nB : 2')
    print('Enter numbers in the order of length to width.')

    while is_finished(board):
        if is_pass(board, turn):
            if True:
                ans = ask(board, turn)
            else:
                ans = random_computer(board, turn)
            
            move(board, ans[0], ans[1], turn)
            print_board(board, 1 - turn, mode1)
            print('A :', count_stones(board, 0))
            print('B :', count_stones(board, 1))
        else:
            print(('A' if turn == 0 else 'B'), 'has to pass.')
        
        print()
        turn = 1 - turn
    
    print('\n Finish!! \n')
    
    A = count_stones(board, 0)
    B = count_stones(board, 1)
    if A > B:
        print('A has won!!')
    elif A < B:
        print('B has won!!')
    else:
        print('The game ended in a draw.')



#実行する
main()
