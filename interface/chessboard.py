from constants import *

def initChessboard(position):
    board = [[EMPTY for _ in range(8)] for _ in range(8)]
    if position == POSITION_DEFAULT:
        for i in range(8):
            board[1][i] = PAWN_W
            board[6][i] = PAWN_B
        for i in [0, 7]:
            board[0][i] = ROOK_W
            board[7][i] = ROOK_B
        for i in [1, 6]:
            board[0][i] = KNIGHT_W
            board[7][i] = KNIGHT_B
        for i in [2, 5]:
            board[0][i] = BISHOP_W
            board[7][i] = BISHOP_B
        board[0][3] = QUEEN_W
        board[0][4] = KING_W
        board[7][3] = QUEEN_B
        board[7][4] = KING_B

    return board

def moveToString(piece, move, takes, promotion, specialPosition, castling):
    if castling:
        if move[1][1] == 5:
            string = '0-0'
        else:
            string = '0-0-0'
    else:
        string = ''
        field = move[1]
        if abs(piece) == PAWN:
            if takes:
                string += chr(move[0][1]+ord('a')) + 'x'
            if promotion:
                string += chr(field[1]+ord('a')) + '8' + PIECE_NAMES[promotion]
        else:
            string += PIECE_NAMES[abs(piece)]
            if takes:
                string += 'x'
        if not promotion:
            string += chr(field[1]+ord('a')) + str(field[0]+1)
    if specialPosition == MATE:
        string += '#'
    elif specialPosition == CHECK:
        string += '+'
    return string


