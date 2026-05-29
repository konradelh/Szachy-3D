class chess: 
      def __init__(self): 
            self.white_pawns   = chess.WHITE_PAWNS
            self.white_knights = chess.WHITE_KNIGHTS
            self.white_bishops = chess.WHITE_BISHOPS
            self.white_rooks   = chess.WHITE_ROOKS
            self.white_queen   = chess.WHITE_QUEEN
            self.white_king    = chess.WHITE_KING

            self.black_pawns   = chess.BLACK_PAWNS
            self.black_knights = chess.BLACK_KNIGHTS
            self.black_bishops = chess.BLACK_BISHOPS
            self.black_rooks   = chess.BLACK_ROOKS
            self.black_queen   = chess.BLACK_QUEEN
            self.black_king    = chess.BLACK_KING

            self.white_pieces = chess.WHITE_PIECES
            self.black_pieces = chess.BLACK_PIECES

            self.all_pieces = chess.ALL_PIECES
      def printBoard(self): 
            print("    -----------------")
            for rank in reversed(range(8)): 
                  rowString = f"{rank + 1} |"
                  for file in range(8): 
                        mask = 1 << (rank*8 + file)
                        if mask & self.all_pieces: rowString += "1 "
                        else: rowString += "0 "
                  print(rowString) 
            print("    -----------------")
            print("    a b c d e f g h")
      FILE_A = 0x0101010101010101
      FILE_B = 0x0202020202020202
      FILE_C = 0x0404040404040404
      FILE_D = 0x0808080808080808
      FILE_E = 0x1010101010101010
      FILE_F = 0x2020202020202020
      FILE_G = 0x4040404040404040
      FILE_H = 0x8080808080808080

      # Ranks (wiersze)
      RANK_1 = 0x00000000000000FF
      RANK_2 = 0x000000000000FF00
      RANK_3 = 0x0000000000FF0000
      RANK_4 = 0x00000000FF000000
      RANK_5 = 0x000000FF00000000
      RANK_6 = 0x0000FF0000000000
      RANK_7 = 0x00FF000000000000
      RANK_8 = 0xFF00000000000000

      # POZYCJE STARTOWE
      WHITE_PAWNS   = RANK_2
      WHITE_KNIGHTS = 0x0000000000000042 # b1, g1
      WHITE_BISHOPS = 0x0000000000000024 # c1, f1
      WHITE_ROOKS   = 0x0000000000000081 # a1, h1
      WHITE_QUEEN   = 0x0000000000000008 # d1
      WHITE_KING    = 0x0000000000000010 # e1

      BLACK_PAWNS   = RANK_7
      BLACK_KNIGHTS = 0x4200000000000000 # b8, g8
      BLACK_BISHOPS = 0x2400000000000000 # c8, f8
      BLACK_ROOKS   = 0x8100000000000000 # a8, h8
      BLACK_QUEEN   = 0x0800000000000000 # d8
      BLACK_KING    = 0x1000000000000000 # e8
      
      WHITE_PIECES  = WHITE_PAWNS | WHITE_KNIGHTS | WHITE_BISHOPS | WHITE_ROOKS | WHITE_QUEEN | WHITE_KING
      BLACK_PIECES  = BLACK_PAWNS | BLACK_KNIGHTS | BLACK_BISHOPS | BLACK_ROOKS | BLACK_QUEEN | BLACK_KING
      ALL_PIECES    = WHITE_PIECES | BLACK_PIECES


      WHITE = 1
      BLACK = 0

      PAWN_ATTACKS = []
      KNIGHT_ATTACKS = []

      POSITIVE_RAY_BITBOARDS = []
      NEGATIVE_RAY_BITBOARDS = []
      @classmethod 
      def generateSquares(cls):
            squares = {} 


            for rank in range(8): 
                  for file in range(8): 
                        squareName = f"{chr(ord('a') + file)}{rank + 1}"
                        squares[squareName] =  (rank*8 + file) # sam indeks, w postaci pola bitowej trzeba przesunac o index 1 <<  index 
            return squares
      
      @classmethod 
      def generatePawnAttacks(cls): 
            cls.PAWN_ATTACKS = [[0] * 64, [0] * 64]

            for bitIndex in range(64):
                  position = 1 << bitIndex
                        #biale lewo skos <<  7 prawo skos - << 9
                  if position & ~cls.FILE_A:   
                        cls.PAWN_ATTACKS[cls.WHITE][bitIndex] |= (position << 7)
                  if position & ~cls.FILE_H:
                        cls.PAWN_ATTACKS[cls.WHITE][bitIndex] |= (position << 9)

                  #czarne 
                  if position & ~cls.FILE_A:   
                        cls.PAWN_ATTACKS[cls.BLACK][bitIndex] |= (position >> 9)
                  if position & ~cls.FILE_H:
                        cls.PAWN_ATTACKS[cls.BLACK][bitIndex] |= (position >> 7)

            return cls.PAWN_ATTACKS




        #noNoWe    noNoEa
            #+15  +17
             #|     |
