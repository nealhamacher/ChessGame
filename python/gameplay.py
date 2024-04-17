import graphics as gr
from setup import setupPieceInfo
from draw import drawPiece

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


def initializeBoard(board,boardDict,pieces,imgTurn):
    '''
    Purpose: initializes the turn counter and draws the pieces to the board.
    Inputs: board (GraphWin), boardDict (dict), pieces (list),
    imgTurn (img)
    Returns: board (GraphWin), pieces (dict), imgTurn (img)
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
    imgTurn = gr.Image(imgTurn.getAnchor(), '../img/king1.png')
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
    p1_x = boardDict['B4']['up'].getX() - 25
    p1_y = boardDict['B4']['up'].getY() - 25
    p2_x = boardDict['G5']['lp'].getX() + 25
    p2_y = boardDict['G5']['lp'].getY() + 25
    prom_w = gr.Rectangle(gr.Point(p1_x,p1_y),gr.Point(p2_x,p2_y))
    prom_w.setFill('white')
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
            name = '../img/rook{}.png'.format(iplayer+1)
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
            name = '../img/knight{}.png'.format(iplayer+1)
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
            name = '../img/bishop{}.png'.format(iplayer+1)
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
            name = '../img/queen{}.png'.format(iplayer+1)
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
        imgTurn = gr.Image(img_point, '../img/king1.png')
        imgTurn.draw(board)
    else:
        imgTurn = gr.Image(img_point, '../img/king2.png')
        imgTurn.draw(board)
    return(imgTurn,board)


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