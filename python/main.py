import graphics as gr
from setup import setupPieceInfo
from draw import drawBoard
from gameplay import *
from moves import *

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


def chessGame():
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
    init_board_width = gr.Image(gr.Point(0, 0), '../img/king1.png')
    board_width = init_board_width.getWidth() * 8
    infoB = {'full': board_width + 50, 'board': board_width, 'edge': 100}
    colors = ['white', 'grey']
    pieces = setupPieceInfo()
    board, boardDict, infoBtn, imgTurn = drawBoard(infoB, colors)
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
            board,pieces,p1_turn,imgTurn = initializeBoard(board, boardDict,
                                                           pieces, imgTurn)
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
    chessGame()
