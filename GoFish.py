import time
import random

class Player:
    def __init__(self: 'Player', name: str):
        self.hand: list[str] = []
        self.books: int = 0
        self.name: str = name
        self.is_turn: bool = False
        self.is_winner: bool = False
    
    def takeTurn(self: 'Player', bot1_Obj: 'Bot', bot2_Obj: 'Bot', bot3_Obj: 'Bot') -> None:
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
            
            validCards: list[str] = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
            
            if card not in validCards:
                match card:
                    case 'q':
                        card = 'queen'
                    case 'k':
                        card = 'king'
                    case 'j':
                        card = 'jack'
                    case 'a':
                        card = 'ace'
                    
                    case 'two':
                        card = '2'
                    case 'three':
                        card = '3'
                    case 'four':
                        card = '4'
                    case 'five':
                        card = '5'
                    case 'six':
                        card = '6'
                    case 'seven':
                        card = '7'
                    case 'eight':
                        card = '8'
                    case 'nine':
                        card = '9'
                    case 'ten':
                        card = '10'
                    
                    case _:
                        print("Please enter a valid card value (2-10, Jack, Queen, King, or Ace)")
                        continue
            
            # I'm pretty sure we don't need this but I'll leave it here for now
            # Check if player has the card
            # if card not in self.hand:
            #     print("You don't have that card in your hand. Try again.")
            #     continue
            
            card = card.capitalize()
            break

        print(f"You asked for the {card}.")
        time.sleep(0.3)
        print("Who would you like to ask? (Enter their name)")
        
        while True:
            opponentName: str = input("> ").strip()
            targetPlayerObj: Bot | None = None
            
            for botObj in [bot1_Obj, bot2_Obj, bot3_Obj]:
                if botObj.name.lower() == opponentName.lower():
                    targetPlayerObj = botObj
                    break
            
            if not targetPlayerObj:
                print(f"That player doesn't exist. Please ask {bot1_Obj.name}, {bot2_Obj.name}, or {bot3_Obj.name}")
                continue
            else:
                break

        print(f"You asked {targetPlayerObj.name} for a {card}.")
        time.sleep(0.3)

        # Check if the target player has the requested card
        matchingCards: list[str] = [card for card in targetPlayerObj.hand if card.lower() in card.lower()]
        if matchingCards:
            print(f"{targetPlayerObj.name} has {len(matchingCards)} {card}{'s' if len(matchingCards) > 1 else ''}!")
            for match in matchingCards:
                targetPlayerObj.hand.remove(match)
                self.hand.append(match)
                time.sleep(0.3)
        else:
            print(f"{targetPlayerObj.name} doesn't have a {card}.")
            time.sleep(0.3)
            print("Go fish!")
            if mainDeck.cards:
                drawn_card = mainDeck.cards.pop()
                self.hand.append(drawn_card)
                print(f"You drew the {drawn_card}")
            else:
                print("The deck is empty!")
                time.sleep(1)

    def checkBooks(self: 'Player') -> None:
        rankCounts: dict[str, int] = {}
        
        for card in self.hand:
            rank: str = card.split(' of ')[0].lower()
            rankCounts[rank] = rankCounts.get(rank, 0) + 1
        
        for rank, count in rankCounts.items():
            if count == 4:
                print(f"You got a book of {rank}s!")
                self.books += 1
                self.hand = [card for card in self.hand if rank.lower() not in card.lower()]

