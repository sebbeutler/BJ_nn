import random
from XOR_task import *
from enum import Enum
import matplotlib.pyplot as plt
import time

class Actions(Enum):
    Stand = 'S'
    Hit = 'H'
    Split = 'SP'
    Double = 'DD'
    

class BlackJack:
    DECK = []
    def __init__(self):
        self.deckCount = 8
        self.drawnCards = []
        BlackJack.DECK = BlackJack.getStaticDeck()
        self.bank = 200
        self.deck = BlackJack.DECK * self.deckCount
        random.shuffle(self.deck)
        
        plt.close()
        plt.ion()
        plt.show()
        self.bankHistory = []
        self.bet = 1

    def run(self, agent, plot=True):
        self.bank -= self.bet
        
        if len(self.deck) < (len(BlackJack.DECK) * self.deckCount)/2:
            self.deck = BlackJack.DECK * self.deckCount
            random.shuffle(self.deck)
            # print("New Deck . . .")
                
        dealer_cards = []
        agent_cards = []

        # Initial Turn
        agent_cards.append(self.draw(self.deck))
        dealer_cards.append(self.draw(self.deck))
        agent_cards.append(self.draw(self.deck))
        dealer_cards.append(self.draw(self.deck))
        
        # print(f'Bank: {self.bank}')
        # print(f'Player hand: {agent_cards}')
        # print(f'Dealer hand: {dealer_cards}')

        # Player Dealing
        if BlackJack.countCards(agent_cards) == 21 and BlackJack.countCards(dealer_cards) == 21:
            self.bank += self.bet
            # print("Push Black Jack.")
            return
            
        
        choice = agent.input(agent_cards, dealer_cards[0])
        # print(f'Player chose to: {choice}')
        
        hand1 = hand2 = None
        
        if choice == Actions.Hit:
            while (BlackJack.countCards(agent_cards) < 21):
                agent_cards.append(self.draw(self.deck))
                # print(f'Player hand: {agent_cards}')
                if BlackJack.countCards(agent_cards) > 21:
                    break
                choice = agent.input(agent_cards, dealer_cards[0])
                # print(f'Player chose to: {choice}')
                if (choice != Actions.Hit):
                    break
        elif choice == Actions.Double:
            agent_cards.append(self.draw(self.deck))
            self.bank -= self.bet
            # print(f'Player hand: {agent_cards}')
        elif choice == Actions.Split and agent_cards[0][0] == agent_cards[1][0]:
            hand1 = [agent_cards[0], self.draw(self.deck)]
            hand2 = [agent_cards[1], self.draw(self.deck)]
            self.bank -= self.bet
            
            # print(f'Player hand1: {hand1}')
            choice = agent.input(hand1, dealer_cards[0])
            # print(f'Player chose to: {choice}')
            if choice == Actions.Hit:
                while (BlackJack.countCards(hand1) < 21):
                    hand1.append(self.draw(self.deck))
                    # print(f'Player hand1: {hand1}')
                    if BlackJack.countCards(hand1) > 21:
                        break
                    choice = agent.input(hand1, dealer_cards[0])
                    # print(f'Player chose to: {choice}')
                    if (choice != Actions.Hit):
                        break
            
            # print(f'Player hand2: {hand2}')
            choice = agent.input(hand2, dealer_cards[0])
            # print(f'Player chose to: {choice}')
            if choice == Actions.Hit:
                while (BlackJack.countCards(hand2) < 21):
                    hand2.append(self.draw(self.deck))
                    # print(f'Player hand2: {hand2}')
                    if BlackJack.countCards(hand2) > 21:
                        break
                    choice = agent.input(hand2, dealer_cards[0])
                    # print(f'Player chose to: {choice}')
                    if (choice != Actions.Hit):
                        break
        
        
        # DealerDealing
        while BlackJack.countCards(dealer_cards) < 17:
            dealer_cards.append(self.draw(self.deck))
            # print(f'Dealer hand: {dealer_cards}')
        
        # Final Count
        for hand in [agent_cards, hand1, hand2]:
            if hand == None:
                continue
            if len(hand) == 2 and hand1 == None and BlackJack.countCards(hand) == 21:
                # print("BLACK JACK !!!!")
                self.bank += self.bet*2.5
            elif BlackJack.countCards(hand) == BlackJack.countCards(dealer_cards):
                if choice == Actions.Double:
                    self.bank += self.bet
                self.bank += self.bet
            elif BlackJack.countCards(hand) > 21:
                ()
            elif BlackJack.countCards(hand) > BlackJack.countCards(dealer_cards):
                if choice == Actions.Double:
                    self.bank += self.bet*2
                self.bank += self.bet*2
            elif BlackJack.countCards(dealer_cards) > 21:
                if choice == Actions.Double:
                    self.bank += self.bet*2
                self.bank += self.bet*2
        
        # print(f'Final bank: {self.bank}')
        self.bankHistory.append(self.bank)
        if plot and len(self.bankHistory)%10 == 0:
            plt.xlim(0, max(300, len(self.bankHistory)+(1-((len(self.bankHistory)%300)/300))*300))
            plt.ylim(0, 300)
            plt.grid(True)
            plt.xlabel("matches played")
            plt.ylabel("bank")
            plt.plot(self.bankHistory, color='blue')
            plt.show()
            plt.pause(0.001)
    
    def countCards(cards):
        count = 0
        aces = 0
        for card in cards:
            if card[0] in "KQJT":
                count += 10
            elif card[0] in "23456789":
                count += int(card[0])
            elif card[0] == "A":
                aces += 1
        for i in range(aces):
            if count + 11 > 21:
                count += 1
            else:
                count += 11
        return count

    def draw(self, deck):
        card = deck.pop(0)
        self.drawnCards.append(card)
        return card

    def getStaticDeck():
        deck = []
        for card in "A23456789TJQK":
            for sign in "SCDH":
                deck.append(card + sign)
        return deck

class BasicAgent:
    def __init__(self) -> None:
        pass
    
    def input(self, agent_cards, dealer_card):
        # Table Strat
        for i in range(len(X)):
            c1 = BlackJack.countCards(agent_cards[0])
            c2 = BlackJack.countCards(agent_cards[1])
            row = BlackJack.countCards(dealer_card)
            
            if c1 == 11:
                c1 = 1
            if c2 == 11:
                c2 = 1
            if row == 11:
                row = 1

            if X[i][0] == c1 and X[i][1] == c2 and X[i][3] == row:
                if y[i] == [1, 0, 0, 0]:
                    return Actions.Stand
                elif y[i] == [0, 1, 0, 0]:
                    return Actions.Hit
                elif y[i] == [0, 0, 1, 0]:
                    return Actions.Split
                elif y[i] == [0, 0, 0, 1]:
                    return Actions.Double
                else:
                    assert False
        # print(f'Agent Cards: {agent_cards}')
        # print(f'Dealer Card: {dealer_card}')
        assert False
        
        # Dealer Strat
        #
        # if BlackJack.countCards(agent_cards) < 17:
        #     return Actions.Hit
        # else:
        #     return Actions.Stand
        
        # Manual Mode
        #
        # choice = input('>')
        # if choice == 'H':
        #     return Actions.Hit
        # elif choice == 'S':
        #     return Actions.Stand
        # elif choice == 'SP':
        #     return Actions.Split
        # elif choice == 'DD':
        #     return Actions.Double
        # else:
        #     print(f'Action "{choice}" not found.')
        #     return Actions.Stand
        
        
if __name__ == '__main__':
    bj = BlackJack()
    agent = BasicAgent()
    
    while bj.bank > 0:
        bj.run(agent)
    
    plt.pause(0)