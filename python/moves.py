
def checkBounds(np):
    num="12345678"
    let="abcdefgh"
    if np[0] in let:
        if np[1] in num:
            return(True)
    return(False)

def checkMoved(cp,np):
    if cp[0] == np[0]:
        if cp[1] == np[1]:
            return(False)
    return(True)

def checkRookMove(cp,np,pieces):

    cols = 'abcdefgh'

    if(not checkBounds(np)):
        return False

    if(not checkMoved(cp,np)):
        return False

    if np[0] == cp[0]:
        if int(np[1]) > int(cp[1]):
            for n in range(int(cp[1])+1,int(np[1]),1):
                test_p = np[0].upper() + str(n)
                for plyr in pieces:
                    for piece in plyr:
                        if plyr[piece]['cpos'] == test_p:
                            return False
        elif int(np[1]) < int(cp[1]):
            for n in range(int(np[1])+1,int(cp[1]),1):
                test_p = np[0].upper() + str(n)
                for plyr in pieces:
                    for piece in plyr:
                        if plyr[piece]['cpos'] == test_p:
                            return False
        return True

    idx_cp = cols.index(cp[0])
    idx_np = cols.index(np[0])
    if np[1] == cp[1]:
        if idx_np > idx_cp:
            for n in range(idx_cp+1, idx_np, 1):
                test_p = cols[n].upper() + np[1]
                for plyr in pieces:
                    for piece in plyr:
                        if plyr[piece]['cpos'] == test_p:
                            return False
        elif idx_np < idx_cp:
            for n in range(idx_np+1, idx_cp, 1):
                print(n)
                test_p = cols[n].upper() + np[1]
                for plyr in pieces:
                    for piece in plyr:
                        if plyr[piece]['cpos'] == test_p:
                            return False
        return(True)
    return(False)

def checkPawnMove(cp,np,player,np_occupied):
    # Assume player 0 can only move up and player 1 can only move down
    if(not checkBounds(np)):
        return False
    if(not checkMoved(cp,np)):
        return False
    cols = 'abcdefgh'
    if player == 0:
        if ((int(cp[1])-1 == int(np[1]) and cp[0]==np[0]) or \
        (cp[1] == '7' and int(cp[1]) - 2 == int(np[1]) and cp[0] == np[0]))\
        and np_occupied == False:
            return True
        elif np_occupied == True:
            if cols.index(cp[0]) == 7:
                if (int(cp[1])-1 == int(np[1]) and cols[cols.index(cp[0])-1]==np[0]):
                    return True
            elif cols.index(cp[0]) == 0:
                if (int(cp[1])-1 == int(np[1]) and cols[cols.index(cp[0])+1]==np[0]):
                    return True
            elif ((int(cp[1])-1 == int(np[1]) and cols[cols.index(cp[0])+1]==np[0]) \
            or (int(cp[1])-1 == int(np[1]) and cols[cols.index(cp[0])-1]==np[0])):
                return True

    elif player == 1:
        if ((int(cp[1])+1 == int(np[1]) and cp[0]==np[0]) or \
        (cp[1] == '2' and int(cp[1]) + 2 == int(np[1]) and cp[0] == np[0])) \
        and np_occupied == False:
            return True
        elif np_occupied == True:
            if cols.index(cp[0]) == 7:
                if (int(cp[1]) + 1 == int(np[1]) and cols[cols.index(cp[0]) - 1] == np[0]):
                    return True
            elif cols.index(cp[0]) == 0:
                if (int(cp[1]) + 1 == int(np[1]) and cols[cols.index(cp[0]) + 1] == np[0]):
                    return True
            elif ((int(cp[1]) + 1 == int(np[1]) and cols[cols.index(cp[0]) + 1] == np[0]) \
            or (int(cp[1]) + 1 == int(np[1]) and cols[cols.index(cp[0]) - 1] == np[0])):
                return True

    return False

def checkKnightMove(cp,np):
    print(cp,np)
    if(not checkBounds(np)):
        return False
    if(not checkMoved(cp,np)):
        return False

    drow = ord(cp[0]) - ord(np[0])
    dcol = int(cp[1]) - int(np[1])
    print(drow,dcol)
    if( (abs(drow)==1 and abs(dcol)==2) or \
        (abs(drow)==2 and abs(dcol)==1) ):
        return True
    else:
        return False

