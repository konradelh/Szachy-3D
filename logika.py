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
            self.all_pieces = self.white_pieces | self.black_pieces

            self.piecesTable = [[0]*6 for _ in range(2)]
            self.piecesTable[chess.WHITE][0] = self.white_pawns
            self.piecesTable[chess.WHITE][1] = self.white_king
            self.piecesTable[chess.WHITE][2] = self.white_rooks
            self.piecesTable[chess.WHITE][3] = self.white_knights
            self.piecesTable[chess.WHITE][4] = self.white_bishops
            self.piecesTable[chess.WHITE][5] = self.white_queen

            self.piecesTable[chess.BLACK][0] = self.black_pawns
            self.piecesTable[chess.BLACK][1] = self.black_king
            self.piecesTable[chess.BLACK][2] = self.black_rooks
            self.piecesTable[chess.BLACK][3] = self.black_knights
            self.piecesTable[chess.BLACK][4] = self.black_bishops
            self.piecesTable[chess.BLACK][5] = self.black_queen


            self.allPiecesTable = [0] * 2
            for i in range(2):
                      for j in range(6): 
                            self.allPiecesTable[i] |= self.piecesTable[i][j]


            self.enPassantSquare = 0 
            self.pseudoMoves = []


      FILE_A = 0x0101010101010101
      FILE_B = 0x0202020202020202
      FILE_C = 0x0404040404040404
      FILE_D = 0x0808080808080808
      FILE_E = 0x1010101010101010
      FILE_F = 0x2020202020202020
      FILE_G = 0x4040404040404040
      FILE_H = 0x8080808080808080
      FILES = (FILE_A, FILE_B, FILE_C, FILE_D, FILE_E, FILE_F, FILE_G, FILE_H)

      # Ranks (wiersze)
      RANK_1 = 0x00000000000000FF
      RANK_2 = 0x000000000000FF00
      RANK_3 = 0x0000000000FF0000
      RANK_4 = 0x00000000FF000000
      RANK_5 = 0x000000FF00000000
      RANK_6 = 0x0000FF0000000000
      RANK_7 = 0x00FF000000000000
      RANK_8 = 0xFF00000000000000
      RANKS = (RANK_1, RANK_2, RANK_3, RANK_4, RANK_5, RANK_6, RANK_7, RANK_8)
      MASK_WHOLE_BOARD = 0xFFFFFFFFFFFFFFFF
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
      KING_ATTACKS = []

      POSITIVE_RAY_BITBOARDS = []
      NEGATIVE_RAY_BITBOARDS = []


      def generateBishopAttacks(self, square):

            attacks = 0
            occupancy = self.all_pieces
            for direction in range(2, len(chess.POSITIVE_RAY_BITBOARDS)): 
                  mask = chess.POSITIVE_RAY_BITBOARDS[direction][square] & occupancy
                  if (mask):
                        lsbMask = self.getLSB(mask)
                        attacks |=  chess.POSITIVE_RAY_BITBOARDS[direction][square] ^ chess.POSITIVE_RAY_BITBOARDS[direction][lsbMask]
                        # Zwraca ataki RAZEM z pierwszą napotkaną blokadą, check czy można zbić będzie w funkcji ruchu
                  else: # w przypadku gdyby nie było blokad 
                        attacks |= chess.POSITIVE_RAY_BITBOARDS[direction][square]

            for direction in range(2, len(chess.NEGATIVE_RAY_BITBOARDS)): 
                  mask = chess.NEGATIVE_RAY_BITBOARDS[direction][square] & occupancy
                  if(mask): 
                        msbMask = self.getMSB(mask)
                        attacks |= chess.NEGATIVE_RAY_BITBOARDS[direction][square] ^ chess.NEGATIVE_RAY_BITBOARDS[direction][msbMask]
                  else: # w przypadku gdyby nie było blokad 
                        attacks |= chess.NEGATIVE_RAY_BITBOARDS[direction][square]

            return attacks
      
      def generateRookAttacks(self, square):
            
            attacks = 0
            occupancy = self.all_pieces
            for direction in range(0, 2): 
                  mask = chess.POSITIVE_RAY_BITBOARDS[direction][square] & occupancy
                  if (mask):
                        lsbMask = self.getLSB(mask)
                        attacks |=  chess.POSITIVE_RAY_BITBOARDS[direction][square] ^ chess.POSITIVE_RAY_BITBOARDS[direction][lsbMask]
                        # Zwraca ataki RAZEM z pierwszą napotkaną blokadą, check czy można zbić będzie w funkcji ruchu
                  else: # w przypadku gdyby nie było blokad 
                        attacks |= chess.POSITIVE_RAY_BITBOARDS[direction][square]
            for direction in range(0, 2): 
                  mask = chess.NEGATIVE_RAY_BITBOARDS[direction][square] & occupancy
                  if(mask): 
                        msbMask = self.getMSB(mask)
                        attacks |= chess.NEGATIVE_RAY_BITBOARDS[direction][square] ^ chess.NEGATIVE_RAY_BITBOARDS[direction][msbMask]
                  else: # w przypadku gdyby nie było blokad 
                        attacks |= chess.NEGATIVE_RAY_BITBOARDS[direction][square]


            return attacks
      

       
      def generateQueenAttacks(self, square):
            return self.generateBishopAttacks(square) | self.generateRookAttacks(square)
                       
            



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
                        cls.PAWN_ATTACKS[cls.WHITE][bitIndex] &= cls.MASK_WHOLE_BOARD
                  if position & ~cls.FILE_H:
                        cls.PAWN_ATTACKS[cls.WHITE][bitIndex] |= (position << 9)
                        cls.PAWN_ATTACKS[cls.WHITE][bitIndex] &= cls.MASK_WHOLE_BOARD

                  #czarne 
                  if position & ~cls.FILE_A:   
                        cls.PAWN_ATTACKS[cls.BLACK][bitIndex] |= (position >> 9)
                        cls.PAWN_ATTACKS[cls.BLACK][bitIndex] &= cls.MASK_WHOLE_BOARD
                  if position & ~cls.FILE_H:
                        cls.PAWN_ATTACKS[cls.BLACK][bitIndex] |= (position >> 7)
                        cls.PAWN_ATTACKS[cls.BLACK][bitIndex] &= cls.MASK_WHOLE_BOARD

            return cls.PAWN_ATTACKS

      @classmethod
      def generateKingAttacks(cls): 
            cls.KING_ATTACKS = [0] *64
            for index in range(64): 
                  position = 1 << index 
                  eastAndWest = ((position << 1) ) | ((position >> 1) ) | position # jedynka w srodku usuwana na koncu
                  eastAndWest = eastAndWest | (eastAndWest >> 8) | (eastAndWest << 8)
                  
                  finalMask = eastAndWest 
                  if((1 << index) & chess.FILE_H) : finalMask &= ~chess.FILE_A 
                  if((1 << index) & chess.FILE_A) : finalMask &= ~chess.FILE_H 

                  wholeboard = 0 
                  for rank in (cls.RANKS):
                        wholeboard |= rank

                  finalMask &= wholeboard
                  chess.KING_ATTACKS[index] = chess.popBit(finalMask, index)
            return cls.KING_ATTACKS





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
                  cls.KNIGHT_ATTACKS[bitIndex] &= cls.MASK_WHOLE_BOARD
            return cls.KNIGHT_ATTACKS
      @classmethod
      def generatePositiveRays(cls): 
            
            positiveRaysCoefficients = {"e": 1, "n": 8, "ne":9 , "nw":7} 
            cls.POSITIVE_RAY_BITBOARDS = [[0] * 64 for _ in range(4)] 
            for square in range(64): 
                  squareRank = square//8 
                  squareFile = square - squareRank*8 


                  eastMask = 0
                  westMask = 0 
                  northMask = 0 
                  for file in range(squareFile,len(cls.FILES)): 
                        eastMask |= cls.FILES[file] 
                  

                  for file in range(0, squareFile):
                        westMask |= cls.FILES[file]
