POSITION_DEFAULT = 10000

# Players
WHITE = 'White'
BLACK = 'Black'

# Game situations
MATE = 200
STALEMATE = 201
CHECK = 202

# Special moves
EN_PASSANT = 110
CAPTURE = 111
# PROMOTION = 12

# Error codes
MOVE_INVALID = 400


# Piece declarations.
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

# Pieces representations
PIECE_NAMES = {
    PAWN: '',
    BISHOP: 'B',
    KNIGHT: 'N',
    ROOK: 'R',
    QUEEN: 'Q',
    KING: 'K'
}
