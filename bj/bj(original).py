import random
import time

suit = ['d','h','c','s']

#カード生成
class Deck:
    def __init__(self):
        self.cards = [[i,j] for i in range(1,14) for j in suit]

        random.shuffle(self.cards)
    
    def emmision(self):
        emission_card = self.cards.pop()
        return emission_card

#deck = Deck()
# print(ins.cards)
# print(ins.emmision())
# print(ins.emmision())
# print(ins.emmision())

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
        card = deck.emmision()
        self.cards.append(card)
        card = deck.emmision()
        self.cards.append(card)

    def card_open(self):
        print('PL:',self.cards)

    def point_open(self):
        print('PL:',count_point(self.cards))
    
    def draw(self):
        card = deck.emmision()
        self.cards.append(card)

#Playerと挙動が似ているのでクラスを継承
class Deerer(Player):
    def card_open(self):
        print('DR:',self.cards)

    def point_open(self):
        print('DR:',count_point(self.cards))

    def card_close(self):
        print('DR:',self.cards[0],"[*,*]")

    def point_close(self):
        print('DR:',str_point(self.cards[0]))

def game(deck):
    player = Player()
    player.card_open()
    player.point_open()

    deerer = Deerer()
    deerer.card_close()
    deerer.point_close()

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
    
    time.sleep(1)

    deerer.card_open()
    time.sleep(1)
    deerer.point_open()
    
    while count_point(deerer.cards) < 16:
        time.sleep(1)
        deerer.draw()
        deerer.card_open()
        time.sleep(1)
        deerer.point_open()
        time.sleep(1)

        if count_point(deerer.cards) > 21:
            print('Burst')
            return 1
    
    if count_point(player.cards) > count_point(deerer.cards):
        return 1
    elif count_point(player.cards) < count_point(deerer.cards):
        return 0
    else:
        return -1

start = 1
win_lose = [0,0]

deck = Deck()

while(len(deck.cards)) > 10:
    start = input('ゲームを始めますか？ y:1')
    if start != '1':
        print("fin.")
        break
    print('Start game')
    result = game(deck)
    if result == 1:
        win_lose[0] += 1
        print(f'You win. win:{win_lose[0]} lose:{win_lose[1]}')
    elif result == 0:
        win_lose[1] += 1
        print(f'You lose. win:{win_lose[0]} lose:{win_lose[1]}')
    else:
        print("ドロー")

else:
    print('カードがなくなりました。')


    






