import graphics as gr

def setupInitialPositions(player, pieces, player_num, isBackRow):
    '''
    Purpose: Initializes pieces starting position, current position, image, and
    graphic object type
    Inputs: player (dict), pieces (list), player_num (int), isBackRow (bool)
    Returns: player (dict)
    '''
    #uses a counter to keep track of which column we're in and which image to use
    i = 0
    columns = 'ABCDEFGH'
    images = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight',
              'rook']
    # determines which row to place pieces in depending on if the pieces are
    # back row or front row and which player it is
    if isBackRow:
        if player_num == 1:
            row_num = 8
        else:
            row_num = 1
    else:
        if player_num == 1:
            row_num = 7
        else:
            row_num = 2
    #loops through the list of pieces and initializes the position and image
    for piece in pieces:
        pos = '{}{}'.format(columns[i],row_num)
        if isBackRow:
            img = '../img/{}{}.png'.format(images[i],player_num)
        else:
            img = '../img/pawn{}.png'.format(player_num)
        infoC = {'ipos': pos, 'cpos': pos, 'imgName':img, 'gObj':None}
        player[piece] = infoC
        i += 1
    return(player)


def setupPieceInfo():
    '''
    Purpose: Initializes a dictionary for each player's pieces, and combines the
            two dictionaries into a list
    Inputs: none
    Returns: pieces (dict)
    '''
    backRow = ['RookL', 'KnightL', 'BishopL', 'Queen', 'King', 'BishopR',
               'KnightR', 'RookR']
    frontRow = ['Pawn1', 'Pawn2', 'Pawn3', 'Pawn4', 'Pawn5', 'Pawn6', 'Pawn7',
                'Pawn8']
    player1 = {}
    player2 = {}
    player1.update(setupInitialPositions(player1, backRow, 1, True))
    player1.update(setupInitialPositions(player1, frontRow, 1, False))
    player2.update(setupInitialPositions(player2, backRow, 2, True))
    player2.update(setupInitialPositions(player2, frontRow, 2, False))
    pieces = [player1, player2]
    return(pieces)


def setupLabels(sp, increment_w, increment_h):
    '''
    Purpose: setups dictionaries containing the row and column labels
    Inputs: sp (float), increment_w (float), increment_h (float)
    Returns: labelDict (dict)
    '''
    labelDict = {}
    col_num = 1
    row_num = 1
    for char in 'ABCDEFGH':
        p_x = sp[0] + (increment_w * col_num) - increment_w/2
        p_y = sp[1]/2
        labelDict[char] = gr.Point(p_x,p_y)
        col_num += 1
    for num in '12345678':
        p_x = sp[0]/2
        p_y = sp[1] + (increment_h * row_num) - increment_h/2
        labelDict[num] = gr.Point(p_x,p_y)
        row_num +=1
    return labelDict


def setupBoard(sp,width,height,colors):
    '''
    Purpose: setups the initial state of the board (the coordinates of each
    square, the colour of the squares, and the row/column labels)
    Inputs: sp (float), width (float), height (float), colors (list)
    Returns: boardDict (dict), labelDict (dict)
    '''
    boardDict = {}
    increment_width = width / 8
    increment_height = height / 8
    row_num = 0
    col_num = 0
    #loops through the rows and columns, setting up the lower right corner
    #point, centre point, and upper left corner point
    for num in range(1, 9):
        for char in 'ABCDEFGH':
            key = char + str(num)
            up_x = sp[0] + col_num * increment_width
            up_y = sp[1] + row_num * increment_height
            cp_x = up_x + increment_width / 2
            cp_y = up_y + increment_width / 2
            lp_x = up_x + increment_width
            lp_y = up_y + increment_height
            color_index = (row_num + col_num) % 2
            color = colors[color_index]
            boardDict[key] = {'up': gr.Point(up_x,up_y),
                              'cp':gr.Point(cp_x,cp_y),
                              'lp': gr.Point(lp_x,lp_y),
                              'color':color
                             }
            col_num += 1
        col_num = 0
        row_num += 1
    labelDict = setupLabels(sp, increment_width, increment_height)
    return(boardDict, labelDict)