class Bot:
    def __init__(self: 'Bot', name: str):
        self.hand: list[str] = []
        self.books: int = 0
        self.name: str = name
        self.is_turn: bool = False
        self.is_winner: bool = False
    
    def takeTurn(self: 'Bot', playerObj: Player, bot1_Obj: 'Bot', bot2_Obj: 'Bot', bot3_Obj: 'Bot') -> None:
        print(f"It's {self.name}'s turn!")
        # Count occurrences of each rank in hand
        rankCounts: dict[str, int] = {}
        for card in self.hand:
            rank = card.split(' of ')[0].lower()
            rankCounts[rank] = rankCounts.get(rank, 0) + 1
        
        if not rankCounts:
            return  # Empty hand

        # Find the ranks with maximum count
        maxCount: int = max(rankCounts.values()) if rankCounts else 0
        maxRanks: list[str] = [rank for rank, count in rankCounts.items() if count == maxCount]
        
        # Choose random rank from those with max count
        chosenRank: str = random.choice(maxRanks) if maxRanks else ""
        
        possibleTargets: list[Player | Bot] = []
        # Choose random player to ask
        for player in [playerObj, bot1_Obj, bot2_Obj, bot3_Obj]:
            if player != self and player.hand:
                possibleTargets.append(player)
                break
        
        if not possibleTargets:
            return
        
        targetPlayer: Player | Bot = random.choice(possibleTargets)
        
        print(f"{self.name} asks {targetPlayer.name} for a {chosenRank}")
        time.sleep(0.3)
        
        # Check if target has matching cards
        matchingCards: list[str] = [card for card in targetPlayer.hand if chosenRank.lower() in card.lower()]
        
        if matchingCards:
            print(f"{targetPlayer.name} has {len(matchingCards)} {chosenRank}{'s' if len(matchingCards) > 1 else ''}!")
            for match in matchingCards:
                targetPlayer.hand.remove(match)
                self.hand.append(match)
                time.sleep(0.3)
        
        else:
            print(f"{targetPlayer.name} doesn't have a {chosenRank}")
            print(f"{self.name} goes fish!")
            if mainDeck.cards:
                drawn_card = mainDeck.cards.pop()
                self.hand.append(drawn_card)
                time.sleep(0.3)
    
    def checkBooks(self: 'Bot') -> None:
        rankCounts: dict[str, int] = {}
        
        for card in self.hand:
            rank: str = card.split(' of ')[0].lower()
            rankCounts[rank] = rankCounts.get(rank, 0) + 1
        
        for rank, count in rankCounts.items():
            if count == 4:
                print(f"{self.name} got a book of {rank}s!")
                self.books += 1
                self.hand = [c for c in self.hand if rank.lower() not in c.lower()]

class Deck:
    def __init__(self: 'Deck') -> None:
        self.cards: list[str] = []
        suits: list[str] = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks: list[str] = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for suit in suits:
            for rank in ranks:
                self.cards.append(f"{rank} of {suit}")

def generateRandomBotNames() -> tuple[str, str, str]:
    botNames: list[str] = ['Edmund', 'Alfred', 'Harold', 'Edward', 'William', 'Richard', 'Henry']
    
    random.shuffle(botNames)
    
    bot1Name = botNames.pop()
    bot2Name = botNames.pop()
    bot3Name = botNames.pop()
    
    return bot1Name, bot2Name, bot3Name



def shuffleAndDeal(playerObj: Player, bot1_Obj: Bot, bot2_Obj: Bot, bot3_Obj: Bot) -> tuple[Player, Bot, Bot, Bot]:
    random.shuffle(mainDeck.cards)
    
    for i in range(5):
        playerObj.hand.append(mainDeck.cards.pop())
        bot1_Obj.hand.append(mainDeck.cards.pop())
        bot2_Obj.hand.append(mainDeck.cards.pop())
        bot3_Obj.hand.append(mainDeck.cards.pop())

    return playerObj, bot1_Obj, bot2_Obj, bot3_Obj