#                  eastMask &= cls.RANKS[squareRank]

                  for rank in range(squareRank, len(cls.RANKS)): 
                        northMask |= cls.RANKS[rank]

                  northEastMask = northMask & eastMask
                  northWestMask = northMask & westMask

                  eastMask &= cls.RANKS[squareRank] 
                  northMask &= cls.FILES[squareFile]

                  masks = [eastMask, northMask, northEastMask, northWestMask]
                  for index, coeff in enumerate(positiveRaysCoefficients.values()): 
                        nextSquare = square 
                        while 0<= nextSquare <= 63: 
                              cls.POSITIVE_RAY_BITBOARDS[index][square] |= 1 << (nextSquare + coeff)
                              cls.POSITIVE_RAY_BITBOARDS[index][square] &= masks[index]
                              cls.POSITIVE_RAY_BITBOARDS[index][square] &= cls.MASK_WHOLE_BOARD
                              nextSquare += coeff
            return cls.POSITIVE_RAY_BITBOARDS

      @classmethod
      def generateNegativeRays(cls): 
            negativeRaysCoefficients = {"w": 1, "s": 8, "se":7 , "sw":9} 
            cls.NEGATIVE_RAY_BITBOARDS = [[0] * 64 for _ in range(4)] 
            for square in range(64): 
                  squareRank = square//8 
                  squareFile = square - squareRank*8 

                  southMask = 0
                  eastmask = 0 
                  westMask = 0

                  for file in range(0, squareFile):
                        westMask |= cls.FILES[file]
                  for file in range(squareFile, len(cls.FILES)): 
                        eastmask |= cls.FILES[file]
                  for rank in range(0, squareRank): 
                        southMask |= cls.RANKS[rank]

                  southEastMask = eastmask & southMask & ~cls.FILES[squareFile] # znaleziono podczas generacji w partii 
                  southWestMask = westMask & southMask & ~cls.FILES[squareFile]

                  southMask &= cls.FILES[squareFile]
                  westMask &= cls.RANKS[squareRank]

                  masks = [westMask, southMask, southEastMask, southWestMask]

                  for index, coeff in enumerate(negativeRaysCoefficients.values()): 
                              nextSquare = square 
                              while 0<= nextSquare <= 63: 
                                    cls.NEGATIVE_RAY_BITBOARDS[index][square] |= (1 << nextSquare) >> ( coeff)
                                    nextSquare -= coeff
                                    cls.NEGATIVE_RAY_BITBOARDS[index][square] &= masks[index]
                                    cls.NEGATIVE_RAY_BITBOARDS[index][square] &= cls.MASK_WHOLE_BOARD
            return cls.NEGATIVE_RAY_BITBOARDS


                  
      @staticmethod
      def getMSB(bitboard): 
            return bitboard.bit_length() -1 

      @staticmethod
      def getLSB(bitboard): 
            return (bitboard & -bitboard).bit_length() -1  # -x == ~x + 1 
      @staticmethod
      def popBit(bitboard, square): 
            
            return bitboard & (~(1 << square))
      @staticmethod
      def insertBit(bitboard, square): 
            return bitboard | (1<<square)
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


            print(f"Bitboard = {(bitboard)}")


      @classmethod
      def indexToSquare(self, index): 
            rank = index // 8 
            file   =index - rank * 8
            return f"{chr(ord('a')+file)}{chr(ord('1') +rank)}"

      def generateMoves(self,  fromSquareIndex): 
            fromSquare = 1 << fromSquareIndex
            potentialEnPassant = self.enPassantSquare

            if(fromSquare & self.white_pieces): color = self.WHITE
            elif(fromSquare & self.black_pieces): color = self.BLACK
            else: return 0 

            if(color==self.WHITE): opponent_occupancy = self.black_pieces
            else: opponent_occupancy = self.white_pieces



