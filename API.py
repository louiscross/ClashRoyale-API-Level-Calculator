# imports required
import requests
from Card import Card
from Account import Account

# main class
class Main:
    def __init__(self, player_tag,auth):
        self.player_tag = player_tag
        self.headers = {
            "Accept": "application/json",
            "Authorization": "Bearer "+auth

        }

    @staticmethod
    def _to_int(value):
        """Return an integer from a string that may contain commas, text, or 'N/A'. Non-numeric -> 0."""
        if value is None:
            return 0
        if isinstance(value, int):
            return value
        s = str(value)
        # Fast path
        if s.upper() == 'N/A':
            return 0
        # Remove everything except digits
        digits = ''.join(ch for ch in s if ch.isdigit())
        return int(digits) if digits else 0

    # not used in this release
    def updated_cards(self, newcardlist):
        print("Card Name\tLevel\tMax Level\tCount")
        print("--------")
        for card in newcardlist:
            print(f"{card.name}\t\t{card.level}\t{card.max_level}\t\t{card.count}")

    # function to get basic details for account ( name , current level, current exp toard next level) will apply this to object
    def getAccount(self, player_data):
        account_name = player_data['name']
        account_gold = 0
        account_level = player_data['expLevel']
        account_exp = player_data['expPoints']
        account_elite_wild_cards = 0
        
        # Initialize all magic items to 0 (these would be manually entered later)
        account_common_wild_cards = 0
        account_rare_wild_cards = 0
        account_epic_wild_cards = 0
        account_legendary_wild_cards = 0
        account_champion_wild_cards = 0
        account_common_book = 0
        account_rare_book = 0
        account_epic_book = 0
        account_legendary_book = 0
        account_champion_book = 0
        account_magic_coin = 0
        
        account = Account(account_name, account_gold, account_level, account_exp, account_elite_wild_cards,
                         account_common_wild_cards, account_rare_wild_cards, account_epic_wild_cards, 
                         account_legendary_wild_cards, account_champion_wild_cards,
                         account_common_book, account_rare_book, account_epic_book, 
                         account_legendary_book, account_champion_book,
                         account_magic_coin)
        return account
    
    # function to get all of the cards in your account, formatting them to cover name, card level, amount of cards and the card max level. This will be applied to object class and listed in card_data
    def getCards(self,cards,card_data):
            # The API returns per-rarity level caps in `maxLevel`. To normalize into a single
            # "card level" scale (so our tables work), anchor the scale to the highest cap
            # seen in the collection (typically the common rarity cap).
            base_max_level = max((c.get('maxLevel', 0) for c in cards), default=0) or 16

            for card in cards:
                card_name = card['name']
                card_max_level = card['maxLevel']
                # Normalize to the base scale.
                card_level = base_max_level - (card_max_level - card['level'])
                card_count = card['count']
                card = Card(card_name, card_level, card_max_level, card_count)
                card_data.append(card)
            return card_data
    
    # function to read data from text file and display level and exp to next level
    # we dont use cumulative exp currently, but could be useful in updates
    def exp_table(self,expTable):
        with open('exp_table.txt', 'r') as f:
            lines = f.readlines()
            
            for line in lines:
                line = line.strip().split('\t')
                level = int(line[0])
                exp_to_next_level = line[1].replace(',', '')
                cumulative_exp = int(line[2].replace(',', ''))
                
                expTable.append((level, exp_to_next_level, cumulative_exp))
        return expTable

    # function to read data from text file and display level and gold required to upgrade to next level. We only need to use the uncommon column as values are all the same
    # apart from legendaries to level 10 however we will counter this later.
    def upgrade_table(self,upgradeTable):
        with open('upgrade_table.txt', 'r') as f:
            lines = f.readlines()
            
            for line in lines:
                line = line.strip().split('\t')
                level = int(line[0])
                gold_to_next_level = line[1].replace(',', '')
                
                upgradeTable.append((level, gold_to_next_level))
        return upgradeTable
    
    # function to read data from text file and display level and exp required to upgrade to next level. We only need to use the uncommon column as values are all the same
    # apart from legendaries to level 10 however we will counter this later.
    def upgrade_table_exp(self,upgradeTableExp):
        with open('upgrade_table_exp.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().split('\t')
                level = int(line[0])
                exp_to_next_level = line[1].replace(',', '')
                
                upgradeTableExp.append((level, exp_to_next_level))
        return upgradeTableExp
    
    def card_required_table(self,cardRequiredTable):
        with open('card_required_table.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().split('\t')
                level = int(line[0])
                card_to_next_level_common = line[1].replace(',', '')
                card_to_next_level_rare = line[2].replace(',', '')
                card_to_next_level_epic = line[3].replace(',', '')
                card_to_next_level_legendary = line[4].replace(',', '')
                card_to_next_level_champion = line[5].replace(',', '')
                
                cardRequiredTable.append((level, card_to_next_level_common,card_to_next_level_rare,card_to_next_level_epic,card_to_next_level_legendary,card_to_next_level_champion))
        return cardRequiredTable
    



    def run(self):
        # initialise variables
        option = 0
        upgradeTableExp = []
        card_data = []
        upgradeTable = []
        expTable = []
        cardRequiredTable = []
        updatedcards = []
        
        # this index is used to determine which column to use on the card required table.
        itemRarityIndex = 0
        response = requests.get(f"https://api.clashroyale.com/v1/players/%23{self.player_tag}", headers=self.headers)

        # if response is good, then program will continue
        if response.status_code == 200:
            player_data = response.json()

            # this is the majority of data needed for the task.
            account = self.getAccount(player_data)
            cards = player_data['cards']
            card = self.getCards(cards,card_data)
            newcardlist = []
            expTable = self.exp_table(expTable)
            upgradeTable = self.upgrade_table(upgradeTable)
            upgradeTableExp = self.upgrade_table_exp(upgradeTableExp)
            cardRequiredTable = self.card_required_table(cardRequiredTable)
            max_king_level = expTable[-1][0] if expTable else 90
            DesiredLevel = input(f"\nplease enter desired level, must be above your current level and below {max_king_level + 1}: ")
            try:
                DesiredLevel = int(DesiredLevel)
            except ValueError:
                print("You did not enter an integer, please try again")
                return self.run()

            if DesiredLevel > max_king_level:
                print(f"Value is above {max_king_level} (the highest level), please try again")
                return self.run()

            if DesiredLevel < account.explevel:
                print("value is lower than your current level, please try again:\n")
                return self.run()
            
            # main logic
            card = sorted(card_data, key=lambda x: x.level, reverse=False)
            # Unified max card level (top of the normalized scale).
            max_card_level = 16

            def rarity_index_from_max_level(max_level):
                # Post-update mapping (Level 16):
                # Common=16, Rare=14, Epic=11, Legendary=8, Champion=6
                if max_level == 16:
                    return 1
                if max_level == 14:
                    return 2
                if max_level == 11:
                    return 3
                if max_level == 8:
                    return 4
                if max_level == 6:
                    return 5
                # Legacy mapping fallback (Level 14/15 era):
                if max_level == 14:
                    return 1
                if max_level == 12:
                    return 2
                if max_level == 9:
                    return 3
                if max_level == 6:
                    return 4
                if max_level == 4:
                    return 5
                return 1

            while account.explevel != DesiredLevel:
                if not card:
                    print("-------\n\nnot enough cards to reach desired level.\n\nThe maximum level / exp you can achieve is:\nLevel: " + str(account.explevel) + "\nExperience: " + str(account.exppoints) + " / " + str(expTable[account.explevel-1][1]) + "\nCosting: " + f'{int(account.gold * -1):,}' + " gold\n\n--------")
                    return
                print("------")
                print(card[0])
                # Determine rarity column (for card requirements table).
                itemRarityIndex = rarity_index_from_max_level(card[0].maxLevel)
                
                if card[0].level >= max_card_level:
                    print( str(card[0].name) + " is removed as level is max\n" )
                    newcardlist.append(card[0])
                    card_data.remove(card[0])
                    # update the card list that is sorted by level
                    card = sorted(card_data, key=lambda x: x.level, reverse=False)
                    continue
                #print(cardRequiredTable[card[0].level-1][itemRarityIndex])
                # This is the amount of cards required to level up
                #cardRequiredTable[card[0].level-1][itemRarityIndex]

                # if number of cards for card is less than the required amount to level up. We then delete from the list
                # Use current level index to fetch requirement to next level (e.g., L8->L9 uses row 9)
                if card[0].level >= len(cardRequiredTable):
                    print( str(card[0].name) + " is removed as no further level data available")
                    target = card_data.index(card[0])
                    newcardlist.append(card_data[target])
                    card_data.remove(card[0])
                    card = sorted(card_data, key=lambda x: x.level, reverse=False)
                    continue
                if card[0].count < Main._to_int(cardRequiredTable[card[0].level][itemRarityIndex]):
                    print( str(card[0].name) + " is removed as not enough cards to upgrade:\n" + str(card[0].count) + "/" + str(cardRequiredTable[card[0].level][itemRarityIndex]))
                    target = card_data.index(card[0])
                    newcardlist.append(card_data[target])
                    card_data.remove(card[0])
                    # update the card list that is sorted by level
                    card = sorted(card_data, key=lambda x: x.level, reverse=False)
                    continue
                
                # if we have enough cards to upgrade then we do. We then add and subtract the neccessary information so our while loop can be continuously updated
                else: 

                    #print(upgradeTable[card[0].level-1][1] )
                    card[0].count = int(card[0].count) - Main._to_int(cardRequiredTable[card[0].level][itemRarityIndex])
                    # increment level first
                    card[0].level = int(card[0].level) + 1
                    # Use next level row for costs/exp (index card.level-1)
                    gold_cost = Main._to_int(upgradeTable[card[0].level-1][1]) if (card[0].level - 1) < len(upgradeTable) else 0
                    exp_gain = Main._to_int(upgradeTableExp[card[0].level-1][1]) if (card[0].level - 1) < len(upgradeTableExp) else 0
                    print("Gold to upgrade: " + str(gold_cost))
                    print("Experience from upgrade: " + str(exp_gain))
                    account.gold = account.gold - gold_cost
                    account.exppoints = account.exppoints + exp_gain
                    print("has been upgraded to: " + str(card[0]))
                    card_data = [c if c.name != card[0].name else card[0] for c in card_data]
                    # update the card list that is sorted by level
                    card = sorted(card_data, key=lambda x: x.level, reverse=False)
                    
                    
                #print(expTable[account.explevel][1])
                #print(account.exppoints)
                exp_to_next = Main._to_int(expTable[account.explevel-1][1])
                if exp_to_next > 0 and account.exppoints >= exp_to_next:
                    account.exppoints = account.exppoints - exp_to_next
                    account.explevel = account.explevel + 1

                    print("--------\n\nYou have reached the requested leve!.\n\nYour new level is:\nLevel: " + str(account.explevel) + "\nExperience: " + str(account.exppoints) + " / " + str(expTable[account.explevel-1][1]) + "\nCosting: " + f'{int(account.gold * -1):,}' + " gold\n\n--------")
                    
                    
                    #option = input("Do you want to:\n1: see cards which have been updated\n2: calculate again with different desired level\n3: Exit\n")
                    #if option == "1":
                    #        print("Card Name\t\tLevel\t\tCount")
                    #        print("--------")
                    #        for card in newcardlist:
                    #            print(f"{card.name}\t\t{card.level}\t\t{card.count}")
                    
                
                            
        else:
            print(f"Error {response.status_code}: {response.text}")


if __name__ == '__main__':
    # Prompt for credentials when running as a script
    try:
        player_tag = input("please enter clash royale player tag, with or without the # : ").strip().upper()
        if player_tag.startswith('#'):
            player_tag = player_tag[1:]
        auth = input("please enter your Clash Royale API token: ").strip()
        main = Main(player_tag, auth)
        main.run()
    except KeyboardInterrupt:
        print("\nExiting...")
