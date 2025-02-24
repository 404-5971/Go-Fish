import time
import random

class Player:
    def __init__(self, name):
        self.hand = []
        self.books = 0
        self.name = name
        self.is_human = True
        self.is_turn = False
        self.is_winner = False
    def take_turn(self):
        print("It's your turn!")
        print("Your current hand:")
        for card in self.hand:
            print(card)
            time.sleep(0.1)
        print("Which card would you like to ask for?")
        while True:
            card = input("> ").strip().lower()
            if not card:
                print("Please enter a card value (2-10, Jack, Queen, King, or Ace)")
                continue
            
            valid_cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 
                  'jack', 'queen', 'king', 'ace']
            
            # Handle common variations
            if card in ['q', 'queen']:
                card = 'queen'
            elif card in ['k', 'king']:
                card = 'king'
            elif card in ['j', 'jack']:
                card = 'jack'
            elif card in ['a', 'ace']:
                card = 'ace'
            elif card.isdigit() and int(card) >= 2 and int(card) <= 10:
                card = card
            else:
                print("Please enter a valid card value (2-10, Jack, Queen, King, or Ace)")
                continue

            # Check if player has the card
            if not any(card in c.lower() for c in self.hand):
                print("You don't have that card in your hand. Try again.")
                continue
            
            card = card.capitalize()
            break

        print(f"You asked for the {card}.")
        time.sleep(0.3)
        print("Who would you like to ask? (Enter their name)")
        while True:
            player_name = input("> ").strip()
            target_player = None
            for player in [BOT1, BOT2, BOT3]:
                if player.name.lower() == player_name.lower():
                    target_player = player
                    break
            if target_player:
                break
            print(f"That player doesn't exist. Please ask {BOT1.name}, {BOT2.name}, or {BOT3.name}")

        print(f"You asked {target_player.name} for a {card}.")
        time.sleep(0.3)

        # Check if the target player has the requested card
        matching_cards = [c for c in target_player.hand if card.lower() in c.lower()]
        if matching_cards:
            print(f"{target_player.name} has {len(matching_cards)} {card}{'s' if len(matching_cards) > 1 else ''}!")
            for match in matching_cards:
                target_player.hand.remove(match)
                self.hand.append(match)
                time.sleep(0.3)
        else:
            print(f"{target_player.name} doesn't have a {card}.")
            time.sleep(0.3)
            print("Go fish!")
            if MAIN_DECK.cards:
                drawn_card = MAIN_DECK.cards.pop()
                self.hand.append(drawn_card)
                print(f"You drew the {drawn_card}")
            else:
                print("The deck is empty!")
                time.sleep(1)

    def check_books(self):
        rank_counts = {}
        for card in self.hand:
            rank = card.split(' of ')[0].lower()
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
        
        for rank, count in rank_counts.items():
            if count == 4:
                print(f"You got a book of {rank}s!")
                self.books += 1
                self.hand = [c for c in self.hand if rank.lower() not in c.lower()]

class Bot:
    def __init__(self, name):
        self.hand = []
        self.books = 0
        self.name = name
        self.is_human = False
        self.is_turn = False
        self.is_winner = False
    def take_turn(self):
        print(f"It's {self.name}'s turn!")
        # Count occurrences of each rank in hand
        rank_counts = {}
        for card in self.hand:
            rank = card.split(' of ')[0].lower()
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
        
        if not rank_counts:
            return  # Empty hand

        # Find the ranks with maximum count
        max_count = max(rank_counts.values())
        max_ranks = [rank for rank, count in rank_counts.items() if count == max_count]
        
        # Choose random rank from those with max count
        chosen_rank = random.choice(max_ranks)
        
        # Choose random player to ask
        possible_targets = [p for p in [PLAYER, BOT1, BOT2, BOT3] if p != self and p.hand]
        if not possible_targets:
            return
        
        target_player = random.choice(possible_targets)
        
        print(f"{self.name} asks {target_player.name} for a {chosen_rank}")
        time.sleep(0.3)
        
        # Check if target has matching cards
        matching_cards = [c for c in target_player.hand if chosen_rank.lower() in c.lower()]
        if matching_cards:
            print(f"{target_player.name} has {len(matching_cards)} {chosen_rank}{'s' if len(matching_cards) > 1 else ''}!")
            for match in matching_cards:
                target_player.hand.remove(match)
                self.hand.append(match)
                time.sleep(0.3)
        else:
            print(f"{target_player.name} doesn't have a {chosen_rank}")
            print(f"{self.name} goes fish!")
            if MAIN_DECK.cards:
                drawn_card = MAIN_DECK.cards.pop()
                self.hand.append(drawn_card)
                time.sleep(0.3)
    
    def check_books(self):
        rank_counts = {}
        for card in self.hand:
            rank = card.split(' of ')[0].lower()
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
        
        for rank, count in rank_counts.items():
            if count == 4:
                print(f"{self.name} got a book of {rank}s!")
                self.books += 1
                self.hand = [c for c in self.hand if rank.lower() not in c.lower()]

class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for suit in suits:
            for rank in ranks:
                self.cards.append(f"{rank} of {suit}")

def get_bot_names():
    bot_names = ['Edmund', 'Alfred', 'Harold', 'Edward', 'William', 'Richard', 'Henry']
    random.shuffle(bot_names)
    bot1_name = bot_names.pop()
    bot2_name = bot_names.pop()
    bot3_name = bot_names.pop()
    return bot1_name, bot2_name, bot3_name

MAIN_DECK = Deck()
PLAYER = Player(name = input("Enter your name: "))


bot1_name, bot2_name, bot3_name = get_bot_names()

BOT1 = Bot(bot1_name)
BOT2 = Bot(bot2_name)
BOT3 = Bot(bot3_name)


def shuffle_and_deal():
    random.shuffle(MAIN_DECK.cards)
    for i in range(5):
        PLAYER.hand.append(MAIN_DECK.cards.pop())
        BOT1.hand.append(MAIN_DECK.cards.pop())
        BOT2.hand.append(MAIN_DECK.cards.pop())
        BOT3.hand.append(MAIN_DECK.cards.pop())

def go_fish():
    print("Welcome to Go Fish! {PLAYER.name}!")
    shuffle_and_deal()
    time.sleep(0.5)
    print(f"Today you're up against three gentleman: {BOT1.name}, {BOT2.name}, and {BOT3.name}.")
    # Main gameplay loop
    while True:
        if len(MAIN_DECK.cards) == 0 and not any(player.hand for player in [PLAYER, BOT1, BOT2, BOT3]):
            break

        # Player's turn
        PLAYER.take_turn()
        PLAYER.check_books()
        # Show press Enter message only on first turn
        if 'shown_enter_message' not in globals():
            print("\nPress Enter between turns to continue...")
            global shown_enter_message
            shown_enter_message = True
        input()

        # Bot 1's turn
        BOT1.take_turn()
        BOT1.check_books()
        input()

        # Bot 2's turn
        BOT2.take_turn()
        BOT2.check_books()
        input()

        # Bot 3's turn
        BOT3.take_turn()
        BOT3.check_books()
        input()

go_fish()