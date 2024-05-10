from copy import deepcopy
import random
import sys

from constraint import*

def makeRandomMove(validMoves):
    i = random.randint(0,len(validMoves)-1)
    return validMoves[i]


def selectRandomPromote(defaultPromote = None):
    if defaultPromote is None:
        return random.choice(['q','n','r','b'])
    return defaultPromote

def evaluateScore(gameState):
    if gameState.checkMate:
        if gameState.whiteToMove:
            return -CHECKMATE
        else: 
            return CHECKMATE
    
    elif gameState.staleMate:
        return STALEMATE
    
    score = 0 # score of state

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            positionScore = 0
            chessCell = gameState.board[row][col]

            if chessCell == '--':
                continue

            if not gameState.whiteToMove and chessCell[0] == 'w':
                if chessCell[1] == 'p':
                    positionScore = PIECE_POSITIONS_SCORE['wp'][row][col] * WEIGHT_SCORE['p']

                elif chessCell[1] != 'k':
                    positionScore = PIECE_POSITIONS_SCORE[chessCell[1]][row][col] * WEIGHT_SCORE[chessCell[1]]

                score += PIECESCORE[chessCell[1]]*(1 + positionScore)

            elif gameState.whiteToMove and chessCell[0] == 'b':
                if chessCell[1] == 'p':
                    positionScore = PIECE_POSITIONS_SCORE['bp'][row][col] * WEIGHT_SCORE['p']

                elif chessCell[1] != 'k':
                    positionScore = PIECE_POSITIONS_SCORE[chessCell[1]][row][col] * WEIGHT_SCORE[chessCell[1]]

                score -= PIECESCORE[chessCell[1]]*(1 + positionScore)
    
    return score


def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves) # Shuffle all valid moves to make them random
    findMoveMinimax(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)

    return nextMove

def findMoveMinimax(gameState, validMoves, depth, alpha, beta, turn):
    global nextMove
    
    if depth == 0:
        return turn * evaluateScore(gameState)
    
    maximumScore = -CHECKMATE    
    
        
    for move in validMoves:

        if move.isPromote:
            move.promoteTo=makeRandomMove('q')

        localGameState = deepcopy(gameState)
        localGameState.makeMove(validMoves[0])

        nextMoves = localGameState.getValidMoves()
        score = -findMoveMinimax(localGameState, nextMoves, depth -1, -beta, -alpha, -turn)

        if score > maximumScore:
            score = maximumScore
            if depth == DEPTH:
                nextMove = move   

        if maximumScore > alpha:
            alpha = maximumScore
        if alpha >= beta:
            break   

    return score
            

            



            
    