#######################################
# PAWNS 
######################################
            if (fromSquare & self.piecesTable[color][0]): 
                  if (color == chess.WHITE):
                              toSquare = fromSquare << 8
                              if (toSquare & ~self.all_pieces):
                                    self.pseudoMoves.append(Move(fromSquareIndex, fromSquareIndex + 8, 0,0,1,0))
                                    print(f" push from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(fromSquareIndex + 8)}")
                                    if(fromSquare & self.RANK_2): 
                                          toSquare <<= 8 
                                          if(toSquare & ~self.all_pieces): 
                                                self.pseudoMoves.append(Move(fromSquareIndex, self.getMSB(toSquare), 0,0,1,0))
                                                print(f" double push from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(self.getMSB(toSquare))}")
                                    if (fromSquare & self.RANK_7): 
                                                self.pseudoMoves.append(Move(fromSquareIndex, self.getMSB(toSquare), 0,0,0,1))
                                                print(f" promotion push from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(self.getMSB(toSquare))}")
                                    if ((fromSquareIndex +7 == potentialEnPassant)  or (fromSquareIndex + 9 == potentialEnPassant))  and ((1<<(potentialEnPassant -8 )) & self.piecesTable[chess.BLACK][0]):
                                          self.pseudoMoves.append(Move(fromSquareIndex, potentialEnPassant, 1,0,0,0,1))
                                          print(f"en passant capture from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(potentialEnPassant)}")

                              attacks = chess.PAWN_ATTACKS[color][fromSquareIndex]
                              while (attacks != 0): 
                                     possibleAttackIndex = self.getMSB(attacks)
                                     possibleAttack = 1 << possibleAttackIndex
                                     if (possibleAttack & opponent_occupancy): 
                                           self.pseudoMoves.append(Move(fromSquareIndex, possibleAttackIndex,1,0,0,0))
                                           print(f"attack pawn move from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(possibleAttackIndex)}")
                                     attacks = self.popBit(attacks, possibleAttackIndex) 

                  else: 
                              toSquare = fromSquare >> 8
                              if (toSquare & ~self.all_pieces):
                                    self.pseudoMoves.append(Move(fromSquareIndex, fromSquareIndex - 8, 0,0,1,0))
                                    print(f" push from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(fromSquareIndex -8)}")
                                    if(fromSquare & self.RANK_7): 
                                          toSquare >>= 8 
                                          if(toSquare & ~self.all_pieces): 
                                                self.pseudoMoves.append(Move(fromSquareIndex, self.getMSB(toSquare), 0,0,1,0))
                                                print(f" double push from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(self.getMSB(toSquare))}")
                                    if (fromSquare & self.RANK_2): 
                                                self.pseudoMoves.append(Move(fromSquareIndex, self.getMSB(toSquare), 0,0,0,1))
                                                print(f" promotion push from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(self.getMSB(toSquare))}")
                                    if ((fromSquareIndex -7 == potentialEnPassant)  or (fromSquareIndex - 9 == potentialEnPassant))and ((1<<(potentialEnPassant +8 )) & self.piecesTable[chess.WHITE][0]):
                                                                              self.pseudoMoves.append(Move(fromSquareIndex, potentialEnPassant, 1,0,0,0,1))
                                                                              print(f"en passant capture from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(potentialEnPassant)}")

                              attacks = chess.PAWN_ATTACKS[color][fromSquareIndex]
                              while (attacks != 0): 
                                     possibleAttackIndex = self.getMSB(attacks)
                                     possibleAttack = 1 << possibleAttackIndex
                                     if (possibleAttack & opponent_occupancy): 
                                           self.pseudoMoves.append(Move(fromSquareIndex, possibleAttackIndex,1,0,0,0))
                                           print(f"attack pawn move from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(possibleAttackIndex)}")
                                     attacks = self.popBit(attacks, possibleAttackIndex) 


 #######################################
