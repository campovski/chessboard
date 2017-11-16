POSITION_DEFAULT = 0

# Players
WHITE = 'White'
BLACK = 'Black'

# Game situations
MATE = 'm'
STALEMATE = 'sm'
CHECK = 'c'

# Special moves
EN_PASSANT = 10
CAPTURE = 11
# PROMOTION = 12
MOVE_INVALID = 13


# Figure declarations.
EMPTY = 0
PAWN = 1
BISHOP = 2
KNIGHT = 3
ROOK = 4
QUEEN = 5
KING = 6
PAWN_W = PAWN
PAWN_B = -PAWN
BISHOP_W = BISHOP
BISHOP_B = -BISHOP
KNIGHT_W = KNIGHT
KNIGHT_B = -KNIGHT
ROOK_W = ROOK
ROOK_B = -ROOK
QUEEN_W = QUEEN
QUEEN_B = -QUEEN
KING_W = KING
KING_B = -KING

# Figures representations
FIGURE_NAMES = {
    PAWN: '',
    BISHOP: 'B',
    KNIGHT: 'N',
    ROOK: 'R',
    QUEEN: 'Q',
    KING: 'K'
}
