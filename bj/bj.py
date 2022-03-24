import random
import time

suit = ['d','h','c','s']

#カード生成
class Deck():
    def __init__(self):
        self.cards = [[i,j] for i in range(1,14) for j in suit]
        random.shuffle(self.cards)
    def emission(self):
        print(f'deck{self.cards}')
        emission_card = self.cards.pop()
        print(f'emission{emission_card}')
        return emission_card

#絵札変換
def str_point(cards):
    #dealerのカードが1枚の時、card[0]が存在しないため
    if type(cards) is int:
        card = cards
    elif type(cards) is list:
        card = cards[0]
    else:
        #suitが来てしまうので、適当に1を返す
        return 0
    if card > 10:
        return 10
    elif card == 1:
        return 11
    else:
        return card

#point計算
def count_point(cards):
    #カードの数字をポイントに直した1次元リスト リストの合計が得点
    point = [str_point(c) for c in cards]
    #Aを1か11としてカウント
    cnt = point.count(11)
    point_sum = sum(point)
    if cnt > 1 and point_sum > 21:
        for i in range(cnt):
            point_sum -= 10
            if point_sum <= 21:
                break        
    return point_sum

#プレイヤー作成
class Player():
    def __init__(self):
        #手札ホルダーに2枚セット
        self.cards = []
    
    def draw(self,card):
        self.cards.append(card)

def game(deck):
    player = Player()
    player.card_open()
    player.point_open()

    select = 0

    while count_point(player.cards) <= 21:
        time.sleep(1)

        if count_point(player.cards) == 21:
            print('BJ')
            return 1
        
        select = input('カードを引きますか？ yes:1')
        if select == '1':
            player.draw()
            player.card_open()
            player.point_open()
        else:
            break
    else:
        print("Burst!")
        return 0

start = 1
win_lose = [0,0]


    






