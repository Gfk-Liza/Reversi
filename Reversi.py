'''
Reversi
8*8

空白 = -1
〇 = 0
✕ = 1

必ず、(y,x)の順番
'''


def is_in_board(board, y, x):
    return (y > -1 and y < 8 and x > -1 and x < 8)


def count_Stones(board, turn):
    n = 0
    for f in board:
        if f == turn:
            n += 1
    return n


def can_move_search(board, y, x, turn, dirY, dirX):
    flag1 = False
    flag2 = False

    y += dirY
    x += dirX

    while is_in_board(board, y, x):
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


def printBoard(board, turn, hints):
    print('┌──┬───┬───┬───┬───┬───┬───┬───┬───┐')
    print('│  │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │')
    for y in range(8):
        print('├──┼───┼───┼───┼───┼───┼───┼───┼───┤')
        print('│ ' + str(y), end = '│')
        for x in range(8):
            print(
                ' * ' if (hints and can_move(board, y, x, turn)) else 
                '   ' if board[y][x] == -1 else 
                ' 〇' if board[y][x] == 0 else ' ✕ '
                , end='│')
        print()
    print('└──┴───┴───┴───┴───┴───┴───┴───┴───┘')


def ask(board, turn):
    while True:
        try:
            answer = input('Circle>' if turn == 0 else 'Cross> ')
            answer = int(answer)
            if can_move(board, int(str(answer)[0]), int(str(answer)[1]), turn):
                return str(answer)
            print(answer, str(answer)[0], str(answer)[1])
            print('You guys cannot put a stone in its place.')
        except ValueError:
            if (answer in 'hint'):
                print('System> Okay, I understand.')
                printBoard(board, turn, True)
            else:
                print('Do not enter anything other than numbers.')


def question(text):
    while True:
        answer = input(text + '(1 if yes, 0 if no)> ')
        if answer in ['1', '0']:
            return (True if (answer == '1') else False)
        print('Please enter 0 or 1.')


def main():
    #盤面作成
    board = [[ -1 for _ in range(8) ] for _ in range(8)]
    board[3][3] = 0
    board[3][4] = 1
    board[4][3] = 1
    board[4][4] = 0

    print('===REVERSI===')
    mode1 = question('Do you guys want to show hints?')
    turn = 1
    printBoard(board, turn, mode1)
    print('Please enter numbers in the order of length to width.')
    while is_finished(board):
        if is_pass(board, turn):
            ans = ask(board, turn)
            move(board, ans[0], ans[1], turn)
            printBoard(board, turn, mode1)
        else:
            print(('Circle' if turn == 0 else 'Cross'), 'has to pass.')
        turn = 1 - turn
    
    print('\n Finish!! \n')
    
    circle = count_Stones(board, 0)
    cross = count_Stones(board, 1)
    if circle > cross:
        print('Circle won!!)
    elif circle < cross:
        print('Cross won!!')
    else:
        print('Drow!!')

#実行する
main()
