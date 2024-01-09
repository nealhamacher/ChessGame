import graphics as gr
from moves import *

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
            img = 'img/{}{}.png'.format(images[i],player_num)
        else:
            img = 'img/pawn{}.png'.format(player_num)
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


def setupBoardInfo(sp,width,height,colors):
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


def drawButton(board, sp, board_width, infoB):
    '''
    Purpose: draws the reset button and text
    Inputs: sp (list), board_width (float), infoB (dict)
    Returns: board (GraphWin), infoBtn (dict)
    '''
    button_width = board_width / 4
    button_height = infoB['edge'] / 2
    button_p2_x = sp[0] + board_width
    button_p2_y = sp[1] + board_width + (button_height + infoB['edge']) / 2
    button_p1_x = button_p2_x - button_width
    button_p1_y = button_p2_y - button_height
    button_p1 = gr.Point(button_p1_x, button_p1_y)
    button_p2 = gr.Point(button_p2_x, button_p2_y)
    button = gr.Rectangle(button_p1,button_p2)
    button.setFill('white')
    button_text = gr.Text(button.getCenter(), 'Restart')
    button_text.setSize(24)
    button.draw(board)
    button_text.draw(board)
    infoBtn = {'sp':button_p1,'ep':button_p2}
    return(board, infoBtn)

def drawTurn(board, sp, board_height, infoB):
    '''
    Purpose: draws the image and text indicating which player's turn it is
    Inputs: board, (GraphWin), sp (list), board_height (float), infoB (dict)
    Returns: board (GraphWin), imgTurn (Image)
    '''
    #load image to get width and height for centre point before moving to
    #final location
    imgTurn = gr.Image(gr.Point(0, 0), 'img/king1.png')
    img_x = sp[0] + imgTurn.getWidth() / 2
    img_y = sp[1] + board_height + infoB['edge'] / 2
    imgTurn.move(img_x, img_y)
    imgTurn.draw(board)
    txtTurn = gr.Text(gr.Point(img_x + 125, img_y), "Player's Turn")
    txtTurn.setSize(24)
    txtTurn.draw(board)
    return(board, imgTurn)

def setupBoard(infoB,colors):
    '''
    Purpose: initializes the graphics window, draws the board and labels,
    draws reset button and current player's turn indicator
    Inputs: infoB (dict), colors (list)
    Returns: board (GraphWin), boardDict (dict), infoBtn (dict), imgTurn (Image)
    '''
    #Pull window and board dimensions from infoB
    win_width = infoB['full']
    win_height = (infoB['full'] + infoB['board']) / 2  + infoB['edge']
    board_width = board_height = infoB['board']
    #Set the title and draw the graphics window
    title = "Neal's Chess Game"
    board = gr.GraphWin(title,win_width,win_height)
    #Initialize the starting points for the board and labels, then draws them
    sp_x = (win_width - board_width) / 2
    sp_y = sp_x
    sp = [sp_x,sp_y]
    boardDict, labelDict = setupBoardInfo(sp,board_width,board_height,colors)
    for item in boardDict:
        p1 = boardDict[item]['up']
        p2 = boardDict[item]['lp']
        square = gr.Rectangle(p1,p2)
        square.setFill(boardDict[item]['color'])
        square.draw(board)
    for label in labelDict:
        text = gr.Text(labelDict[label],label)
        text.draw(board)
    #Draw the reset button and the current player's turn text and image
    board, infoBtn = drawButton(board, sp, board_width, infoB)
    board, imgTurn = drawTurn(board, sp, board_height, infoB)
    return(board, boardDict, infoBtn, imgTurn)


def drawPiece(board, boardDict, piece):
    '''
    Purpose: draws a piece to the board
    Inputs: board (GraphWin), boardDict (dict), piece (dict)
    Returns: board (GraphWin), image (Image)
    '''
    loc = piece['cpos']
    p = boardDict[loc]['cp']
    image = gr.Image(p,piece['imgName'])
    image.draw(board)
    return(board, image)


