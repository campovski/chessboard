from interface.chessboard import *

game = Chessboard()
game.makeMove([[1, 4], [3, 4]])

game.makeMove([[6, 3], [5, 3]])
game.makeMove([[3, 4], [4, 4]])
game.makeMove([[6, 5], [4, 5]])

"""
game.makeMove([[6, 4], [4, 4]])
game.makeMove([[0, 3], [4, 7]])
game.makeMove([[7, 4], [6, 4]])
game.makeMove([[4, 7], [4, 4]])


game.makeMove([[6, 3], [4, 3]])
game.makeMove([[3, 4], [4, 3]])
"""
print game.history

print game