# KNIGHTS
######################################

 
                                          
            if (fromSquare & self.piecesTable[color][3]): 
                  attacks = chess.KNIGHT_ATTACKS[fromSquareIndex] 

                  while (attacks != 0):  
                        possibleAttackIndex = self.getMSB(attacks)
                        possibleAttack = 1 << possibleAttackIndex
                        if(possibleAttack & ~self.all_pieces): 
                              self.pseudoMoves.append(Move(fromSquareIndex, possibleAttackIndex,0,0,0,0))
                              print(f"quiet knight move from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(possibleAttackIndex)}")
                        if (possibleAttack & opponent_occupancy): 
                              self.pseudoMoves.append(Move(fromSquareIndex, possibleAttackIndex,1,0,0,0))
                              print(f"attack knight move from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(possibleAttackIndex)}")
                        attacks = self.popBit(attacks, possibleAttackIndex)
 
#######################################
# BISHOPS
######################################
            if (fromSquare & self.piecesTable[color][4]):
                  attacks = game.generateBishopAttacks(fromSquareIndex)
                  self.calculateMovesFromTables(attacks, "bishop", fromSquareIndex, opponent_occupancy)
                       
#######################################
# ROOKS
######################################
 
            if( fromSquare & self.piecesTable[color][2]): 
                  attacks = game.generateRookAttacks(fromSquareIndex)
                  self.calculateMovesFromTables(attacks, "rooks", fromSquareIndex, opponent_occupancy)

#######################################
# QUEENS 
######################################
 
            if( fromSquare & self.piecesTable[color][5]): 
                  attacks = game.generateQueenAttacks(fromSquareIndex)
                  self.calculateMovesFromTables(attacks, "queen", fromSquareIndex, opponent_occupancy)
