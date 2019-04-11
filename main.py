from models.trump import PokerPlayer, Deck

def main():
    print('Poker Game Start.')
    player1 = PokerPlayer()
    deck = Deck()
    deck.shuffle()
    for i in range(5):
        c = deck.draw()
        player1.append(c)
    e = player1.evaluate()
    print(player1.pokerplayer)
    print(e)
    print('捨てるカードの番号をスペース区切りで入力してください')
    s = input()
    player1.discard(list(map(int, s.split())))
    for i in range(5 - len(player1)):
        c = deck.draw()
        player1.append(c)
    e = player1.evaluate()
    print(player1.pokerplayer)

    print('捨てるカードの番号をスペース区切りで入力してください')
    s = input()
    player1.discard(list(map(int, s.split())))
    for i in range(5 - len(player1)):
        c = deck.draw()
        player1.append(c)
    e = player1.evaluate()
    print(player1.pokerplayer)
    print(e)


if __name__ == '__main__':
    main()