#Card Values and inputs for card class
from IPython.display import clear_output
import random

#Tuples of names of suits
suits = ('Hearts', 'Diamond', 'Spades', 'Clubs')

#Tuples of names of rank of cards
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

#Dictionary that assigns a rank to a integer value
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace': 11}

playing = True

#Card class
class Card:
    '''
    Create a Card object. Takes suit and rank. Each rank has a assigned value
    '''
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __str__(self):
        return self.rank + " of " + self.suit

#Deck class
class Deck:
    '''
    Creates a deck by storing 52 unique card instances
    '''
    
    def __init__(self):
        #An array to hold card objects
        self.all_cards = []
        
        #Create a deck of 52 unique cards
        for suit in suits:
            for rank in ranks:
                #Create the card object
                created_card = Card(suit, rank)
                
                self.all_cards.append(created_card)
    
    #Shuffle the given deck
    def shuffle(self):
        random.shuffle(self.all_cards)
        
    #Remove the last card from the deck    
    def deal_one(self):
        return self.all_cards.pop()


class Hand:
    '''
    A hand object can hold cards, adjust hand value by considering aces.
    '''
    
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        
    #Adds a card to the hand, each time a card is added, the hand value is calculated    
    def add_card(self, new_card):
        self.value = 0
        self.cards.append(new_card)
        for i in range(len(self.cards)):
            self.value += self.cards[i].value
    
    #Function reduces the value of an ace by 10 making it 1
    def adjust_for_ace(self):
        self.value = self.value - (self.aces*10)

class Chips:
    '''
    Holds players chips and their current bets
    '''
    
    def __init__(self):     
        self.total = 100
        self.bet = 0
    
    #Once player wins bet, the bet is doubled and added to the total
    def win_bet(self):
        self.total += 2 * self.bet
        self.bet = 0
    
    #If a player loses, bet is reset.
    def lose_bet(self):
        self.bet = 0

def take_bet(bankroll):
        '''
        Takes in a user input of how much bet they would like to place 
        If user input is less than their available chips
        Or their input is an invalid input then you get an error message
        The bet is deducted from the bankroll
        '''

        while True:
            try:
                bet = int(input('How much bet would you like to place? '))
                
                if bet > bankroll.total:
                    print('You do not have enough chips')
                    continue
                elif bet <= 0:
                    print("Please enter a valid amount")
                else:
                    bankroll.total -= bet
                    return bet
                    break
            except:
                print('Invalid input, please enter a number')
                continue

def hit(deck, hand):
    
    #Draws a card from the deck and adds it to hand
    hand.add_card(deck.deal_one())
    
    #reset the number of aces
    hand.aces = 0
    
    #count for aces in hand
    for i in range(len(hand.cards)):
            if hand.cards[i].rank == 'Ace':
                hand.aces += 1

    #Adjust for ace if hand value is above 21
    if hand.value > 21 and hand.aces >= 1:
        hand.adjust_for_ace()
        
def show_some(player, dealer):
    
    clear_output()
    
    #PRINT THE PLAYERS CARD AND DEALERS CARDS. DEALERS FIRST CARD IS HIDDEN
    print("Player's hand:\n")
    for i in range(len(player.cards)):
        print(f'{player.cards[i]}')
        
    print("\nDealers hand:")
    print("A hidden card")
    for i in range(len(dealer.cards)):
        if i == 0:
            continue
        else:
            print(dealer.cards[i])

def show_all(player, dealer):
    
    clear_output()
    
    #PRINT BOTH PLAYERS CARDS AND DEALERS CARD FULLY
    print("Player's hand:")
    
    for i in range(len(player.cards)):
        print(f'{player.cards[i]}')
        
    print("\nDealers hand:")
    for i in range(len(dealer.cards)):
        print(f'{dealer.cards[i]}')