#######################################
# KING 
######################################
 
            if( fromSquare & self.piecesTable[color][1]): 
                  attacks = chess.KING_ATTACKS[fromSquareIndex]
                  self.calculateMovesFromTables(attacks, "king", fromSquareIndex, opponent_occupancy)

                  if(color == chess.WHITE): 
                        if bool(fromSquare & chess.WHITE_KING) and  self.isEmpty(chess.SQUARES['f1']) and  self.isEmpty(chess.SQUARES['g1']) and  bool((1<< chess.SQUARES['h1']) & self.piecesTable[color][2]): 
                              toSquareIndex = chess.SQUARES['g1']
                              self.pseudoMoves.append(Move(fromSquareIndex, toSquareIndex, 0, 1, 0, 0)) # king side castle 
                              print(f"king-side castle from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(toSquareIndex)}")

                        if bool(fromSquare & chess.WHITE_KING) and self.isEmpty(chess.SQUARES['d1']) and  self.isEmpty(chess.SQUARES['c1'])and self.isEmpty(chess.SQUARES['b1']) and  bool(1<< chess.SQUARES['a1']) & self.piecesTable[color][2]: 
                              toSquareIndex = chess.SQUARES['c1']
                              self.pseudoMoves.append(Move(fromSquareIndex, toSquareIndex, 0, 1, 0, 0)) # queen side castle 
                              print(f"queen-side castle from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(toSquareIndex)}")
                  if(color == chess.BLACK): 
                        if bool(fromSquare & chess.BLACK_KING) and  self.isEmpty(chess.SQUARES['f8']) and  self.isEmpty(chess.SQUARES['g8'])  and  bool((1<< chess.SQUARES['h8']) & self.piecesTable[color][2]): 
                              toSquareIndex = chess.SQUARES['g8']
                              self.pseudoMoves.append(Move(fromSquareIndex, toSquareIndex, 0, 1, 0, 0)) # king side castle 
                              print(f"king-side castle from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(toSquareIndex)}")

                        if bool(fromSquare & chess.BLACK_KING) and self.isEmpty(chess.SQUARES['d8']) and  self.isEmpty(chess.SQUARES['c8'])and self.isEmpty(chess.SQUARES['b8']) and  bool((1<< chess.SQUARES['a8']) & self.piecesTable[color][2]): 
                              toSquareIndex = chess.SQUARES['c8']
                              self.pseudoMoves.append(Move(fromSquareIndex, toSquareIndex, 0, 1, 0, 0)) # queen side castle 
                              print(f"queen-side castle from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(toSquareIndex)}")
 




      def calculateMovesFromTables(self, attacks, piece, fromSquareIndex, opponent_occupancy): 
                  while (attacks != 0):  
                        possibleAttackIndex = self.getMSB(attacks)
                        possibleAttack = 1 << possibleAttackIndex
                        if(possibleAttack & ~self.all_pieces): 
                              self.pseudoMoves.append(Move(fromSquareIndex, possibleAttackIndex,0,0,0,0))
                              print(f"quiet {piece} move from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(possibleAttackIndex)}")
                        if (possibleAttack & opponent_occupancy): 
                              self.pseudoMoves.append(Move(fromSquareIndex, possibleAttackIndex,1,0,0,0))
                              print(f"attack {piece} move from {self.indexToSquare(fromSquareIndex)} to {self.indexToSquare(possibleAttackIndex)}")
                        attacks = self.popBit(attacks, possibleAttackIndex)
      def isEmpty(self, square):
            if (self.all_pieces & (1 << square)): return False 
            else:  return True 
 
      def isAttacked(self, square): 
            if(self.white_pieces & (1<<square)): 
                  squareColor = chess.WHITE
                  oponnentColor = chess.BLACK

            elif(self.black_pieces & (1<<square)): 
                  squareColor = chess.BLACK
                  oponnentColor = chess.WHITE
            else: squareColor = -1
            if squareColor > -1: 
                  for move in self.pseudoMoves: 
                        if(( 1 << move.getFromSquare())&self.allPiecesTable[oponnentColor]): 
                              toSquare = move.getToSquare() 
                              if(toSquare == square): return True
                  return False 
            else: 
                  for move in self.pseudoMoves: 
                        toSquare = move.getToSquare()
                        if(toSquare == square): return True 
                  return False 

      def parseFEN(self, fen): # DO debugowania USUN POZNIEJ
              # 1. Reset all bitboards to 0
              self.white_pawns = self.white_knights = self.white_bishops = self.white_rooks = self.white_queen = self.white_king = 0
              self.black_pawns = self.black_knights = self.black_bishops = self.black_rooks = self.black_queen = self.black_king = 0

              # FEN strings have 6 parts separated by spaces.
              fen_parts = fen.split(' ')
              board_layout = fen_parts[0]
        
              # FEN starts at Rank 8 (index 7) and File A (index 0)
              rank = 7
              file = 0

              for char in board_layout:
                  if char == '/':
                      # Move down a rank and reset file to A
                      rank -= 1
                      file = 0
                  elif char.isdigit():
                      # Numbers represent empty squares, skip them
                      file += int(char)
                  else:
                      # Calculate the exact bit position and create a mask
                      square = rank * 8 + file
                      mask = 1 << square

                      # Map the character to the correct bitboard
                      if char == 'P': self.white_pawns |= mask
                      elif char == 'N': self.white_knights |= mask
                      elif char == 'B': self.white_bishops |= mask
                      elif char == 'R': self.white_rooks |= mask
                      elif char == 'Q': self.white_queen |= mask
                      elif char == 'K': self.white_king |= mask
                      elif char == 'p': self.black_pawns |= mask
                      elif char == 'n': self.black_knights |= mask
                      elif char == 'b': self.black_bishops |= mask
                      elif char == 'r': self.black_rooks |= mask
                      elif char == 'q': self.black_queen |= mask
                      elif char == 'k': self.black_king |= mask
                
                      # Move to the next square on the right
                      file += 1

              # 2. Update occupancy bitboards
              self.white_pieces = self.white_pawns | self.white_knights | self.white_bishops | self.white_rooks | self.white_queen | self.white_king
              self.black_pieces = self.black_pawns | self.black_knights | self.black_bishops | self.black_rooks | self.black_queen | self.black_king
              self.all_pieces = self.white_pieces | self.black_pieces

              self.piecesTable[chess.WHITE][0] = self.white_pawns
              self.piecesTable[chess.WHITE][1] = self.white_king
              self.piecesTable[chess.WHITE][2] = self.white_rooks
              self.piecesTable[chess.WHITE][3] = self.white_knights
              self.piecesTable[chess.WHITE][4] = self.white_bishops
              self.piecesTable[chess.WHITE][5] = self.white_queen

              self.piecesTable[chess.BLACK][0] = self.black_pawns
              self.piecesTable[chess.BLACK][1] = self.black_king
              self.piecesTable[chess.BLACK][2] = self.black_rooks
              self.piecesTable[chess.BLACK][3] = self.black_knights
              self.piecesTable[chess.BLACK][4] = self.black_bishops
              self.piecesTable[chess.BLACK][5] = self.black_queen

              self.allPiecesTable = [0]*2 
        
              for i in range(2):
                    for j in range(6): 
                          self.allPiecesTable[i] |= self.piecesTable[i][j]

              # 3. Parse En Passant Square
              # FEN index 3 holds the en passant target square (e.g., "f3" or "-")
              if len(fen_parts) > 3:
                  ep_str = fen_parts[3]
                  if ep_str == '-':
                      self.enPassantSquare = 0  # 0 indicates no en passant square
                  else:
                      # Convert algebraic notation (e.g. 'f3') to bitboard mask
                      ep_file = ord(ep_str[0]) - ord('a')   # 'a' -> 0, 'b' -> 1, ..., 'h' -> 7
                      ep_rank = int(ep_str[1]) - 1        # '1' -> 0, '2' -> 1, ..., '8' -> 7
                      ep_square_index = ep_rank * 8 + ep_file
                
                      self.enPassantSquare =  ep_square_index 
                      # Note: If your engine logic expects an integer index instead of a bitboard mask, 
                      # change the line above to: self.enPassantSquare = ep_square_index
              else:
                  self.enPassantSquare = 0                   
      def printBoard(self):  # DO debugowania USUN POZNIEJ 
                  print("   -----------------")
            
                  # Character map matching your piecesTable indices:
                  # 0: Pawns, 1: King, 2: Rooks, 3: Knights, 4: Bishops, 5: Queen
                  piece_chars = {
                        chess.WHITE: ['P', 'K', 'R', 'N', 'B', 'Q'],
                        chess.BLACK: ['p', 'k', 'r', 'n', 'b', 'q']
                  }

                  for rank in reversed(range(8)): 
                        rowString = f"{rank + 1} | "
                        for file in range(8): 
                              mask = 1 << (rank * 8 + file)
                              char_to_print = '.' # Default empty square
                        
                              # Only search for a piece if the square is occupied
                              if mask & self.all_pieces: 
                                    found = False
                                    for color in (chess.WHITE, chess.BLACK):
                                          for piece_idx in range(6):
                                                if mask & self.piecesTable[color][piece_idx]:
                                                      char_to_print = piece_chars[color][piece_idx]
                                                      found = True
                                                      break
                                          if found:
                                                break
                                          
                              rowString += char_to_print + " "
                        print(rowString) 
                  print("   -----------------")
                  print("    a b c d e f g h")
      
      
      
      def makeMove(self, move): 
            foundPiece = -1

            piecesTable = [self.piecesTable[0][:], self.piecesTable[1][:]]
            allPiecesTable = self.allPiecesTable[:]
            white_pieces = self.white_pieces
            black_pieces = self.black_pieces
            all_pieces = self.all_pieces
            copyPseudoMoves = self.pseudoMoves[:]  
            
            copyPiecesTable = [piecesTable[0][:], piecesTable[1][:]]

            if ( (1 << move.getFromSquare()) & allPiecesTable[chess.WHITE]):
                  color = chess.WHITE
                  opponentColor = chess.BLACK
            else:
                  color = chess.BLACK
                  opponentColor = chess.WHITE

            fromSquareBitboard = 1 << move.getFromSquare()
            for piecesIndex in range(len(piecesTable[0])):
                  if bool(fromSquareBitboard & piecesTable[color][piecesIndex]):
                        foundPiece = piecesIndex
                        break

            if foundPiece == -1:
                  return


            piecesTable[color][foundPiece] = game.popBit(piecesTable[color][foundPiece], move.getFromSquare())
            if (move.isPromotion()):
                        
                  chosenPiece = 3 # Zaimplementowac wybieranie z interfejsu
                  piecesTable[color][foundPiece] = game.insertBit(piecesTable[color][chosenPiece], move.getToSquare())
            else: 
                  piecesTable[color][foundPiece] = game.insertBit(piecesTable[color][foundPiece], move.getToSquare())

            if(move.isCastle()):
                  if move.getToSquare() == chess.SQUARES['g1']:
                        piecesTable[color][2] = game.popBit(piecesTable[color][2], chess.SQUARES['h1'])
                        piecesTable[color][2] = game.insertBit(piecesTable[color][2], chess.SQUARES['f1'])
                  elif move.getToSquare() == chess.SQUARES['c1']:
                        piecesTable[color][2] = game.popBit(piecesTable[color][2], chess.SQUARES['a1'])
                        piecesTable[color][2] = game.insertBit(piecesTable[color][2], chess.SQUARES['d1'])
                  elif move.getToSquare() == chess.SQUARES['g8']:
                        piecesTable[color][2] = game.popBit(piecesTable[color][2], chess.SQUARES['h8'])
                        piecesTable[color][2] = game.insertBit(piecesTable[color][2], chess.SQUARES['f8'])
                  elif move.getToSquare() == chess.SQUARES['c8']:
                        piecesTable[color][2] = game.popBit(piecesTable[color][2], chess.SQUARES['a8'])
                        piecesTable[color][2] = game.insertBit(piecesTable[color][2], chess.SQUARES['d8'])

            opponendFoundPiece = -1

            if(move.isCapture()):
                  for opponentPieceIndex in range(len(piecesTable[0])):
                        if bool( (1 << move.getToSquare()) & piecesTable[opponentColor][opponentPieceIndex]):
                              opponendFoundPiece = opponentPieceIndex
                              break
                  if (move.isEnPassant()):
                        if color == chess.WHITE:
                              piecesTable[opponentColor][0] = game.popBit(piecesTable[opponentColor][0], move.getToSquare() - 8)
                        else:
                              piecesTable[opponentColor][0] = game.popBit(piecesTable[opponentColor][0], move.getToSquare() + 8)
                  if (opponendFoundPiece != -1):
                        piecesTable[opponentColor][opponendFoundPiece] = game.popBit(piecesTable[opponentColor][opponendFoundPiece], move.getToSquare())

            self.enPassantSquare = 0
            if move.isDoublePush():
                  if color == chess.WHITE:
                        self.enPassantSquare = move.getToSquare() - 8
                  else:
                        self.enPassantSquare = move.getToSquare() + 8


            self.pseudoMoves = []
            self.piecesTable = piecesTable
            self.reconstructOccupancy()

            isEverythingOK =  not self.validate( color) 
            if isEverythingOK:
                  self.reconstructOccupancy()
            else:

                  self.piecesTable = copyPiecesTable
                  self.allPiecesTable = allPiecesTable
                  self.white_pieces = white_pieces
                  self.black_pieces = black_pieces
                  self.all_pieces = all_pieces
                  self.pseudoMoves = copyPseudoMoves
                  print("BAD MOVE ")


      def reconstructOccupancy(self):
             self.allPiecesTable = [0, 0]
             for i in range(2):
                      for j in range(6): 
                            self.allPiecesTable[i] |= self.piecesTable[i][j]
             self.white_pieces = self.allPiecesTable[chess.WHITE]
             self.black_pieces = self.allPiecesTable[chess.BLACK]
             self.all_pieces = self.white_pieces | self.black_pieces
            

      def validate(self, playerColor): 
            self.pseudoMoves = []
            for index in range(64): 
                  game.generateMoves(index)
            king = self.piecesTable[playerColor][1]
            kingIndex = self.getLSB(king)
            if(self.isAttacked(kingIndex)): 
                        return True
            return False
      def isCheckamte (self,playerColor): 
            pass

      # def mainGame(self): 
      #       currentPlayer = chess.WHITE
      #       while True: 
      #             game.printBoard()
      #             for index in range(64): 
      #                   self.generateMoves(index)
      #             inputFromSquare = input("Enter from square: ")
      #             inputToSquare = input("Enter to square : ")

      #             fromSquareIndex = chess.SQUARES[inputFromSquare]
      #             toSquareIndex = chess.SQUARES[inputToSquare]

      #             while ((1 << fromSquareIndex )& ~self.allPiecesTable[currentPlayer]):
      #                   inputFromSquare = input("Enter from square: ")
      #                   inputToSquare = input("Enter to square : ")
      #                   fromSquareIndex = chess.SQUARES[inputFromSquare]
      #                   toSquareIndex = chess.SQUARES[inputToSquare]



      #             for move in self.pseudoMoves: 
      #                   if move.getFromSquare() == fromSquareIndex and move.getToSquare() == toSquareIndex: 
      #                         self.makeMove(move)
      #                         break
      #             game.printBoard()
      #             currentPlayer  = (currentPlayer + 1) % 2


