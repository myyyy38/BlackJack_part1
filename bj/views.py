from django.shortcuts import render
from . import bj
# Create your views here.

def card_path(cards):
    path = []
    for card in cards:
        path.append(str(card[1])+str(card[0])+'.png')
    return path


def game(request):
    if request.method == 'GET' or 'restart' in request.POST :
        print('ゲーム開始')
        #ゲームの終了判定
        game_flag = False
        #ターン判定
        player_turn = True

        deck = bj.Deck()
        player = bj.Player()
        dealer = bj.Player()

        player.cards = [deck.emission(),deck.emission()]
        dealer.cards = [deck.emission(),deck.emission()]
        print(dealer.cards)

        #セッションに記録して、ボタンを押しても内容が更新されないようにする ボタンを押す度必要
        request.session['deck'] = deck
        request.session['player'] = player
        request.session['dealer'] = dealer
        request.session['player_turn'] = player_turn
        request.session['game_flag'] = game_flag

        d = {
            "message":"はじめましょう",
            "dealer_card":["u0.png","u0.png"],
            "player_card":["u0.png","u0.png"],
            "player_point":0,
            "dealer_point":0,
        }

        return render(request,'bj/game.html',d)

    elif request.method == 'POST':
        game_flag = request.session["game_flag"]
        player_turn = request.session["player_turn"]
        deck = request.session["deck"]
        player = request.session["player"]
        dealer = request.session["dealer"]

        if "hit" in request.POST:
            player.draw(deck.emission())
        elif "stand" in request.POST:
            player_turn = False
        elif "restart" in request.POST:
            request.session.clear()
    
        
        if bj.count_point(player.cards) > 21:
            game_flag = True
        elif bj.count_point(dealer.cards) > 16 and player_turn == False:
            game_flag = True

        if not game_flag:
            if player_turn:
                print(f'player.cards{player.cards}')
                player_point  = bj.count_point(player.cards)
                print(f'dealer.cards[0]{dealer.cards[0]}')
                dealer_point  = bj.count_point(dealer.cards[0])

                dealer_close = [[""],["0","u"]]
                dealer_close[0] = dealer.cards[0]

                if player_point == 21:
                    player_turn = False
                    request.session['deck'] = deck
                    request.session['player'] = player
                    request.session['dealer'] = dealer
                    request.session['player_turn'] = player_turn
                    request.session['game_flag'] = game_flag

                    d = {
                        "message":"BJ",
                        "dealer_card":card_path(dealer_close),
                        "player_card":card_path(player.cards),
                        "player_point":player_point,
                        "dealer_point":dealer_point,
                        "turn":player_turn,
                        "flag":game_flag,
                    }
                    return render(request,'bj/game.html',d)
                
                else:
                    request.session['deck'] = deck
                    request.session['player'] = player
                    request.session['dealer'] = dealer
                    request.session['player_turn'] = player_turn
                    request.session['game_flag'] = game_flag
                    d = {
                        "message":"カードを引きますか",
                        "dealer_card":card_path(dealer_close),
                        "player_card":card_path(player.cards),
                        "player_point":player_point,
                        "dealer_point":dealer_point,
                        "turn":player_turn,
                        "flag":game_flag,
                    }
                    return render(request,'bj/game.html',d)
            #dealerのターン
            else:
                dealer.draw(deck.emission())
                player_point  = bj.count_point(player.cards)
                dealer_point  = bj.count_point(dealer.cards)
                
                player_turn = False
                request.session['deck'] = deck
                request.session['player'] = player
                request.session['dealer'] = dealer
                request.session['player_turn'] = player_turn
                request.session['game_flag'] = game_flag

                d = {
                    "message":"ディーラーがカードを引きました",
                    "dealer_card":card_path(dealer.cards),
                    "player_card":card_path(player.cards),
                    "player_point":player_point,
                    "dealer_point":dealer_point,
                    "flag":game_flag,
                }
                return render(request,'bj/game.html',d)
        else:
            player_point  = bj.count_point(player.cards)
            dealer_point  = bj.count_point(dealer.cards)

            player_turn = False
            game_flag = True

            if player_point > 21:
                msg = "you lose!"

            elif player_point < 21 and dealer_point > 21:
                 msg = "you Win!"

            elif player_point > dealer_point:
                msg = "you win!"

            elif player_point == dealer_point:
                msg = "引き分け"
            
            else:
                msg = "you lose!"
            
            d = {
                "message":msg,
                "dealer_card":card_path(dealer.cards),
                "player_card":card_path(player.cards),
                "player_point":player_point,
                "dealer_point":dealer_point,
                "flag":game_flag,
            }
            return render(request,'bj/game.html',d)

    return render(request,'bj/game.html')