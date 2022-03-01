# Author: Jenna Bucien
# Date: 12/03/2021
# Description: A representation of a Hasami Shogi game (version 1). The game
# is represented by the HasamiShogiGame class, which has the data members and
# methods necessary to play a complete game. When a HasamiShogiGame object is
# created, a 9x9 board is initialized. Playar 1 has 9 black pieces arranged
# in a row one one side of the board, and Player 2 has 9 red pieces on the
# opposite side of the board. The players take turns using the class’s
# make_move method to move their pieces vertically or horizontally
# across the board. The goal is to capture an opponent’s pieces by sandwiching
# them between one’s own pieces. The game ends when one player has captured
# 8 or 9 of their opponent’s pieces.

class InvalidPlayerError(Exception):
	"""
	Error raised when input is not 'RED' or 'BLACK' for methods that have
	'color' as a parameter.
	"""
	pass


class InvalidSquareError(Exception):
	"""
	Error raised when input for methods that have 'square', 'sq_origin', or
	'sq_dest' as a parameter are invalid. (For example: not in range a-i and
	1-9, not in algebraic notation.
	"""
	pass


class HasamiShogiGame:
	"""
	A class representing a Hasami Shogi game, which is played by two players:
	Player 1 with BLACK pieces and Player 2 with RED pieces. Contains data
	members: game_state, active_player, board, captured_black, and
	captured_red. Declaring a HasamiShogiGame object initializes a new game,
	where each player starts with 9 pieces, arranged in a row on opposite ends
	of a 9x9 board. The players take turns using the class’s make_move method
	to move their pieces vertically or horizontally across the board. The goal
	is to capture an opponent’s pieces by sandwiching them between one’s own
	pieces. The game ends when one player has captured 8 or 9 of their
	opponent’s pieces.
	"""

	def __init__(self):
		"""
		The constructor of the HasamiShogiGame class.
		Parameter: none
		Data members (all private):
			- game_state (str): 'UNFINISHED', 'RED_WON', or 'BLACK_WON'
				initializes to unfinished (in progress) game
			- active_player (str): 'BLACK' or 'RED'
				initializes to 'BLACK', as Black goes first
			- opponent (str): 'RED' or 'BLACK'
				initializes to 'RED', as Black goes first, so Red is the opponent
			- board (list): a representation of the current board state,
				initializes to starting board
			- captured_black (int): number of captured black pieces
				initializes to 0 captured pieces
			- captured_red (int): number of captured red pieces
				initializes to 0 captured pieces
		"""
		self._game_state = 'UNFINISHED'
		self._active_player = 'BLACK'
		self._opponent = 'RED'
		self._board = [[' ', 1, 2, 3, 4, 5, 6, 7, 8, 9],
		               ['a', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'],
		               ['b', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
		               ['c', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
		               ['d', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
		               ['e', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
		               ['f', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
		               ['g', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
		               ['h', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
		               ['i', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
		               ]
		self._captured_black = 0
		self._captured_red = 0

	def get_game_state(self):
		"""
		Parameter: none
		Returns:
		‘UNFINISHED’ (str): the game is still in progress
		‘RED_WON’ (str): Red has won the game
		‘BLACK_WON’ (str): Black has won the game
		"""
		return self._game_state

	def get_active_player(self):
		"""
		Parameter: none
		Returns:
		‘RED’ (str): it is currently Red’s turn
		‘BLACK’ (str): it is currently Black’s turn
		"""
		return self._active_player

	def get_num_captured_pieces(self, color):
		"""
		Parameter:
		color (str): ‘RED’ or ‘BLACK’
		Returns:
		(str) the number of pieces of that color that have been captured
		"""
		if color == 'RED':
			return self._captured_red
		elif color == 'BLACK':
			return self._captured_black
		else:
			raise InvalidPlayerError(
				'Method only takes RED or BLACK as arguments')

	def get_square_occupant(self, square):
		"""
		Parameters: square (str)
		Returns:
		'RED' (str) – square is occupied by a red piece
		'BLACK' (str) – square is occupied by a white piece
		'NONE' (None) – square is empty
		"""
		square_indices = self._translate_to_space(square)
		occupant = self._board[square_indices[0]][square_indices[1]]
		if occupant == 'R':
			return 'RED'
		elif occupant == 'B':
			return 'BLACK'
		else:
			return 'NONE'

	def display_board(self):
		"""
		Parameters: none
		Returns: print board to console
		"""
		for row_list in self._board:
			for square in row_list:
				print(square, end=' ')
			print('')

	def make_move(self, sq_origin, sq_dest):
		"""
		Parameters: sq_origin (str), sq_dest (str)
		Returns:
		'TRUE' (bool) – valid move was completed
		'FALSE' (bool) – if the origin square does not contain a
		piece belonging to the active player, or if the indicated
		move is invalid, or if the game has already been won
		"""
		try:
			coord_origin = self._translate_to_space(sq_origin)
			coord_dest = self._translate_to_space(sq_dest)
		except InvalidSquareError:
			return False

		validation = self._validate_move(coord_origin, coord_dest)
		if validation is False:
			return False
		else:
			self._move_piece(coord_origin, coord_dest)
			self._check_captures(coord_dest)
			if self._captured_red == 8 or self._captured_red == 9:
				self._game_state = 'BLACK_WON'
			elif self._captured_black == 8 or self._captured_black == 9:
				self._game_state = 'RED_WON'
			else:
				if self._active_player == 'RED':
					self._active_player = 'BLACK'
					self._opponent = 'RED'
				else:
					self._active_player = 'RED'
					self._opponent = 'BLACK'
			return True

	def _validate_move(self, coord_origin, coord_dest):
		"""
		A helper method called by make_move. Checks that the proposed move is
		valid, meaning that (a) the game is still ongoing (b) the move’s origin
		and destination squares are within bounds of the board (c) the origin
		square is occupied by the current player’s piece (d) the destination
		square is unoccupied (e) the destination square is either in the same
		column or the same row as the origin square (f) the squares between
		the origin and destination square are unoccupied
		Parameters: coord_origin (tuple), coord_dest (tuple)
		Returns:
			True (bool) – move is valid
			False (bool) – move is invalid
		"""
		if self._game_state != 'UNFINISHED':
			return False

		occupant_origin = self._board[coord_origin[0]][coord_origin[1]]
		occupant_dest = self._board[coord_dest[0]][coord_dest[1]]

		if occupant_origin == '.' or occupant_dest != '.':
			return False
		elif occupant_origin == 'R' and self._active_player != 'RED':
			return False
		elif occupant_origin == 'B' and self._active_player != 'BLACK':
			return False

		# determine that all squares between origin/destination are empty
		square = None
		end = None
		if coord_origin[0] == coord_dest[0]:  # same row
			if coord_origin[1] > coord_dest[1]:
				square = coord_dest[1] + 1
				end = coord_origin[1]
			else:
				square = coord_origin[1] + 1
				end = coord_dest[1]
			while square < end:
				if self._board[coord_origin[0]][square] != '.':
					return False
				square += 1
			else:
				return True
		elif coord_origin[1] == coord_dest[1]:  # same column
			if coord_origin[0] > coord_dest[0]:
				square = coord_dest[0] + 1
				end = coord_origin[0]
			else:
				square = coord_origin[0] + 1
				end = coord_dest[0]
			while square < end:
				if self._board[square][coord_origin[1]] != '.':
					return False
				square += 1
			return True
		else:                   # not in same row or column, so invalid move
			return False

	def _check_captures(self, coord_dest):
		"""
		A helper method called by make_move that checks if the move just made
		creates any capture conditions. First checks if corner capture can be
		made by calling helper method check_corners. If so, adds captured
		square to captured_list and moves to next capture condition. If no
		corner captures made, check for other capture conditions by
		manipulating board[j][k] indices to find adjacent squares and their
		occupying pieces. Returns list of squares captured and passes list to
		_make_capture.
		Parameter: coord_dest (tuple)
		Returns: captured_list (list)
		"""
		captured_list = self._check_corners(coord_dest)
		offset = 1                  # to traverse board indices away from coord_dest
		opponent_squares = []       # list of adjacent squares that contain opponent's piece

		# Check "up" direction
		if coord_dest[0] != 1:
			while (coord_dest[0] - offset) > 1 and\
					self._board[coord_dest[0] - offset][coord_dest[1]] == self._opponent[0]:
					opponent_squares.append((coord_dest[0] - offset, coord_dest[1]))
					offset += 1
			if self._board[coord_dest[0] - offset][coord_dest[1]] == self._active_player[0]\
						and len(opponent_squares) >= 1:
				captured_list = captured_list + opponent_squares
			else:
				opponent_squares = []
			offset = 1

		#Check "down" direction
		if coord_dest[0] != 9:
			while (coord_dest[0] + offset) < 9 and\
					self._board[coord_dest[0] + offset][coord_dest[1]] == self._opponent[0]:
					opponent_squares.append((coord_dest[0] + offset, coord_dest[1]))
					offset += 1
			if self._board[coord_dest[0] + offset][coord_dest[1]] == self._active_player[0]\
						and len(opponent_squares) >= 1:
				captured_list = captured_list + opponent_squares
			else:
				opponent_squares = []
			offset = 1

		# Check "left" direction
		if coord_dest[1] != 1:
			while (coord_dest[1] - offset) > 1 and\
					self._board[coord_dest[0]][coord_dest[1] - offset] == self._opponent[0]:
					opponent_squares.append((coord_dest[0], coord_dest[1] - offset))
					offset += 1
			if self._board[coord_dest[0]][coord_dest[1] - offset] == self._active_player[0]\
						and len(opponent_squares) >= 1:
				captured_list = captured_list + opponent_squares
			else:
				opponent_squares = []
			offset = 1

		# Check "right" direction
		if coord_dest[1] != 9:
			while (coord_dest[1] + offset) < 9 and\
					self._board[coord_dest[0]][coord_dest[1] + offset] == self._opponent[0]:
				opponent_squares.append((coord_dest[0], coord_dest[1] + offset))
				offset += 1
				if self._board[coord_dest[0]][coord_dest[1] + offset] == self._active_player[0]\
						and len(opponent_squares) >= 1:
					captured_list = captured_list + opponent_squares

		self._make_capture(captured_list)

	def _check_corners(self, coord_dest):
		"""
		A helper method called by check_captures. Determines that an opponent's
		piece is in one of the corner squares. The corner squares have indices
		(1,1), (1,9), (9,1) and (9,9). If an opponent's piece occupies one of
		these corners, determines if the move just made creates a corner
		capture condition, meaning that the active player occupies the two
		orthogonal squares. If a capture condition exists, adds captured square
		to capture_list.
		Parameter: coord_dest (tuple)
		Returns: captured_list (list)
		"""
		captured_list = []
		if self._board[1][1] == self._opponent[0]:
			if (coord_dest == (1,2) and self._board[2][1] == self._active_player[0]) or\
				(coord_dest == (2,1) and self._board[1][2] == self._active_player[0]):
				captured_list.append((1,1))
		if self._board[1][9] == self._opponent[0]:
			if (coord_dest == (1,8) and self._board[2][9] == self._active_player[0]) or\
				(coord_dest == (2,9) and self._board[1][8] == self._active_player[0]):
				captured_list.append((1,9))
		if self._board[9][1] == self._opponent[0]:
			if (coord_dest == (8,1) and self._board[9][2] == self._active_player[0]) or\
				(coord_dest == (9,2) and self._board[8][1] == self._active_player[0]):
				captured_list.append((9,1))
		if self._board[9][9] == self._opponent[0]:
			if (coord_dest == (9,8) and self._board[8][9] == self._active_player[0]) or\
				(coord_dest == (8,9) and self._board[9][8] == self._active_player[0]):
				captured_list.append((9,9))
		return captured_list

	def _make_capture(self, captured_list):
		"""
		A helper method called by _check_captures that removes captured pieces
		from the board. For each element in captured_list, changes the value
		at the corresponding square to ',' (unoccupied) and increases the
		captured_black or captured_red count by one.
		Parameter: captured_list (list)
		Returns: none
		"""
		for square in captured_list:
			if self._board[square[0]][square[1]] == 'B':
				self._captured_black += 1
			elif self._board[square[0]][square[1]] == 'R':
				self._captured_red += 1
			self._board[square[0]][square[1]] = '.'

	def _move_piece(self, coord_origin, coord_dest):
		"""
		A helper method called by make_move that moves a piece from a
		validated origin square to a validated destination square.
		Replaces the ‘R’ or ‘B’ at the origin square with a '.', meaning that
		the square is now unoccupied. Then replaces the ',' at the destination
		square with a ‘R’ or ‘B’, depending on whose turn it is.
		Parameters: coord_origin (tuple), coord_dest (tuple)
		Returns: none
		"""
		# sq_destination = sq_origin  (moving piece)
		self._board[coord_dest[0]][coord_dest[1]] =\
			self._board[coord_origin[0]][coord_origin[1]]
		# sq_origin = '.'
		self._board[coord_origin[0]][coord_origin[1]] = '.'

	def _translate_to_space(self, square):
		"""
		A helper method that takes a board location in algebraic notation.
		Splits the string into a two-element list. The list[0] is the letter
		that represents the square’s row. The list[1] is the number that
		represents the square’s column.
		Parameters: square (str)
		Returns:
			(j, k) (tuple): j is the index of the board’s rows a-i that
			corresponds to the passed-in algebraic notation. k is the index of
			the board’s columns 1-9 that corresponds to the passed-in
			algebraic notation.
		"""
		square_list = list(square)
		column_num = ''.join(square_list[1:])
		if ord(square_list[0]) not in range(97, 106):           # ord() converts chars to their ascii code
			raise InvalidSquareError('Invalid row. Rows must be in range a-i.')
		elif int(column_num) not in range(1, 10):
			raise InvalidSquareError(
				'Invalid column number. Columns must be in range 1-9.')
		else:
			char_to_index = ord(square_list[0]) - 96            # because 97 is ascii code for 'a'
			board_indices = (char_to_index, int(column_num))
			return board_indices


