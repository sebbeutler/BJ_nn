import random

class BlackJack:
    DECK = []
    def __init__(self):
        self.deckCount = 8
        self.drawnCards = []
        BlackJack.DECK = BlackJack.getStaticDeck()

    def run(self, agent, matches=1):
        deck = self.deckCount = BlackJack.DECK * self.deckCount
        random.shuffle(deck)
        dealer_cards = []
        agent_cards = []

        # Initial Turn
        agent_cards.append(self.draw(deck))
        dealer_cards.append(self.draw(deck))
        agent_cards.append(self.draw(deck))
        dealer_cards.append(self.draw(deck))

        # Player Dealing

        choice = agent.input(agent_cards, dealer_cards)

        if choice == "Hit":
            while (BlackJack.countCards(agent_cards) < 21):
                agent_cards.append(self.draw(deck))
                choice = agent.input(agent_cards, dealer_cards)
                if (choice != "Hit"):
                    break
        elif choice == "Double":
            agent_cards.append(self.draw(deck))
        elif choice == "Split" and agent_cards[0][0] == agent_cards[1][0]:
            hand1 = [agent_cards[0], agent_cards.append(self.draw(deck))]
            hand2 = [agent_cards[1], agent_cards.append(self.draw(deck))]

            choice = agent.input(agent_cards, dealer_cards)
            if choice == "Hit":
                while (BlackJack.countCards(hand1) < 21):
                    hand1.append(self.draw(deck))
                    choice = agent.input(hand1, dealer_cards)
                    if (choice != "Hit"):
                        break

            choice = agent.input(hand2, dealer_cards)
            if choice == "Hit":
                while (BlackJack.countCards(hand2) < 21):
                    hand2.append(self.draw(deck))
                    choice = agent.input(hand2, dealer_cards)
                    if (choice != "Hit"):
                        break
         # DealerDealing

    
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

if __name__ == '__main__':
    bj = BlackJack()

    bj.run(None)