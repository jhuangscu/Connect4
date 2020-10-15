import tweepy
import time
from copy import deepcopy
import sys


auth = tweepy.OAuthHandler("8t8aBsAwHNdjfqcmjNCdJLYvh", "0qA3NPWldJ7WDVRsdkMJWBJZeUAtrmQ0Kj9GJOlAm8BzNdo1BB");
auth.set_access_token("1263961271923142656-qw0BrZtApT7b9jK0BeOK8fdoEVlxkK", "1dgQemuT15wAlyvC2OZyD9SVr0HMvIS8VUrI2rH5l6JgA");
api = tweepy.API(auth, wait_on_rate_limit=True)

mentions = api.mentions_timeline()

FILE_NAME = 'last_seen_id.txt'

def printBoard(board):
    printedboard = ""
    for row in board:
        for i in row:
            printedboard += i + '   '
        printedboard += '\n'

    return printedboard

xends = {-1 : -1, 1 : 7}
yends = {-1 : -1, 1 : 6}

def isWin(board, x, y, player):
    directionPairs = [(1,0),(0,1),(1,1),(-1,1)]
    for dx,dy in directionPairs:
        firstDirection = 0
        if dx == 0:
            xiter = [x for _ in range(7)]
        else:
            xiter = range(x + dx, xends[dx], dx)
        if dy == 0:
            yiter = [y for _ in range(7)]
        else:
            yiter = range(y + dy, yends[dy], dy)
        for xi,yj in zip(xiter,yiter):
            if board[yj][xi] == player:
                firstDirection+=1
            else:
                break
        secondDirection = 0
        if dx == 0:
            xiter = [x for _ in range(7)]
        else:
            xiter = range(x - dx, xends[-dx], -dx)
        if dy == 0:
            yiter = [y for _ in range(7)]
        else:
            yiter = range(y - dy, yends[-dy], -dy)
        for xi,yj in zip(xiter,yiter):
            if board[yj][xi] == player:
                secondDirection+=1
            else:
                break
        if secondDirection+firstDirection >= 3:
            return 1
    return 0

def distanceFromBottom(board, column):
    d = 0
    for i in range(5, -1, -1):
        if board[i][column] != '-':
            d += 1
        else:
            break
    return d

def rateBoard(board):
    numberOfWinsX = 0
    for row in range(6):
        for column in range(7):
            if board[row][column] == '-':
                d = distanceFromBottom(board, column)
                numberOfWinsX += isWin(board, column, row, 'X') * (0.8 ** (5 - row - d))
    numberOfWinsO = 0
    for row in range(6):
        for column in range(7):
            if board[row][column] == '-':
                d = distanceFromBottom(board, column)
                numberOfWinsO += isWin(board, column, row, 'O') * 4 * (0.8 ** (5 - row - d))
    return numberOfWinsX - numberOfWinsO

def recursivelyPickAiSpot(board, iterations, turn):
    if turn == 'X':
        turn = 'O'
    else:
        turn = 'X'
    if iterations <= 0:
        return rateBoard(board)
    avg = 0
    for column in range(7):
        boardCopy = deepcopy(board)
        r,c = 5 - distanceFromBottom(board, column),column
        if turn == 'O' and isWin(boardCopy, c, r, 'O'):
            return -4
        elif turn == 'X' and isWin(boardCopy, c, r, 'X'):
            return 1
        boardCopy[r][c] = turn
        avg += recursivelyPickAiSpot(boardCopy, iterations - 1, turn)
    avg /= 7
    return avg

def pickAiSpot(board, iterations):
    for column in range(7):
        r,c = 5 - distanceFromBottom(board, column),column
        if board[r][c] == '-' and isWin(board, c, r, 'X'):
            return column
    for column in range(7):
        r,c = 5 - distanceFromBottom(board,column),column
        if board[r][c] == '-' and isWin(board, c, r, 'O'):
            return column
    plays = [0 for i in range(7)]
    for column in range(7):
        boardCopy = [row[:] for row in board]
        r,c = 5 - distanceFromBottom(board, column),column
        if r < 0:
            plays[column] = -100000
        else:
            boardCopy[r][c] = 'X'
            plays[column] =  recursivelyPickAiSpot(boardCopy, iterations - 1, 'O')

    for column in range(7):
        boardCopy = [row[:] for row in board]
        r,c = 5 - distanceFromBottom(board, column),column
        if r > 0:
            boardCopy[r][c] = 'X'
            if isWin(boardCopy, c, r - 1, 'O'):
                plays[column] = -10000

    p = plays.copy()
    p.sort()
    return plays.index(p[-1])

def retrieve_last_seen_id(file_name):
  f_read = open(file_name, 'r')
  last_seen_id = int(f_read.read().strip())
  f_read.close()
  return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
  f_write = open(file_name, 'w')
  f_write.write(str(last_seen_id))
  f_write.close()
  return

def reply_to_tweets():
  print('retrieving and replying to tweets...', flush=True)
  last_seen_id = retrieve_last_seen_id(FILE_NAME)
  mentions = api.mentions_timeline(
                      last_seen_id,
                      tweet_mode='extended')

tweets = reversed(mentions)
last_seen_name = ''
for mention in tweets:
  print(str(mention.id) + ' - ' + mention.text, flush=True)
  last_seen_id = mention.id
  count = 0
  line = store_last_seen_id(last_seen_id, FILE_NAME)
  print('found game!', flush=True)
  print('responding back...', flush=True)
  if last_seen_name != mention.user.screen_name:
      board = [['-' for i in range(7)] for j in range(6)]
      winner = None
  if '0' in mention.text.lower():
      i = '0'
  elif '1'in mention.text.lower():
      i = '1'
  elif '2' in mention.text.lower():
      i = '2'
  elif '3' in mention.text.lower():
      i = '3'
  elif '4' in mention.text.lower():
      i = '4'
  elif '5' in mention.text.lower():
      i = '5'
  elif '6' in mention.text.lower():
      i = '6'
  column = int(i[0])
  r,c = 5 - distanceFromBottom(board, column),column
  if isWin(board,c,r,'O'):
      winner = "O"
  board[5 - distanceFromBottom(board, column)][column] = 'O'
  if winner != None:
      break
  column = pickAiSpot(board[:], 5)
  r,c = 5 - distanceFromBottom(board, column),column
  if isWin(board,c,r,'X'):
      winner = "X"
  board[r][c] = 'X'
  try:
      print(line)
      if line != '\n':
          last_seen_name = mention.user.screen_name
          api.update_status('@' + mention.user.screen_name + '\n 0   1   2   3   4   5   6\n' + printBoard(board), in_reply_to_status_id = mention.id , auto_populate_reply_metadata=True)
      else:
          pass
  except tweepy.TweepError as e:
      print(e.reason)

if(winner == "0"):
  try:
      print(line)
      if line != '\n':
          api.update_status('@' + mention.user.screen_name +  '\n 0   1   2   3   4   5   6\n' + printBoard(board) + '\n You win!', mention.id)
          last_seen_name = ''
      else:
          pass
  except tweepy.TweepError as e:
      print(e.reason)
elif(winner == "X"):
  try:
      print(line)
      if line != '\n':
          api.update_status('@' + mention.user.screen_name + '\n 0   1   2   3   4   5   6\n' + printBoard(board) + ' Better luck next time!', mention.id)
          last_seen_name = ''
      else:
          pass
  except tweepy.TweepError as e:
      print(e.reason)

while True:
  reply_to_tweets()
  time.sleep(15)