def hit_or_stand(deck, player_hand, dealer_hand):
    '''
    TAKES INPUT FROM USER TO EITHER HIT OR STAY
    IF HIT, THE PLAYER IS DEALT A CARD FROM THE DECK
    AFTER HITTING IF PLAYERS CARD IS OVER 21 THE PLAYER BUSTS
    IF STAY, PLAYING = FALSE
    '''
    
    global playing
    
    while True:
            try:
                decision = input('Would you like to hit or stay? ')
                decision = decision.lower()
                
                if decision == 'hit':
                    hit(deck, player_hand)
                    show_some(player_hand, dealer_hand)
                    if player_hand.value > 21:
                        break
                elif decision == 'stay':
                    playing = False
                    break
                else:
                    print("Invalid entry, please input either hit or stay")
                    continue
            except:
                print('Invalid entry')
                continue

def player_busts(player_chips):
    
    #RESET BET WHEN PLAYER BUSTS
    player_chips.lose_bet()
    print('\nYou have busted')
    return True

def player_wins(player_chips):

    #PLAYER WINS BET AND BET IS ADDED TO THE TOTAL
    player_chips.win_bet()
    print('\nYou win')
    
def dealer_busts(player_chips):
    
    #PLAYER WINS THE BET
    player_chips.win_bet()
    print('\nDealer has busted')
    
def dealer_wins(player_chips):
    
    #PLAYER LOSES BET
    player_chips.lose_bet()
    print('\nDealer wins')
    
def push(player_chips):
    
    #THE GAME TIES, PLAYER IS REFUNDED THE BET
    player_chips.total += player_chips.bet
    player_chips.lose_bet()
    print('\nIts a tie')

#Set up players chips
players_chips = Chips()
keep_playing = True

while keep_playing:
    clear_output()
    print("Welcome to Blackjack")
    print(f"You have {players_chips.total} chips")
    
    #Create the deck and shuffle and deal two cards to each player
    deck = Deck()
    
    #Shuffle deck
    deck.shuffle()
    
    #Create hands
    players_hand = Hand()
    dealers_hand = Hand()
    
    player_bust = False
    
    #Deal two cards to each player
    for i in range(4):
        if i%2 == 0:
            players_hand.add_card(deck.deal_one())
        else:
            dealers_hand.add_card(deck.deal_one())
    
    #Place bet
    players_chips.bet = take_bet(players_chips)
        
    #Show Cards
    show_some(players_hand, dealers_hand)
    
    while playing:
        #Hit or stand
        hit_or_stand(deck, players_hand, dealers_hand)
        
        #Show some cards
        show_some(players_hand, dealers_hand)
        
        #Condition for bust
        
        #If player busts, the variable becomes True
        if players_hand.value > 21:
            player_bust = player_busts(players_chips)
            break
    
    #If player didn't bust
    #Dealer hits until it reaches 17 and stops if it is between 17 to 21
    if player_bust == False:
        while dealers_hand.value < 17:
            dealers_hand.add_card(deck.deal_one())
            
        show_all(players_hand, dealers_hand)
        
        #Endgame scenarios
        if dealers_hand.value > 21:
            dealer_busts(players_chips)
        elif dealers_hand.value > players_hand.value:
            dealer_wins(players_chips)
        elif dealers_hand.value < players_hand.value:
            player_wins(players_chips)
        else:
            push(players_chips)
    
    
    print(f'Your chip balance: {players_chips.total}')
    
    #If player has no chips remaining, end the game
    #else as the player if they want to replay
    while True:
        try:
            if players_chips.total == 0:
                print('You have no chips remaining')
                print('Game over')
                keep_playing = False
                break
            
            else:
                play_again = input("Would you like to play again? ")
                play_again = play_again.lower()
                
                if play_again == 'yes':
                    playing = True
                    break
                elif play_again == 'no':
                    keep_playing = False
                    break
                else:
                    print('Invalid input, please input either yes or no')
        except:
            print('Invalid input, please input either yes or no')