#noWeWe  +6 __|     |__+10  noEaEa
              #\   /
               #>0<
           #__ /   \ __
#soWeWe -10   |     |   -6  soEaEa
             #|     |
            #-17  -15
        #soSoWe    soSoEa

      @classmethod 
      def generateKnightAttacks(cls): 
            cls.KNIGHT_ATTACKS = [0]*64

            for bitIndex in range(64): 
                  position = 1 << bitIndex
                  noNoEa = (position << 17) & ~(cls.FILE_A)
                  noEaEa = (position << 10) & ~(cls.FILE_A | cls.FILE_B)
                  soEaEa = (position >> 6) & ~(cls.FILE_A | cls.FILE_B)
                  soSoEa = (position >> 15)& ~cls.FILE_A
                  noNoWe = (position << 15) & ~(cls.FILE_H)
                  noWeWe = (position << 6) & ~(cls.FILE_G | cls.FILE_H)
                  soWeWe = (position >> 10 )  & ~(cls.FILE_G | cls.FILE_H)
                  soSoWe = (position >> 17) & ~cls.FILE_H

                  cls.KNIGHT_ATTACKS[bitIndex] = noNoEa | noEaEa | soEaEa | soSoEa | noNoWe | noWeWe | soWeWe | soSoWe
            return cls.KNIGHT_ATTACKS
      @classmethod
      def generatePositiveRays(cls): 
            positiveRaysCoefficients = {"e": 1, "n": 8, "ne":9 , "nw":7} 
            cls.POSITIVE_RAY_BITBOARDS = [[0] * 64 for _ in range(4)] 
            for square in range(64): 
                  for index, coeff in enumerate(positiveRaysCoefficients.values()): 
                        nextSquare = square 
                        while(nextSquare<63): 
                              cls.POSITIVE_RAY_BITBOARDS[index][square] |= 1 << (nextSquare + coeff)
                              nextSquare += coeff
            return cls.POSITIVE_RAY_BITBOARDS
      @classmethod
      def generateNegativeRays(cls): 
            negativeRaysCoefficients = {"w": 1, "s": 8, "se":9 , "sw":7} 
            cls.NEGATIVE_RAY_BITBOARDS = [[0] * 64 for _ in range(4)] 
            for square in range(64): 
                  for index, coeff in enumerate(negativeRaysCoefficients.values()): 
                        nextSquare = square 
                        while(nextSquare  >0): 
                              cls.NEGATIVE_RAY_BITBOARDS[index][square] |= (1 << nextSquare) >> ( coeff)
                              nextSquare -= coeff
            return cls.NEGATIVE_RAY_BITBOARDS


                  
      @staticmethod
      def getMSB(bitboard): 
            return bitboard.bit_length() -1 

      @staticmethod
      def getLSB(bitboard): 
            return (bitboard & -bitboard).bit_length() -1  # -x == ~x + 1 
      @staticmethod
      def printBitBoard(bitboard): 
            print("    -----------------")
            for rank in reversed(range(8)): 
                  rowString = f"{rank + 1} |"
                  for file in range(8): 
                        mask = 1 << (rank*8 + file)
                        if mask & bitboard: rowString += "1 "
                        else: rowString += "0 "
                  print(rowString) 
            print("    -----------------")
            print("    a b c d e f g h")
 



      
chess.SQUARES = chess.generateSquares()
chess.PAWN_ATTACKS = chess.generatePawnAttacks() 
chess.KNIGHT_ATTACKS = chess.generateKnightAttacks()
chess.POSITIVE_RAY_BITBOARDS = chess.generatePositiveRays()
chess.NEGATIVE_RAY_BITBOARDS = chess.generateNegativeRays()
game = chess() 
game.printBoard()
game.printBitBoard(chess.KNIGHT_ATTACKS[chess.SQUARES['e5']])
print(chess.SQUARES['h8'])
game.printBitBoard(chess.PAWN_ATTACKS[chess.BLACK][chess.SQUARES['h8']])
game.printBitBoard(chess.POSITIVE_RAY_BITBOARDS[2][chess.SQUARES['h8']])
game.printBitBoard(chess.NEGATIVE_RAY_BITBOARDS[2][chess.SQUARES['e5']])