class Move: 
      def __init__(self, fromSquare, toSquare, capture, castle, double_push, promotion, enpassant=0):
            self.code = fromSquare | (toSquare << 6) | (capture << 12) | (castle << 13) | (double_push << 14) | (promotion << 15) | (enpassant << 16)
      def getToSquare(self): 
            return (self.code>>6) & 0x3F 
      def getFromSquare(self): 
            return self.code & 0x3F
      def isCapture(self): 
            if (self.code >> 12 & 1): return True 
            else: return False
      
      def isEnPassant(self): 
            if (self.code >> 16 &1): return True 
            else: return False 

      def isCastle(self): 
            if (self.code >> 13 &1): return True 
            else: return False
      def isDoublePush(self): 
            if (self.code >> 14 &1): return True 
            else: return False
      def isPromotion(self): 
            if ((self.code >> 15) & 1): return True 
            else: return False 
      
chess.SQUARES = chess.generateSquares()
chess.PAWN_ATTACKS = chess.generatePawnAttacks() 
chess.KNIGHT_ATTACKS = chess.generateKnightAttacks()
chess.POSITIVE_RAY_BITBOARDS = chess.generatePositiveRays()
chess.NEGATIVE_RAY_BITBOARDS = chess.generateNegativeRays()
chess.KING_ATTACKS = chess.generateKingAttacks()
game = chess() 
#game.printBoard()
#game.printBitBoard(chess.KNIGHT_ATTACKS[chess.SQUARES['e5']])
#print(chess.SQUARES['h8'])
#game.printBitBoard(chess.PAWN_ATTACKS[chess.BLACK][chess.SQUARES['h8']])
#game.printBitBoard(chess.NEGATIVE_RAY_BITBOARDS[0][chess.SQUARES['e5']])
#game.printBitBoard(chess.NEGATIVE_RAY_BITBOARDS[2][chess.SQUARES['e5']])

#game.printBitBoard(game.generateBishopAttacks(chess.SQUARES['e5']))/

#game.printBitBoard(game.generateQueenAttacks(chess.SQUARES['e5']))

#game.parseFEN("rnbqkbnr/ppppp1pp/8/8/4PPp1/8/PPPP3P/RNBQKBNR b KQkq f3 0 3")
#game.printBitBoard(game.generateBishopAttacks(chess.SQUARES['c8']))
#game.printBoard()
#game.printBitBoard(game.generateQueenAttacks(chess.SQUARES['e5']))
#game.printBitBoard(chess.NEGATIVE_RAY_BITBOARDS[3][chess.SQUARES['e5']])
#game.printBitBoard(chess.POSITIVE_RAY_BITBOARDS[2][chess.SQUARES['e5']])


#game.printBitBoard(chess.POSITIVE_RAY_BITBOARDS[0][chess.SQUARES['c8']])
#game.printBitBoard(game.generateBishopAttacks(chess.SQUARES["c8"]))
#for index in range(64): 
#      game.generateMoves(index)


# game.mainGame()