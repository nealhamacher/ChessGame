import graphics as gr
from setup import setupBoard

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
    imgTurn = gr.Image(gr.Point(0, 0), '../img/king1.png')
    img_x = sp[0] + imgTurn.getWidth() / 2
    img_y = sp[1] + board_height + infoB['edge'] / 2
    imgTurn.move(img_x, img_y)
    imgTurn.draw(board)
    txtTurn = gr.Text(gr.Point(img_x + 125, img_y), "Player's Turn")
    txtTurn.setSize(24)
    txtTurn.draw(board)
    return(board, imgTurn)

def drawBoard(infoB,colors):
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
    boardDict, labelDict = setupBoard(sp,board_width,board_height,colors)
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
