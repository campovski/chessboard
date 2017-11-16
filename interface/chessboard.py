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

def moveToString(figure, move, takes, promotion, specialPosition):
    string = ''
    field = move[1]
    if abs(figure) == PAWN:
        if takes:
            string += chr(move[0][1]+ord('a')) + 'x'
        if promotion:
            string += chr(field[1]+ord('a')) + '8' + FIGURE_NAMES[promotion]
    else:
        string += FIGURE_NAMES[abs(figure)]
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
    def __init__(self, position=POSITION_DEFAULT):
        self.board = initChessboard(position)
        self.history = { WHITE: [], BLACK: [] }
        self.onMove = WHITE
        self.check = False
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

    def getMovesWithFigure(self, field):
        moves = []
        figure = self.board[field[0]][field[1]]

        if self.onMove == WHITE:
            if figure == PAWN:
                if self.board[field[0]+1][field[1]] == 0:
                    moves.append([field[0]+1, field[1]])
                    if field[0] == 1 and self.board[field[0]+2][field[1]] == 0:
                        moves.append([field[0]+2, field[1]])
                if field[1] < 7 and self.board[field[0]+1][field[1]+1] < 0:
                    moves.append([field[0]+1, field[1]+1])
                if field[1] > 0 and self.board[field[0]+1][field[1]-1] < 0:
                    moves.append([field[0]+1, field[1]-1])
                # TODO add EN_PASSANT support
                return moves

            elif figure == KNIGHT:
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

            elif figure == KING:
                if field[0] > 0:
                    if self.board[field[0]-1][field[1]] <= 0 and [field[0]-1, field[1]] not in self.attackedFields:
                        moves.append([field[0]-1, field[1]])
                    if field[1] > 0 and self.board[field[0]-1][field[1]-1] <= 0 and [field[0]-1, field[1]-1] not in self.attackedFields:
                        moves.append([field[0]-1, field[1]-1])
                    if field[1] < 7 and self.board[field[0]-1][field[1]+1] <= 0 and [field[0]-1, field[1]+1] not in self.attackedFields:
                        moves.append([field[0]-1, field[1]+1])
                if field[0] < 7:
                    if self.board[field[0]+1][field[1]] < 0 and [field[0]+1, field[1]] not in self.attackedFields:
                        moves.append([field[0]+1, field[1]])
                    if field[1] > 0 and self.board[field[0]+1][field[1]-1] <= 0 and [field[0]+1, field[1]-1] not in self.attackedFields:
                        moves.append([field[0]+1, field[1]-1])
                    if field[1] < 7 and self.board[field[0]+1][field[0]+1] <= 0 and [field[0]+1, field[1]+1] not in self.attackedFields:
                        moves.append([field[0]+1, field[0]+1])
                if field[1] > 0 and self.board[field[0]][field[1]-1] <= 0 and [field[0], field[1]-1] not in self.attackedFields:
                    moves.append([field[0], field[1]-1])
                if field[1] < 7 and self.board[field[0]][field[1]+1] <= 0 and [field[0], field[1]+1] not in self.attackedFields:
                    moves.append([field[0], field[1]+1])
                return moves

            if figure == ROOK or figure == QUEEN:
                # up
                for i in range(1, 8-field[0]):
                    if self.board[field[0]+i][field[1]] == 0:
                        moves.append([field[0]+i, field[1]])
                    elif self.board[field[0]+i][field[1]] < 0:
                        moves.append([field[0]+i, field[1]])
                        break
                    else: # white figure blocking path
                        break
                # down
                for i in range(1, field[0]+1):
                    if self.board[field[0]-i][field[1]] == 0:
                        moves.append([field[0]-i, field[1]])
                    elif self.board[field[0]-i][field[1]] < 0:
                        moves.append([field[0]-i, field[1]])
                        break
                    else: # white figure blocking path
                        break
                # left
                for i in range(1, field[1]+1):
                    if self.board[field[0]][field[1]-i] == 0:
                        moves.append([field[0], field[1]-i])
                    elif self.board[field[0]][field[1]-i] < 0:
                        moves.append([field[0], field[1]-i])
                        break
                    else: # white figure blocking path
                        break
                # right
                for i in range(1, 8-field[1]):
                    if self.board[field[0]][field[1]+i] == 0:
                        moves.append([field[0], field[1]+i])
                    elif self.board[field[0]][field[1]+i] < 0:
                        moves.append([field[0], field[1]+i])
                        break
                    else: # white figure blocking path
                        break

            if figure == BISHOP or figure == QUEEN:
                # left down
                for i in range(1, min(field[0]+1, field[1]+1)):
                    if self.board[field[0]-i][field[1]-i] == 0:
                        moves.append([field[0]-i, field[1]-i])
                    elif self.board[field[0]-i][field[1]-i] < 0:
                        moves.append([field[0]-i, field[1]-i])
                        break
                    else: # white figure blocking path
                        break
                # left up
                for i in range(1, min(8-field[0], field[1]+1)):
                    if self.board[field[0]+i][field[1]-i] == 0:
                        moves.append([field[0]+i, field[1]-i])
                    elif self.board[field[0]+i][field[1]-i] < 0:
                        moves.append([field[0]+i, field[1]-i])
                        break
                    else: # white figure blocking path
                        break
                # right down
                for i in range(1, min(field[0]+1, 8-field[1])):
                    if self.board[field[0]-i][field[1]+i] == 0:
                        moves.append([field[0]-i, field[1]+i])
                    elif self.board[field[0]-i][field[1]+i] < 0:
                        moves.append([field[0]-i, field[1]+i])
                        break
                    else: # white figure blocking path
                        break
                # right up
                for i in range(1, min(8-field[0], 8-field[1])):
                    if self.board[field[0]+i][field[1]+i] == 0:
                        moves.append([field[0]+i, field[1]+i])
                    elif self.board[field[0]+i][field[1]+i] < 0:
                        moves.append([field[0]+i, field[1]+i])
                        break
                    else: # white figure blocking path
                        break

        else: # self.onMove = BLACK
            if figure == PAWN_B:
                if self.board[field[0]-1][field[1]] == 0:
                    moves.append([field[0]-1, field[1]])
                    if field[0] == 6 and self.board[field[0]-2][field[1]] == 0:
                        moves.append([field[0]-2, field[1]])
                if field[1] < 7 and self.board[field[0]-1][field[1]+1] > 0:
                    moves.append([field[0]-1, field[1]+1])
                if field[1] > 0 and self.board[field[0]-1][field[1]-1] > 0:
                    moves.append([field[0]-1, field[1]-1])
                # TODO add EN_PASSANT support
                return moves

            elif figure == KNIGHT_B:
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

            elif figure == KING_B:
                if field[0] > 0:
                    if self.board[field[0]-1][field[1]] >= 0 and [field[0]-1, field[1]] not in self.attackedFields:
                        moves.append([field[0]-1, field[1]])
                    if field[1] > 0 and self.board[field[0]-1][field[1]-1] >= 0 and [field[0]-1, field[1]-1] not in self.attackedFields:
                        moves.append([field[0]-1, field[1]-1])
                    if field[1] < 7 and self.board[field[0]-1][field[1]+1] >= 0 and [field[0]-1, field[1]+1] not in self.attackedFields:
                        moves.append([field[0]-1, field[1]+1])
                if field[0] < 7:
                    if self.board[field[0]+1][field[1]] < 0 and [field[0]+1, field[1]] not in self.attackedFields:
                        moves.append([field[0]+1, field[1]])
                    if field[1] > 0 and self.board[field[0]+1][field[1]-1] >= 0 and [field[0]+1, field[1]-1] not in self.attackedFields:
                        moves.append([field[0]+1, field[1]-1])
                    if field[1] < 7 and self.board[field[0]+1][field[0]+1] >= 0 and [field[0]+1, field[1]+1] not in self.attackedFields:
                        moves.append([field[0]+1, field[0]+1])
                if field[1] > 0 and self.board[field[0]][field[1]-1] >= 0 and [field[0], field[1]-1] not in self.attackedFields:
                    moves.append([field[0], field[1]-1])
                if field[1] < 7 and self.board[field[0]][field[1]+1] >= 0 and [field[0], field[1]+1] not in self.attackedFields:
                    moves.append([field[0], field[1]+1])
                return moves

            if figure == ROOK_B or figure == QUEEN_B:
                # up
                for i in range(1, 8-field[0]):
                    if self.board[field[0]+i][field[1]] == 0:
                        moves.append([field[0]+i, field[1]])
                    elif self.board[field[0]+i][field[1]] > 0:
                        moves.append([field[0]+i, field[1]])
                        break
                    else: # white figure blocking path
                        break
                # down
                for i in range(1, field[0]+1):
                    if self.board[field[0]-i][field[1]] == 0:
                        moves.append([field[0]-i, field[1]])
                    elif self.board[field[0]-i][field[1]] > 0:
                        moves.append([field[0]-i, field[1]])
                        break
                    else: # white figure blocking path
                        break
                # left
                for i in range(1, field[1]+1):
                    if self.board[field[0]][field[1]-i] == 0:
                        moves.append([field[0], field[1]-i])
                    elif self.board[field[0]][field[1]-i] > 0:
                        moves.append([field[0], field[1]-i])
                        break
                    else: # white figure blocking path
                        break
                # right
                for i in range(1, 8-field[1]):
                    if self.board[field[0]][field[1]+i] == 0:
                        moves.append([field[0], field[1]+i])
                    elif self.board[field[0]][field[1]+i] > 0:
                        moves.append([field[0], field[1]+i])
                        break
                    else: # white figure blocking path
                        break

            if figure == BISHOP_B or figure == QUEEN_B:
                # left down
                for i in range(1, min(field[0]+1, field[1]+1)):
                    if self.board[field[0]-i][field[1]-i] == 0:
                        moves.append([field[0]-i, field[1]-i])
                    elif self.board[field[0]-i][field[1]-i] > 0:
                        moves.append([field[0]-i, field[1]-i])
                        break
                    else: # white figure blocking path
                        break
                # left up
                for i in range(1, min(8-field[0], field[1]+1)):
                    if self.board[field[0]+i][field[1]-i] == 0:
                        moves.append([field[0]+i, field[1]-i])
                    elif self.board[field[0]+i][field[1]-i] > 0:
                        moves.append([field[0]+i, field[1]-i])
                        break
                    else: # white figure blocking path
                        break
                # right down
                for i in range(1, min(field[0]+1, 8-field[1])):
                    if self.board[field[0]-i][field[1]+i] == 0:
                        moves.append([field[0]-i, field[1]+i])
                    elif self.board[field[0]-i][field[1]+i] > 0:
                        moves.append([field[0]-i, field[1]+i])
                        break
                    else: # white figure blocking path
                        break
                # right up
                for i in range(1, min(8-field[0], 8-field[1])):
                    if self.board[field[0]+i][field[1]+i] == 0:
                        moves.append([field[0]+i, field[1]+i])
                    elif self.board[field[0]+i][field[1]+i] > 0:
                        moves.append([field[0]+i, field[1]+i])
                        break
                    else: # white figure blocking path
                        break

        return moves

    #TODO
    def setPossibleMoves(self):
        possibleMoves = []
        if not self.check:
            for i in range(8):
                for j in range(8):
                    if (self.onMove == WHITE and self.board[i][j] > 0) or \
                            (self.onMove == BLACK and self.board[i][j] < 0):
                        movesWithFigure = self.getMovesWithFigure([i, j])
                        for move in movesWithFigure:
                            possibleMoves.append([[i, j], move])
        else: # TODO can block check with another figure
            found = False
            for i in range(8):
                for j in range(8):
                    if (self.onMove == WHITE and self.board[i][j] == KING_W) or \
                            (self.onMove == BLACK and self.board[i][j] == KING_B):
                        moveWithKing = self.getMovesWithFigure([i, j])
                        possibleMoves = [[[i, j], move] for move in moveWithKing]
                        found = True
                        break
                if found:
                    break
        self.possibleMoves = possibleMoves

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

    def makeMove(self, move, promotion=False):
        print 'self.possibleMoves = {}\n'.format(self.possibleMoves)
        if move not in self.possibleMoves:
            return MOVE_INVALID

        # move from move[0] to move[1]; move = [[from y, from x], [to y], [to x]]
        figure = self.board[move[0][0]][move[0][1]]
        takes = False
        if self.board[move[1][0]][move[1][1]] != 0:
            takes = True
        self.board[move[0][0]][move[0][1]] = EMPTY
        self.board[move[1][0]][move[1][1]] = figure

        self.setPossibleMoves()
        self.attackedFields = [self.possibleMoves[i][1] for i in range(len(self.possibleMoves))]
        print 'self.attackedFields = {}\n'.format(self.attackedFields)

        if self.onMove == WHITE:
            self.onMove = BLACK
        else:
            self.onMove = WHITE

        # figure out if in special position
        specialPosition = self.isSpecialPosition()
        print 'self.possibleMoves = {}\n'.format(self.possibleMoves)
        self.changeClock(specialPosition)

        # write move to history
        if figure > 0:
            self.history[WHITE].append(moveToString(figure, move, takes, promotion, specialPosition))
        else:
            self.history[BLACK].append(moveToString(figure, move, takes, promotion, specialPosition))

        return specialPosition