def checkBishopMove(cp,np,pieces):
    if(not checkBounds(np)):
        return False
    if(not checkMoved(cp,np)):
        return False

    cols = 'abcdefgh'

    ncp=int(cp[1])
    nnp=int(np[1])
    cpos = nnp-ncp

    nclet=ord(cp[0])
    nnlet=ord(np[0])
    clet = nnlet-nclet

    if ( abs(cpos) == abs(clet) ) and (cpos !=0):
        for n in range(1,abs(cpos),1):
            if cpos > 0 and clet > 0: #np[1] > cp[1] and np[0] > cp[0]
                test_p =  cols[cols.index(cp[0])+n].upper() + str(int(cp[1])+n)
                for plyr in pieces:
                    for piece in plyr:
                        if plyr[piece]['cpos'] == test_p:
                            return False
            elif cpos > 0 and clet < 0: #np[1] > cp[1] and np[0] < cp[0]
                test_p =  cols[cols.index(cp[0])-n].upper() + str(int(cp[1])+n)
                for plyr in pieces:
                    for piece in plyr:
                        if plyr[piece]['cpos'] == test_p:
                            return False
            elif cpos < 0 and clet > 0:  # np[1] < cp[1] and np[0] > cp[0]
                test_p = cols[cols.index(cp[0])+n].upper() + str(int(cp[1])-n)
                for plyr in pieces:
                    for piece in plyr:
                        if plyr[piece]['cpos'] == test_p:
                            return False
            elif cpos < 0 and clet < 0:  # np[1] < cp[1] and np[0] < cp[0]
                test_p = cols[cols.index(cp[0])-n].upper() + str(int(cp[1])-n)
                for plyr in pieces:
                    for piece in plyr:
                        if plyr[piece]['cpos'] == test_p:
                            return False
        return(True)
    return(False)

def checkKingMove(cp,np,pieces,player):

    if(not checkBounds(np)):
        return False,0
    if(not checkMoved(cp,np)):
        return False,0

    ncp=int(cp[1])
    nnp=int(np[1])
    cpos = nnp-ncp

    nclet=ord(cp[0])
    nnlet=ord(np[0])
    clet = nnlet-nclet

    if ((abs(clet)<=1) and (abs(cpos)<=1) ):
        return(True,0)

    king_not_moved = (pieces[player]["King"]['cpos'] == pieces[player]["King"]['ipos'])
    rookL_not_moved = (pieces[player]["RookL"]['cpos'] == pieces[player]["RookL"]['ipos'])
    rookR_not_moved = (pieces[player]["RookR"]['cpos'] == pieces[player]["RookR"]['ipos'])
    if king_not_moved:
        if player == 0:
            if (ord(np[0]) - ord(cp[0]) == 2) and rookR_not_moved and checkRookMove('h8','e8',pieces):
                castle = ['RookR', ['H8','F8']]
                return True, castle
            elif (ord(cp[0]) - ord(np[0]) == 2) and rookL_not_moved and checkRookMove('a8','e8',pieces):
                castle = ['RookL', ['A8', 'D8']]
                return True, castle
        elif player == 1:
            if (ord(np[0]) - ord(cp[0]) == 2) and rookR_not_moved and checkRookMove('h1','e1',pieces):
                castle = ['RookR', ['H1', 'F1']]
                return True, castle
            elif (ord(cp[0]) - ord(np[0]) == 2) and rookL_not_moved and checkRookMove('a1','e1',pieces):
                castle = ['RookL', ['A1', 'D1']]
                return True, castle

    return(False,0)

def checkQueenMove(cp,np,pieces):
    bm = checkBishopMove(cp,np,pieces)
    rm = checkRookMove(cp,np,pieces)
    if (bm or rm):
        return(True)
    return(False)

def fixPiece(piece):
    piece = piece.lower().strip()
    if "rook" in piece:
      return("rook")
    elif "bishop" in piece:
      return("bishop")
    elif "knight" in piece:
      return("knight")
    elif "queen" in piece:
      return("queen") 
    elif "king" in piece:
      return("king") 
    elif "pawn" in piece:
      return("pawn") 
    else:
      return(None)

def isValidMove(piece,cp,np,player,pieces):
    piece = fixPiece(piece)
    cp = cp.lower()
    np = np.lower()
    print(piece, cp,np)
    if piece == "rook":
        return(checkRookMove(cp,np,pieces),0)
    elif piece == "bishop":
        return(checkBishopMove(cp,np,pieces),0)
    elif piece == "queen":
        return(checkQueenMove(cp,np,pieces),0)
    elif piece == "king":
        return(checkKingMove(cp,np,pieces,player))
    elif piece == "pawn":
        np_occupied = False
        for plyr in pieces:
            for piece in plyr:
                if np.upper() == plyr[piece]['cpos']:
                    np_occupied = True
                    break
        return(checkPawnMove(cp,np,player,np_occupied),0)
    elif piece == "knight":
        return(checkKnightMove(cp,np),0)
    else:
        return(None, 0)

#if __name__ == "__main__":
    #print(checkRookMove("a7","a1"))
    #print(isValidMove("Rook","a7","a1"))

