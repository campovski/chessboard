from interface.chessboard import *

game = Chessboard(debug=False)
game.makeMove([[1, 4], [3, 4]])

game.makeMove([[6, 3], [4, 3]])

game.makeMove([[0, 6], [2, 5]])
game.makeMove([[6, 4], [4, 4]])
game.makeMove([[0, 5], [2, 3]])
game.makeMove([[7, 3], [5, 3]])
# fail castling by moving kings
game.makeMove([[0, 4], [1, 4]])
game.makeMove([[6, 1], [5, 1]])
game.makeMove([[1, 4], [0, 4]])
game.makeMove([[6, 2], [5, 2]])
# castle
game.makeMove([[0, 4], [0, 6]])
game.makeMove([[0, 7], [0, 5]])
# end of castle move
game.makeMove([[6, 0], [4, 0]])

"""
game.makeMove([[3, 4], [4, 4]])
game.makeMove([[6, 5], [4, 5]])

game.makeMove([[6, 4], [4, 4]])
game.makeMove([[0, 3], [4, 7]])
game.makeMove([[7, 4], [6, 4]])
game.makeMove([[4, 7], [4, 4]])


game.makeMove([[6, 3], [4, 3]])
game.makeMove([[3, 4], [4, 3]])
"""
print game.history

print game