def main(mainDeck: Deck, playerObj: Player, bot1_Obj: Bot, bot2_Obj: Bot, bot3_Obj: Bot):
    print(f"Welcome to Go Fish! {playerObj.name}!")
    
    playerAndBotObjs: tuple[Player, Bot, Bot, Bot] = shuffleAndDeal(playerObj, bot1_Obj, bot2_Obj, bot3_Obj)
    
    playerObj = playerAndBotObjs[0]
    bot1_Obj = playerAndBotObjs[1]
    bot2_Obj = playerAndBotObjs[2]
    bot3_Obj = playerAndBotObjs[3]

    time.sleep(0.5)
    
    print(f"Today you're up against three gentleman: {bot1_Obj.name}, {bot2_Obj.name}, and {bot3_Obj.name}.")

    playing: bool = True
    # Main gameplay loop
    while playing:
        # Check if the game is over - when deck is empty and all players have no cards
        deckIsEmpty: bool = len(mainDeck.cards) == 0
        allHandsEmpty: bool = not playerObj.hand and not bot1_Obj.hand and not bot2_Obj.hand and not bot3_Obj.hand
        
        if deckIsEmpty and allHandsEmpty:
            print("Game over! No more cards to play.")
            playing = False
            break

        # Player's turn
        playerObj.takeTurn(bot1_Obj, bot2_Obj, bot3_Obj)
        playerObj.checkBooks()
        
        # Show press Enter message only on first turn
        if 'shown_enter_message' not in globals():
            print("\nPress Enter between turns to continue...")
            shownEnterMessage: bool = True

        # Bot 1's turn
        bot1_Obj.takeTurn(playerObj, bot1_Obj, bot2_Obj, bot3_Obj)
        bot1_Obj.checkBooks()

        # Bot 2's turn
        bot2_Obj.takeTurn(playerObj, bot1_Obj, bot2_Obj, bot3_Obj)
        bot2_Obj.checkBooks()

        # Bot 3's turn
        bot3_Obj.takeTurn(playerObj, bot1_Obj, bot2_Obj, bot3_Obj)
        bot3_Obj.checkBooks()


def getPlayerAndBotNames() -> tuple[str, str, str, str]:
    playerName: str = input("Enter your name: ")
    
    names: tuple[str, str, str] = generateRandomBotNames()

    bot1Name: str = names[0]
    bot2Name: str = names[1]
    bot3Name: str = names[2]

    return playerName, bot1Name, bot2Name, bot3Name

def getPlayerAndBotObjs(playerName: str, bot1Name: str, bot2Name: str, bot3Name: str) -> tuple[Player, Bot, Bot, Bot]:
    playerObj = Player(playerName)
    bot1_Obj = Bot(bot1Name)
    bot2_Obj = Bot(bot2Name)
    bot3_obj = Bot(bot3Name)

    return playerObj, bot1_Obj, bot2_Obj, bot3_obj

def init() -> tuple[Deck, Player, Bot, Bot, Bot]:
    mainDeck = Deck()
    
    playerAndBotNames: tuple[str, str, str, str] = getPlayerAndBotNames()

    playerName: str = playerAndBotNames[0]
    bot1Name: str = playerAndBotNames[1]
    bot2Name: str = playerAndBotNames[2]
    bot3Name: str = playerAndBotNames[3]

    playerAndBotObjs: tuple[Player, Bot, Bot, Bot] = getPlayerAndBotObjs(playerName, bot1Name, bot2Name, bot3Name)
    
    playerObj: Player = playerAndBotObjs[0]
    bot1_Obj: Bot = playerAndBotObjs[1]
    bot2_Obj: Bot = playerAndBotObjs[2]
    bot3_Obj: Bot = playerAndBotObjs[3]

    return mainDeck, playerObj, bot1_Obj, bot2_Obj, bot3_Obj

if __name__ == "__main__":
    playerAndBotObjs: tuple[Deck, Player, Bot, Bot, Bot] = init()

    mainDeck: Deck = playerAndBotObjs[0]
    playerObj: Player = playerAndBotObjs[1]
    bot1_Obj: Bot = playerAndBotObjs[2]
    bot2_Obj: Bot = playerAndBotObjs[3]
    bot3_Obj: Bot = playerAndBotObjs[4]

    main(mainDeck, playerObj, bot1_Obj, bot2_Obj, bot3_Obj)