class Chessboard:
    def __init__(self, position=POSITION_DEFAULT, debug=False):
        self.debug = debug
        self.board = initChessboard(position)
        self.history = { WHITE: [], BLACK: [] }
        self.onMove = WHITE
        self.check = False
        self.enPassant = [False]
        self.whiteKingHasNotMoved = True
        self.whiteLRookHasNotMoved = True
        self.whiteRRookHasNotMoved = True
        self.blackKingHasNotMoved = True
        self.blackLRookHasNotMoved = True
        self.blackRRookHasNotMoved = True
        self.whiteIsCastling = False
        self.blackIsCastling = False
        self.attackedFields = [] # assume that if first move is with king, it is valid. also must not already be mate or stalemate
        self.setPossibleMoves()

    def __str__(self):
        string = '\n'
        for i in range(7, -1, -1):
            for j in range(8):
                if self.board[i][j] >= 0:
                    string += ' '
                string += ' ' + str(self.board[i][j])
            string += '\n'
        return string

    # TODO
    def changeClock(self, specialPosition):
        pass

    def getMovesWithPiece(self, field):
        moves = []
        piece = self.board[field[0]][field[1]]

        if self.onMove == WHITE:
            if piece == PAWN:
                if self.board[field[0]+1][field[1]] == 0:
                    moves.append([field[0]+1, field[1]])
                    if field[0] == 1 and self.board[field[0]+2][field[1]] == 0:
                        moves.append([field[0]+2, field[1]])
                if field[1] < 7 and self.board[field[0]+1][field[1]+1] < 0:
                    moves.append([field[0]+1, field[1]+1])
                if field[1] > 0 and self.board[field[0]+1][field[1]-1] < 0:
                    moves.append([field[0]+1, field[1]-1])
                if self.enPassant[0] and self.enPassant[1][0] == field:
                    moves.append([self.enPassant[1][1]])
                return moves

            elif piece == KNIGHT:
                potentialMoves = [
                    [field[0]-1, field[1]-2],
                    [field[0]+1, field[1]-2],
                    [field[0]-2, field[1]-1],
                    [field[0]-2, field[1]+1],
                    [field[0]-1, field[1]+2],
                    [field[0]+1, field[1]+2],
                    [field[0]+2, field[1]-1],
                    [field[0]+2, field[1]+1]
                ]
                for move in potentialMoves:
                    if move[0] >= 0 and move[0] < 8 and move[1] >= 0 and move[1] < 8:
                        if self.board[move[0]][move[1]] <= 0:
                            moves.append(move)
                return moves

            elif piece == KING:
                if field[0] > 0:
                    if self.board[field[0]-1][field[1]] <= 0 and [field[0]-1, field[1]] not in self.attackedFields:
                        moves.append([field[0]-1, field[1]])
                    if field[1] > 0 and self.board[field[0]-1][field[1]-1] <= 0 and [field[0]-1, field[1]-1] not in self.attackedFields:
                        moves.append([field[0]-1, field[1]-1])
                    if field[1] < 7 and self.board[field[0]-1][field[1]+1] <= 0 and [field[0]-1, field[1]+1] not in self.attackedFields:
                        moves.append([field[0]-1, field[1]+1])
                if field[0] < 7:
                    if self.board[field[0]+1][field[1]] <= 0 and [field[0]+1, field[1]] not in self.attackedFields:
                        moves.append([field[0]+1, field[1]])
                    if field[1] > 0 and self.board[field[0]+1][field[1]-1] <= 0 and [field[0]+1, field[1]-1] not in self.attackedFields:
                        moves.append([field[0]+1, field[1]-1])
                    if field[1] < 7 and self.board[field[0]+1][field[0]+1] <= 0 and [field[0]+1, field[1]+1] not in self.attackedFields:
                        moves.append([field[0]+1, field[0]+1])
                if field[1] > 0 and self.board[field[0]][field[1]-1] <= 0 and [field[0], field[1]-1] not in self.attackedFields:
                    moves.append([field[0], field[1]-1])
                if field[1] < 7 and self.board[field[0]][field[1]+1] <= 0 and [field[0], field[1]+1] not in self.attackedFields:
                    moves.append([field[0], field[1]+1])
                # castling
                if self.whiteKingHasNotMoved and self.whiteRRookHasNotMoved and self.board[0][5] == 0 and self.board[0][6] == 0 and not self.check and \
                    [0, 6] not in self.attackedFields and [0, 5] not in self.attackedFields:
                    moves.append([0, 6])
                if self.whiteKingHasNotMoved and self.whiteLRookHasNotMoved and self.board[0][3] == 0 and self.board[0][2] == 0 and self.board[0][1] == 0 \
                    and not self.check and [0, 2] not in self.attackedFields and [0, 3] not in self.attackedFields:
                    moves.append([0, 2])
                return moves

            if piece == ROOK or piece == QUEEN:
                # up
                for i in range(1, 8-field[0]):
                    if self.board[field[0]+i][field[1]] == 0:
                        moves.append([field[0]+i, field[1]])
                    elif self.board[field[0]+i][field[1]] < 0:
                        moves.append([field[0]+i, field[1]])
                        break
                    else: # white piece blocking path
                        break
                # down
                for i in range(1, field[0]+1):
                    if self.board[field[0]-i][field[1]] == 0:
                        moves.append([field[0]-i, field[1]])
                    elif self.board[field[0]-i][field[1]] < 0:
                        moves.append([field[0]-i, field[1]])
                        break
                    else: # white piece blocking path
                        break
                # left
                for i in range(1, field[1]+1):
                    if self.board[field[0]][field[1]-i] == 0:
                        moves.append([field[0], field[1]-i])
                    elif self.board[field[0]][field[1]-i] < 0:
                        moves.append([field[0], field[1]-i])
                        break
                    else: # white piece blocking path
                        break
                # right
                for i in range(1, 8-field[1]):
                    if self.board[field[0]][field[1]+i] == 0:
                        moves.append([field[0], field[1]+i])
                    elif self.board[field[0]][field[1]+i] < 0:
                        moves.append([field[0], field[1]+i])
                        break
                    else: # white piece blocking path
                        break

            if piece == BISHOP or piece == QUEEN:
                # left down
                for i in range(1, min(field[0]+1, field[1]+1)):
                    if self.board[field[0]-i][field[1]-i] == 0:
                        moves.append([field[0]-i, field[1]-i])
                    elif self.board[field[0]-i][field[1]-i] < 0:
                        moves.append([field[0]-i, field[1]-i])
                        break
                    else: # white piece blocking path
                        break
                # left up
                for i in range(1, min(8-field[0], field[1]+1)):
                    if self.board[field[0]+i][field[1]-i] == 0:
                        moves.append([field[0]+i, field[1]-i])
                    elif self.board[field[0]+i][field[1]-i] < 0:
                        moves.append([field[0]+i, field[1]-i])
                        break
                    else: # white piece blocking path
                        break
                # right down
                for i in range(1, min(field[0]+1, 8-field[1])):
                    if self.board[field[0]-i][field[1]+i] == 0:
                        moves.append([field[0]-i, field[1]+i])
                    elif self.board[field[0]-i][field[1]+i] < 0:
                        moves.append([field[0]-i, field[1]+i])
                        break
                    else: # white piece blocking path
                        break
                # right up
                for i in range(1, min(8-field[0], 8-field[1])):
                    if self.board[field[0]+i][field[1]+i] == 0:
                        moves.append([field[0]+i, field[1]+i])
                    elif self.board[field[0]+i][field[1]+i] < 0:
                        moves.append([field[0]+i, field[1]+i])
                        break
                    else: # white piece blocking path
                        break

        else: # self.onMove = BLACK
            if piece == PAWN_B:
                if self.board[field[0]-1][field[1]] == 0:
                    moves.append([field[0]-1, field[1]])
                    if field[0] == 6 and self.board[field[0]-2][field[1]] == 0:
                        moves.append([field[0]-2, field[1]])
                if field[1] < 7 and self.board[field[0]-1][field[1]+1] > 0:
                    moves.append([field[0]-1, field[1]+1])
                if field[1] > 0 and self.board[field[0]-1][field[1]-1] > 0:
                    moves.append([field[0]-1, field[1]-1])
                if self.enPassant[0] and self.enPassant[1][0] == field:
                    moves.append([self.enPassant[1][1]])
                return moves

            elif piece == KNIGHT_B:
                potentialMoves = [
                    [field[0]-1, field[1]-2],
                    [field[0]+1, field[1]-2],
                    [field[0]-2, field[1]-1],
                    [field[0]-2, field[1]+1],
                    [field[0]-1, field[1]+2],
                    [field[0]+1, field[1]+2],
                    [field[0]+2, field[1]-1],
                    [field[0]+2, field[1]+1]
                ]
                for move in potentialMoves:
                    if move[0] >= 0 and move[0] < 8 and move[1] >= 0 and move[1] < 8:
                        if self.board[move[0]][move[1]] >= 0:
                            moves.append(move)
                return moves

            elif piece == KING_B:
                if field[0] > 0:
                    if self.board[field[0]-1][field[1]] >= 0 and [field[0]-1, field[1]] not in self.attackedFields:
                        moves.append([field[0]-1, field[1]])
                    if field[1] > 0 and self.board[field[0]-1][field[1]-1] >= 0 and [field[0]-1, field[1]-1] not in self.attackedFields:
                        moves.append([field[0]-1, field[1]-1])
                    if field[1] < 7 and self.board[field[0]-1][field[1]+1] >= 0 and [field[0]-1, field[1]+1] not in self.attackedFields:
                        moves.append([field[0]-1, field[1]+1])
                if field[0] < 7:
                    if self.board[field[0]+1][field[1]] >= 0 and [field[0]+1, field[1]] not in self.attackedFields:
                        moves.append([field[0]+1, field[1]])
                    if field[1] > 0 and self.board[field[0]+1][field[1]-1] >= 0 and [field[0]+1, field[1]-1] not in self.attackedFields:
                        moves.append([field[0]+1, field[1]-1])
                    if field[1] < 7 and self.board[field[0]+1][field[0]+1] >= 0 and [field[0]+1, field[1]+1] not in self.attackedFields:
                        moves.append([field[0]+1, field[0]+1])
                if field[1] > 0 and self.board[field[0]][field[1]-1] >= 0 and [field[0], field[1]-1] not in self.attackedFields:
                    moves.append([field[0], field[1]-1])
                if field[1] < 7 and self.board[field[0]][field[1]+1] >= 0 and [field[0], field[1]+1] not in self.attackedFields:
                    moves.append([field[0], field[1]+1])
                # castling
                if self.blackKingHasNotMoved and self.blackRRookHasNotMoved and self.board[7][5] == 0 and self.board[7][6] == 0 and not self.check and \
                    [7, 6] not in self.attackedFields and [7, 5] not in self.attackedFields:
                    moves.append([7, 6])
                if self.blackKingHasNotMoved and self.blackLRookHasNotMoved and self.board[7][3] == 0 and self.board[7][2] == 0 and self.board[7][1] == 0 \
                    and not self.check and [7, 2] not in self.attackedFields and [7, 3] not in self.attackedFields:
                    moves.append([7, 2])
                return moves

            if piece == ROOK_B or piece == QUEEN_B:
                # up
                for i in range(1, 8-field[0]):
                    if self.board[field[0]+i][field[1]] == 0:
                        moves.append([field[0]+i, field[1]])
                    elif self.board[field[0]+i][field[1]] > 0:
                        moves.append([field[0]+i, field[1]])
                        break
                    else: # white piece blocking path
                        break
                # down
                for i in range(1, field[0]+1):
                    if self.board[field[0]-i][field[1]] == 0:
                        moves.append([field[0]-i, field[1]])
                    elif self.board[field[0]-i][field[1]] > 0:
                        moves.append([field[0]-i, field[1]])
                        break
                    else: # white piece blocking path
                        break
                # left
                for i in range(1, field[1]+1):
                    if self.board[field[0]][field[1]-i] == 0:
                        moves.append([field[0], field[1]-i])
                    elif self.board[field[0]][field[1]-i] > 0:
                        moves.append([field[0], field[1]-i])
                        break
                    else: # white piece blocking path
                        break
                # right
                for i in range(1, 8-field[1]):
                    if self.board[field[0]][field[1]+i] == 0:
                        moves.append([field[0], field[1]+i])
                    elif self.board[field[0]][field[1]+i] > 0:
                        moves.append([field[0], field[1]+i])
                        break
                    else: # white piece blocking path
                        break

            if piece == BISHOP_B or piece == QUEEN_B:
                # left down
                for i in range(1, min(field[0]+1, field[1]+1)):
                    if self.board[field[0]-i][field[1]-i] == 0:
                        moves.append([field[0]-i, field[1]-i])
                    elif self.board[field[0]-i][field[1]-i] > 0:
                        moves.append([field[0]-i, field[1]-i])
                        break
                    else: # white piece blocking path
                        break
                # left up
                for i in range(1, min(8-field[0], field[1]+1)):
                    if self.board[field[0]+i][field[1]-i] == 0:
                        moves.append([field[0]+i, field[1]-i])
                    elif self.board[field[0]+i][field[1]-i] > 0:
                        moves.append([field[0]+i, field[1]-i])
                        break
                    else: # white piece blocking path
                        break
                # right down
                for i in range(1, min(field[0]+1, 8-field[1])):
                    if self.board[field[0]-i][field[1]+i] == 0:
                        moves.append([field[0]-i, field[1]+i])
                    elif self.board[field[0]-i][field[1]+i] > 0:
                        moves.append([field[0]-i, field[1]+i])
                        break
                    else: # white piece blocking path
                        break
                # right up
                for i in range(1, min(8-field[0], 8-field[1])):
                    if self.board[field[0]+i][field[1]+i] == 0:
                        moves.append([field[0]+i, field[1]+i])
                    elif self.board[field[0]+i][field[1]+i] > 0:
                        moves.append([field[0]+i, field[1]+i])
                        break
                    else: # white piece blocking path
                        break

        return moves

    # get all possible moves, even those that leave king in check
    def setPossibleMoves(self):
        possibleMoves = []
        for i in range(8):
            for j in range(8):
                if (self.onMove == WHITE and self.board[i][j] > 0) or \
                        (self.onMove == BLACK and self.board[i][j] < 0):
                    movesWithPiece = self.getMovesWithPiece([i, j])
                    for move in movesWithPiece:
                        possibleMoves.append([[i, j], move])

        self.possibleMoves = [possibleMoves[i] for i in range(len(possibleMoves)) if not self.isCheckAfterMove(possibleMoves[i])]
        print self.possibleMoves
        #self.possibleMoves = possibleMoves
        if self.debug:
            print 'self.possibleMoves = {}\n'.format(self.possibleMoves)

    def isCheck(self):
        if self.onMove == WHITE:
            self.check = KING_W in [self.board[af[0]][af[1]] for af in self.attackedFields]
        else:
            self.check = KING_B in [self.board[af[0]][af[1]] for af in self.attackedFields]

    def isSpecialPosition(self):
        self.isCheck()
        self.setPossibleMoves()
        if self.check:
            if self.possibleMoves == []:
                return MATE
            return CHECK
        if self.possibleMoves == []:
            return STALEMATE
        return False

    def canBeTakenEnPassant(self, move):
        enPassantPossible = False
        if abs(move[0][0] - move[1][0]) == 2:
            if self.onMove == WHITE:
                if move[1][1] < 7 and self.board[move[1][0]][move[1][1]+1] == PAWN_B:
                    enPassantPossible = True
                    enPassantFrom = [move[1][0], move[1][1]+1]
                if move[1][1] > 0 and self.board[move[1][0]][move[1][1]-1] == PAWN_B:
                    enPassantPossible = True
                    enPassantFrom = [move[1][0], move[1][1]-1]
                enPassantTo = [move[1][0]-1, move[1][1]]
            else:
                if move[1][1] < 7 and self.board[move[1][0]][move[1][1]+1] == PAWN_W:
                    enPassantPossible = True
                    enPassantFrom = [move[1][0], move[1][1]+1]
                if move[1][1] > 0 and self.board[move[1][0]][move[1][1]-1] == PAWN_W:
                    enPassantPossible = True
                    enPassantFrom = [move[1][0], move[1][1]-1]
                enPassantTo = [move[1][0]+1, move[1][1]]

        if enPassantPossible:
            if self.debug:
                print "EN_PASSANT POSSIBLE!"
            self.enPassant = [True, [enPassantFrom, enPassantTo]]
        else:
            self.enPassant = [False]

    def addAttackedFieldsByPawns(self):
        if self.onMove == WHITE:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == PAWN_W:
                        if j < 7 and self.board[i+1][j+1] <= 0:
                            self.attackedFields.append([i+1, j+1])
                        if j > 0 and self.board[i+1][j-1] <= 0:
                            self.attackedFields.append([i+1, j-1])
        else:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == PAWN_B:
                        if j < 7 and self.board[i-1][j+1] >= 0:
                            self.attackedFields.append([i-1, j+1])
                        if j > 0 and self.board[i-1][j-1] >= 0:
                            self.attackedFields.append([i-1, j-1])

    def isCheckAfterMove(self, move):
        originalMove = move
        pieceMoving = self.board[move[0][0]][move[0][1]]
        pieceOnArrival = self.board[move[1][0]][move[1][1]]
        self.board[originalMove[0][0]][originalMove[0][1]] = EMPTY
        self.board[originalMove[1][0]][originalMove[1][1]] = pieceMoving

        # local possible moves method
        if self.onMove == WHITE:
            self.onMove = BLACK
        else:
            self.onMove = WHITE
        possibleMoves = []
        for i in range(8):
            for j in range(8):
                if (self.onMove == WHITE and self.board[i][j] > 0) or \
                        (self.onMove == BLACK and self.board[i][j] < 0):
                    movesWithPiece = self.getMovesWithPiece([i, j])
                    for move in movesWithPiece:
                        possibleMoves.append([[i, j], move])

        # local attackedFields instance
        attackedFields = [possibleMoves[i][1] for i in range(len(possibleMoves)) \
            if abs(self.board[possibleMoves[i][0][0]][possibleMoves[i][0][1]]) != PAWN ]

        # local addAttackedFieldsByPawns method and isCheck
        if self.onMove == WHITE:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == PAWN_W:
                        if j < 7 and self.board[i+1][j+1] <= 0:
                            attackedFields.append([i+1, j+1])
                        if j > 0 and self.board[i+1][j-1] <= 0:
                            attackedFields.append([i+1, j-1])
            check = KING_B in [self.board[af[0]][af[1]] for af in attackedFields]
        else:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == PAWN_B:
                        if j < 7 and self.board[i-1][j+1] >= 0:
                            attackedFields.append([i-1, j+1])
                        if j > 0 and self.board[i-1][j-1] >= 0:
                            attackedFields.append([i-1, j-1])
            check = KING_W in [self.board[af[0]][af[1]] for af in attackedFields]

        self.board[originalMove[0][0]][originalMove[0][1]] = pieceMoving
        self.board[originalMove[1][0]][originalMove[1][1]] = pieceOnArrival

        if self.onMove == WHITE:
            self.onMove = BLACK
        else:
            self.onMove = WHITE

        return check

    def makeMove(self, move, promotion=False):
        if self.debug:
            print 'self.possibleMoves before move = {}\n'.format(self.possibleMoves)
        if move not in self.possibleMoves and not self.whiteIsCastling and not self.blackIsCastling:
            return MOVE_INVALID

        # move from move[0] to move[1]; move = [[from y, from x], [to y], [to x]]
        piece = self.board[move[0][0]][move[0][1]]
        takes = False
        if self.board[move[1][0]][move[1][1]] != 0:
            takes = True
        self.board[move[0][0]][move[0][1]] = EMPTY
        self.board[move[1][0]][move[1][1]] = piece

        # castling. if white has moved his king for two places (valid move), then
        # he is still on turn and must move the right rook. we prevent the other player
        # from coming onMove by setting the only possible move to the move with rook
        # and stopping the method. when player will move the rook to complete castling,
        # the method will procede and calculate the necessary things.
        whiteCanCastle = self.whiteKingHasNotMoved and (self.whiteLRookHasNotMoved or self.whiteRRookHasNotMoved)
        blackCanCastle = self.blackKingHasNotMoved and (self.blackLRookHasNotMoved or self.blackRRookHasNotMoved)
        if abs(piece) == KING and (whiteCanCastle or blackCanCastle):
            if move[0] == [0, 4]:
                if move[1] == [0, 6]:
                    self.possibleMoves = [[[0, 7], [0, 5]]]
                    self.whiteIsCastling = True
                    return
                elif move[1] == [0, 2]:
                    self.possibleMoves = [[[0, 0], [0, 3]]]
                    self.whiteIsCastling = True
                    return
            elif move[0] == [7, 4]:
                if move[1] == [7, 6]:
                    self.possibleMoves = [[[7, 7], [7, 5]]]
                    self.blackIsCastling = True
                    return
                elif move[1] == [7, 2]:
                    self.possibleMoves = [[[7, 0], [7, 3]]]
                    self.blackIsCastling = True
                    return

        # remember if kings and rooks have moved for castling potential
        if piece == KING_W:
            self.whiteKingHasNotMoved = False
        elif piece == ROOK_W:
            if move[0] == [0, 0]:
                self.whiteLRookHasNotMoved = False
            elif move[0] == [0, 7]:
                self.whiteRRookHasNotMoved = False
        elif piece == KING_B:
            self.blackKingHasNotMoved = False
        elif piece == ROOK_B:
            if move[0] == [7, 0]:
                self.blackLRookHasNotMoved = False
            elif move[0] == [7, 7]:
                self.blackRRookHasNotMoved = False

        # check for potential en-passant move
        if abs(piece) == PAWN:
            self.canBeTakenEnPassant(move)

        if self.debug:
            print self
            print "\n=====================================================\n"

        self.setPossibleMoves()
        self.attackedFields = [self.possibleMoves[i][1] for i in range(len(self.possibleMoves)) \
            if abs(self.board[self.possibleMoves[i][0][0]][self.possibleMoves[i][0][1]]) != PAWN ]
        # add fields that are attacked by pawns BUT ARE EMPTY! this way we prevent duplication of attackedFields
        # field, which is already an issue. But duplication is still better than checking each time if attacked
        # field is already in self.attackedFields
        self.addAttackedFieldsByPawns()

        if self.debug:
            print 'self.attackedFields = {}\n'.format(self.attackedFields)

        if self.onMove == WHITE:
            self.onMove = BLACK
        else:
            self.onMove = WHITE

        # figure out if in special position
        specialPosition = self.isSpecialPosition()
        self.changeClock(specialPosition)

        # write move to history
        if piece > 0:
            self.history[WHITE].append(moveToString(piece, move, takes, promotion, specialPosition, self.whiteIsCastling))
        else:
            self.history[BLACK].append(moveToString(piece, move, takes, promotion, specialPosition, self.blackIsCastling))

        if self.whiteIsCastling:
            self.whiteKingHasNotMoved = False
            self.whiteIsCastling = False
        elif self.blackIsCastling:
            self.blackKingHasNotMoved = False
            self.blackIsCastling = False

        return specialPosition