def cell2Name(coord):
    '''
    Purpose: converts a cell coordinate to a cell name. If reset button is
    clicked, returns RB.
    Inputs: coord (list)
    Returns: cellName (str)
    '''
    columns = 'ABCDEFGH'
    if coord == [0,0]:
        cellName = "RB"
    else:
        cellName = columns[coord[0]-1]+str(coord[1])
    return(cellName)


def getCell(cp, infoB, infoBtn):
    '''
    Purpose: gets a cell coordinate (column and row number) a mouse click.  If
    the mouse click is in the rest button, returns [0,0]. If the mouse click is
    outside of the board or reset button, returns a None variable
    Inputs: cp (Point), infoB (dict), infoBtn (list)
    Returns: coord (list or None)
    '''
    #get the x and y coordinate of the mouse click
    cp_x = cp.getX()
    cp_y = cp.getY()
    #pull board and button location from the appropriate dictionary
    board_sp_x = (infoB['full'] - infoB['board'])/2
    board_sp_y = board_sp_x
    board_ep_x = board_sp_x + infoB['board']
    board_ep_y = board_sp_y + infoB['board']
    btn_sp_x = infoBtn['sp'].getX()
    btn_sp_y = infoBtn['sp'].getY()
    btn_ep_x = infoBtn['ep'].getX()
    btn_ep_y = infoBtn['ep'].getY()
    #check if click point is on the board, if so convert the click point to a
    #coordinate with column and row number between 1 and 8
    if (cp_x >= board_sp_x and cp_y >= board_sp_y) \
            and (cp_x <= board_ep_x and cp_y <= board_ep_y):
        coord_x = int((cp_x - board_sp_x) // (infoB['board']/8) + 1)
        coord_y = int((cp_y - board_sp_y) // (infoB['board'] / 8) + 1)
        coord = [coord_x, coord_y]
    #check if click point is on the reset button, if so set coord to [0,0]
    elif (cp_x >= btn_sp_x and cp_y >= btn_sp_y) \
            and (cp_x <= btn_ep_x and cp_y <= btn_ep_y):
        coord = [0, 0]
    else:
        coord = None
    return(coord)

def undrawPieces(pieces):
    '''
    Purpose: undraws all pieces (for use when reset button is clicked)
    Inputs: pieces (list)
    Returns: pieces (list)
    '''
    for player in pieces:
        for piece in player:
            if player[piece]['gObj'] != None:
                player[piece]['gObj'].undraw()
    return(pieces)


def initializeBoard(board,infoB,boardDict,pieces,imgTurn):
    '''
    Purpose: initializes the turn counter and draws the pieces to the board.
    Inputs: board (GraphWin), infoB (dict), boardDict (dict), pieces (list),
    imgTurn (img)
    Returns: board (GraphWin), infoB (dict), pieces (dict), imgTurn (img)
    '''
    p1_turn = True
    del pieces
    pieces = setupPieceInfo()
    for player in pieces:
        for piece in player:
            #player[piece]['cpos'] = player[piece]['ipos']
            board,player[piece]['gObj'] = drawPiece(board, boardDict,
                                                    player[piece])
    imgTurn.undraw()
    imgTurn = gr.Image(imgTurn.getAnchor(), 'img/king1.png')
    imgTurn.draw(board)
    return(board, pieces, p1_turn, imgTurn)


def getContents(name,pieces):
    '''
    Purpose: gets the contents of a cell (player # and piece name)
    Inputs: move (list), pieces (list)
    Returns: iplayer (bool), piece (str)
    '''
    for player in pieces:
        for unit in player:
            if name == player[unit]['cpos']:
                iplayer = pieces.index(player)
                piece = unit
                '''
                pawn_prom = ''
                if 'Pawn' in unit:
                    if 'rook' in player[unit]['imgName']:
                        pawn_prom = 'Rook'
                    if 'knight' in player[unit]['imgName']:
                        pawn_prom = 'Knight'
                    if 'bishop' in player[unit]['imgName']:
                        pawn_prom = 'Bishop'
                    if 'queen' in player[unit]['imgName']:
                        pawn_prom = 'Queen'
                '''
                return (iplayer, piece)

def cellOccupied(name,pieces,p1_turn):
    '''
    Purpose: Checks if a cell is occupied by a piece of the current player's
    Inputs: name (str), pieces (list), p1_turn (bool)
    Returns: isOccupied (bool)
    '''
    if p1_turn == True:
        for piece in pieces[0]:
            if name == pieces[0][piece]['cpos']:
                return(True)
    else:
        for piece in pieces[1]:
            if name == pieces[1][piece]['cpos']:
                return(True)
    return(False)


def promote(board,iplayer,move,pieces,piece_name,boardDict):
    #promo = []
    #window = {}
    p1_x = boardDict['B4']['up'].getX() - 25
    p1_y = boardDict['B4']['up'].getY() - 25
    p2_x = boardDict['G5']['lp'].getX() + 25
    p2_y = boardDict['G5']['lp'].getY() + 25
    #window['up'] = gr.Point(p1_x,p1_y)
    #window['lp'] = gr.Point(p2_x,p2_y)
    prom_w = gr.Rectangle(gr.Point(p1_x,p1_y),gr.Point(p2_x,p2_y))
    prom_w.setFill('white')
    #window['GrObj'] = prom_w
    #promo.append(window)
    #rook = {}
    #rook_point = boardDict['C5']
    rk_name = pieces[iplayer]['RookL']['imgName']
    kn_name = pieces[iplayer]['KnightL']['imgName']
    bp_name = pieces[iplayer]['BishopL']['imgName']
    qn_name = pieces[iplayer]['Queen']['imgName']
    rk_img = gr.Image(boardDict['C5']['cp'],rk_name)
    kn_img = gr.Image(boardDict['D5']['cp'],kn_name)
    bp_img = gr.Image(boardDict['E5']['cp'], bp_name)
    qn_img = gr.Image(boardDict['F5']['cp'], qn_name)
    text_x = (boardDict['D4']['cp'].getX() + boardDict['E4']['cp'].getX()) / 2
    text_y = boardDict['D4']['cp'].getY()
    text_p = gr.Point(text_x,text_y)
    text = gr.Text(text_p,"Choose A Promotion:")
    text.setSize(24)
    #promo_dict = {}
    prom_w.draw(board)
    rk_img.draw(board)
    kn_img.draw(board)
    bp_img.draw(board)
    qn_img.draw(board)
    text.draw(board)
    rk_img.getAnchor() - rk_img.getWidth()/2
    while True:
        try:
            click = board.getMouse()
        except:
            board.close()
            raise SystemExit
        if click.getX() > boardDict['C5']['up'].getX() and click.getX() < boardDict['C5']['lp'].getX() \
        and click.getY() > boardDict['C5']['up'].getY() and click.getY() < boardDict['C5']['lp'].getY():
            name = 'img/rook{}.png'.format(iplayer+1)
            pos = boardDict[pieces[iplayer][piece_name]['cpos']]['cp']
            image = gr.Image(pos,name)
            pieces[iplayer][piece_name]['gObj'].undraw()
            image.draw(board)
            pieces[iplayer][piece_name]['imgName'] = name
            pieces[iplayer][piece_name]['gObj'] = image
            piece_num = piece_name[4]
            new_piece_name = "Rook" + piece_num
            pieces[iplayer][new_piece_name] = pieces[iplayer][piece_name]
            del pieces[iplayer][piece_name]
            break
        elif click.getX() > boardDict['D5']['up'].getX() and click.getX() < boardDict['D5']['lp'].getX() \
        and click.getY() > boardDict['D5']['up'].getY() and click.getY() < boardDict['D5']['lp'].getY():
            name = 'img/knight{}.png'.format(iplayer+1)
            pos = boardDict[pieces[iplayer][piece_name]['cpos']]['cp']
            image = gr.Image(pos,name)
            pieces[iplayer][piece_name]['gObj'].undraw()
            image.draw(board)
            pieces[iplayer][piece_name]['imgName'] = name
            pieces[iplayer][piece_name]['gObj'] = image
            piece_num = piece_name[4]
            new_piece_name = 'Knight' + piece_num
            pieces[iplayer][new_piece_name] = pieces[iplayer][piece_name]
            del pieces[iplayer][piece_name]
            break
        elif click.getX() > boardDict['E5']['up'].getX() and click.getX() < boardDict['E5']['lp'].getX() \
        and click.getY() > boardDict['E5']['up'].getY() and click.getY() < boardDict['E5']['lp'].getY():
            name = 'img/bishop{}.png'.format(iplayer+1)
            pos = boardDict[pieces[iplayer][piece_name]['cpos']]['cp']
            image = gr.Image(pos,name)
            pieces[iplayer][piece_name]['gObj'].undraw()
            image.draw(board)
            pieces[iplayer][piece_name]['imgName'] = name
            pieces[iplayer][piece_name]['gObj'] = image
            piece_num = piece_name[4]
            new_piece_name = "Bishop" + piece_num
            pieces[iplayer][new_piece_name] = pieces[iplayer][piece_name]
            del pieces[iplayer][piece_name]
            break
        elif click.getX() > boardDict['F5']['up'].getX() and click.getX() < boardDict['F5']['lp'].getX() \
        and click.getY() > boardDict['F5']['up'].getY() and click.getY() < boardDict['F5']['lp'].getY():
            name = 'img/queen{}.png'.format(iplayer+1)
            pos = boardDict[pieces[iplayer][piece_name]['cpos']]['cp']
            image = gr.Image(pos,name)
            pieces[iplayer][piece_name]['gObj'].undraw()
            image.draw(board)
            pieces[iplayer][piece_name]['imgName'] = name
            pieces[iplayer][piece_name]['gObj'] = image
            piece_num = piece_name[4]
            new_piece_name = "Queen" + piece_num
            pieces[iplayer][new_piece_name] = pieces[iplayer][piece_name]
            del pieces[iplayer][piece_name]
            break
    rk_img.undraw()
    kn_img.undraw()
    bp_img.undraw()
    qn_img.undraw()
    text.undraw()
    prom_w.undraw()
    return(board,pieces)

def updatePiece(board,iplayer,piece_name,move,pieces,boardDict):
    '''
    Purpose: updates a piece's current position and redraws it
    Inputs: board (GraphWin), iplayer
    Returns:
    '''
    pieces[iplayer][piece_name]['gObj'].undraw()
    pieces[iplayer][piece_name]['cpos'] = move[1]
    imgName = pieces[iplayer][piece_name]['imgName']
    imgLoc = boardDict[move[1]]['cp']
    image = gr.Image(imgLoc,imgName)
    pieces[iplayer][piece_name]['gObj'] = image
    image.draw(board)
    if piece_name[0:4] == "Pawn":
        if iplayer == 0 and move[1][1] == "1":
            board, pieces = promote(board,iplayer,move,pieces,piece_name,boardDict)
        elif iplayer == 1 and move[1][1] == "8":
            board, pieces = promote(board, iplayer, move, pieces, piece_name, boardDict)
    return(board,pieces)


def updateTurnImage(imgTurn,board,p1_turn):
    '''
    Purpose:
    Inputs:
    Returns:
    '''
    img_point = imgTurn.getAnchor()
    imgTurn.undraw()
    if p1_turn:
        imgTurn = gr.Image(img_point, 'img/king1.png')
        imgTurn.draw(board)
    else:
        imgTurn = gr.Image(img_point, 'img/king2.png')
        imgTurn.draw(board)
    return(imgTurn,board)


def victoryScreen(board,p1_turn, infoB):
    if p1_turn == True:
        winner = "White"
    else:
        winner = "Black"
    w = infoB['full']
    h = infoB['full']
    box_p1 = gr.Point(w/8-10,7*h/16)
    box_p2 = gr.Point(7*w/8+10,9*h/16)
    vs_box = gr.Rectangle(box_p1,box_p2)
    vs_box.setFill('white')
    text_p = gr.Point(w/2,h/2)
    vs_text = gr.Text(text_p,"{} Player is Victorious!".format(winner))
    vs_box.draw(board)
    vs_text.setSize(24)
    vs_text.draw(board)
    return(vs_box, vs_text, board)


def removePiece(board, pieces, name, gameOver):
    '''
    Purpose: removes a piece from the board if taken by opponent
    Inputs:
    Returns:
    '''
    player, piece, = getContents(name, pieces)
    image = pieces[player][piece]['gObj']
    image.undraw()
    pieces[player][piece]['cpos'] = None
    if piece == 'King':
        gameOver = True
    return(board, pieces, gameOver)

def mainGameM3():
    '''
    Purpose: main game function.  Initializes the board dimensions, then setups
    the pieces, and sets up the board. Then checks for mouse clicks and gets
    the location on the board that is clicked.  If the reset button is clicked,
    redraws the pieces at their initial positions. Once two squares are clicked,
    and the inital click is on one of the current players pieces, checks for
    a valid move. If move is valid, moves the piece and removes an opponent's
    piece if the final position is occupied by opponent's piece.
    Inputs: none
    Returns: none
    '''
    # first pulls width of a piece image, which is used as a single square size
    # and then uses that to determine the graphics window width
    init_board_width = gr.Image(gr.Point(0, 0), 'img/king1.png')
    board_width = init_board_width.getWidth() * 8
    infoB = {'full': board_width + 50, 'board': board_width, 'edge': 100}
    colors = ['white', 'grey']
    pieces = setupPieceInfo()
    board, boardDict, infoBtn, imgTurn = setupBoard(infoB, colors)
    move = []
    p1_turn = None
    gameOver = False
    #main game loop
    while(True):
        #Get click, catch exception for clicking on the window close buton
        try:
            cp = board.getMouse()
        except:
            board.close()
            return
        #If click outside board or reset button, continue to next loop
        coord = getCell(cp,infoB,infoBtn)
        if coord == None:
            continue
        #Get cell name
        else:
            cellName = cell2Name(coord)
        #Reset board if reset button is clicked
        if cellName == 'RB':
            if gameOver:
                vs_text.undraw()
                vs_box.undraw()
            undrawPieces(pieces)
            board,pieces,p1_turn,imgTurn = initializeBoard(board,infoB,boardDict,
                                                            pieces,imgTurn)
            gameOver = False
            move = []
        else:
            #if reset button has not been pushed yet, then doesn't go further
            if p1_turn == None or gameOver == True:
                continue
            # check if initial click is on one of current player's pieces
            elif (not cellOccupied(cellName,pieces,p1_turn)) and len(move) == 0:
                continue
            else:
                move.append(cellName)
                if len(move) == 2:
                    #checks if final location interferes with own piece
                    if not cellOccupied(move[1],pieces,p1_turn):
                        iplayer, piece = getContents(move[0], pieces)
                        #check if valid move, if so update piece location
                        validMove, castle = isValidMove(piece,move[0],move[1],iplayer,pieces)
                        if validMove:
                            #remove opponent's piece if occupying final position
                            if cellOccupied(move[1], pieces, not p1_turn):
                                board,pieces,gameOver = removePiece(board,pieces,move[1],gameOver)
                            #update moved piece's location and image
                            board, pieces = updatePiece(board,iplayer,piece,move,
                                                        pieces,boardDict)
                            if castle:
                                board, pieces = updatePiece(board,iplayer,castle[0],
                                                            castle[1],pieces,boardDict)
                            if gameOver:
                                vs_box, vs_text, board = victoryScreen(board, p1_turn, infoB)
                                continue
                            #change player's turn and update the turn image
                            p1_turn = not p1_turn
                            imgTurn, board = updateTurnImage(imgTurn,board,p1_turn)
                    move = []
    board.close()

if __name__ == "__main__":
    mainGameM3()
