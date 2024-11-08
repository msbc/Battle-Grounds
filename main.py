import random
import sys

########################
# CONSTANTS & VARIABLES
########################

_CHAPTER_LINE = "=" * 50
_LOW = 1
_HIGH = 3
_MAX_CHARACTERS = 4
_LOSE = 0  # Might comment this out later... {UPDATE!: I'm not commenting _LOSE out. It's needed}

###############
# DICTIONARIES
###############

# creating a margin of error to allow for the input of moves to feel more active and reactive to the player possibly misspelling a word

classes = {
    "assassin": ["assassin", "a"],
    "cleric": ["cleric", "c"],
    "fighter": ["fighter", "f"],
    "wizard": ["wizard", "w"]
}

ask_user = {
    "ready": ["ready", "r"],
    "not": ["no", "not", "not ready", "n", "nr"]
}


###########
# CLASSES
###########

# __init__ --> (comments on this in the next line)
# This assigns a changeable value to the constants.
# Whenever the functions that denote the actions each class takes, I won't have to worry about the baseline code itself changing alongside any instances of each class.
# This prevents any possible issues with calling the class and makes transforming them throughout the fight much easier on my end.

class Cleric:
    _NAME = "Cleric"
    _BASE_HP = 8
    _BASE_DMG = 2
    _BASE_SHIELD = 2
    _BASE_SPELL = 1

    hp: int
    dmg: int
    shield: int
    spell: int

    moves = {
        "attack": ["hammer", "attack", "hmr", "h", "hamer", "atk", "dmg"],
        "block": ["sacred shield", "block", "blk", "s", "ss", "sacred", "shield", "sacred sheild"],
        "spell": ["pray", "spell", "p", "prey", "status"]
    }

    def __init__(self):
        self.hp = self._BASE_HP
        self.dmg = self._BASE_DMG
        self.shield = self._BASE_SHIELD
        self.spell = self._BASE_SPELL
        self.overflow_dmg = 0

    def stat_line(self):
        stats = f"{self._NAME}\n[HP]: {self.hp}/{self._BASE_HP}\n[ATTACK]: Hammer (DMG = {self.dmg}) | [BLOCK]: Sacred Shield (BLK = {self.shield}) | [SPELL]: Pray ('Increase your HEALTH by {self.spell}')\n"
        return stats

    def attack(self, opponent,
               direct_dmg=True):  # This is across the board for all classes. It will check if the opponent had blocked before calculating health loss.
        if direct_dmg:
            opponent.hp -= self.dmg
        else:
            if self.overflow_dmg >= 1:
                opponent.hp -= self.overflow_dmg
        self.overflow_dmg = 0  # It will also set the overflow dmg back to 0 afterward to prevent any issues with dealing an insane amount of damage all the time.
        self.dmg = self._BASE_DMG
        return opponent.hp, self.overflow_dmg, self.dmg

    def block(self, opponent,
              attacked=True):  # This will only happen if an attack goes into the shield. It'll calculate if the opponent deals any damage over the shield.
        if attacked:
            opponent.overflow_dmg = opponent.dmg - self.shield
        self.shield = self._BASE_SHIELD
        return opponent.overflow_dmg, self.shield

    def status(self):  # will heal only if the player didn't die that turn
        if self.hp > _LOSE:
            self.hp += self.spell
        return self.hp


class Wizard:
    _NAME = "Wizard"
    _BASE_HP = 7
    _BASE_DMG = 3
    _BASE_SHIELD = 2
    _BASE_SPELL = 1

    hp: int
    dmg: int
    shield: int
    spell: int

    moves = {
        "attack": ["fireball", "attack", "fire ball", "fb", "f", "fire", "ball", "atk", "dmg"],
        "block": ["mana ward", "block", "mw", "mana", "ward", "manaward", "blk"],
        "spell": ["weaken", "spell", "w", "status", "weak", "wkn"]
    }

    def __init__(self):
        self.hp = self._BASE_HP
        self.dmg = self._BASE_DMG
        self.shield = self._BASE_SHIELD
        self.spell = self._BASE_SPELL
        self.overflow_dmg = 0

    def stat_line(self):
        stats = f"{self._NAME}\n[HP]: {self.hp}/{self._BASE_HP}\n[ATTACK]: Fireball (DMG = {self.dmg}) | [BLOCK]: Mana Ward (BLK = {self.shield}) | [SPELL]: Weaken ('Reduce opponents ATTACK by {self.spell}')\n"
        return stats

    def attack(self, opponent, direct_dmg=True):
        if direct_dmg:
            opponent.hp -= self.dmg
        else:
            if self.overflow_dmg >= 1:
                opponent.hp -= self.overflow_dmg
        self.dmg = self._BASE_DMG
        self.overflow_dmg = 0
        return opponent.hp, self.overflow_dmg, self.dmg

    def block(self, opponent, attacked=True):
        if attacked:
            opponent.overflow_dmg = opponent.dmg - self.shield
        self.shield = self._BASE_SHIELD
        return opponent.overflow_dmg, self.shield

    def status(self, opponent):  # reduces damage down to 0 flat
        if opponent.dmg > 0:
            opponent.dmg -= self.spell
        return opponent.dmg


class Fighter:
    _NAME = "Fighter"
    _BASE_HP = 7
    _BASE_DMG = 2
    _BASE_SHIELD = 3
    _BASE_SPELL = 1

    hp: int
    dmg: int
    shield: int
    spell: int

    moves = {
        "attack": ["long sword", "sord", "ls", "soard", "l", "sword", "attack", "atk", "longsword", "dmg"],
        "block": ["shield", "s", "block", "blk", "sheild"],
        "spell": ["bolster", "b", "status", "spell", "bolstor"]
    }

    def __init__(self):
        self.hp = self._BASE_HP
        self.dmg = self._BASE_DMG
        self.shield = self._BASE_SHIELD
        self.spell = self._BASE_SPELL
        self.overflow_dmg = 0

    def stat_line(self):
        stats = f"{self._NAME}\n[HP]: {self.hp}/{self._BASE_HP}\n[ATTACK]: Long Sword (DMG = {self.dmg}) | [BLOCK]: Shield (BLK = {self.shield}) | [SPELL]: Bolster ('Increase your ATTACK by {self.spell}')\n"
        return stats

    def attack(self, opponent, direct_dmg=True):
        if direct_dmg:
            opponent.hp -= self.dmg
        else:
            if self.overflow_dmg >= 1:
                opponent.hp -= self.overflow_dmg
        self.dmg = self._BASE_DMG
        self.overflow_dmg = 0
        return opponent.hp, self.overflow_dmg, self.dmg

    def block(self, opponent, attacked=True):
        if attacked:
            opponent.overflow_dmg = opponent.dmg - self.shield
        self.shield = self._BASE_SHIELD
        return opponent.overflow_dmg, self.shield

    def status(self):  # increases dmg per use until you use an attack
        self.dmg += self.spell
        return self.dmg


class Assassin:
    _NAME = "Assassin"
    _BASE_HP = 6
    _BASE_DMG = 2
    _BASE_SHIELD = 3
    _BASE_SPELL = 1

    hp: int
    dmg: int
    shield: int
    spell: int

    moves = {
        "attack": ["attack", "dagger", "d", "dag", "dager", "atk", "dmg"],
        "block": ["block", "cloak", "c", "cloac", "clok", "blk"],
        "spell": ["spell", "sabotage", "s", "sabatoge", "status"]
    }

    def __init__(self):
        self.hp = self._BASE_HP
        self.dmg = self._BASE_DMG
        self.shield = self._BASE_SHIELD
        self.spell = self._BASE_SPELL
        self.overflow_dmg = 0

    def stat_line(self):
        stats = f"{self._NAME}\n[HP]: {self.hp}/{self._BASE_HP}\n[ATTACK]: Dagger (DMG = {self.dmg}) | [BLOCK]: Cloak (BLK = {self.shield} + Deal 1 DMG to opponent if ATTACKED) | [SPELL]: Sabotage ('Reduce opponents BLOCK by {self.spell}')\n"
        return stats

    def attack(self, opponent, direct_dmg=True):
        if direct_dmg:
            opponent.hp -= self.dmg
        else:
            if self.overflow_dmg >= 1:
                opponent.hp -= self.overflow_dmg
        self.dmg = self._BASE_DMG
        self.overflow_dmg = 0
        return opponent.hp, self.overflow_dmg, self.dmg

    def block(self, opponent, attacked=True):
        if attacked:
            opponent.overflow_dmg = opponent.dmg - self.shield
            opponent.hp -= 1
        self.shield = self._BASE_SHIELD
        return opponent.overflow_dmg, opponent.hp, self.shield

    def status(self, opponent):
        if opponent.shield > 0:
            opponent.shield -= self.spell
        return opponent.shield


######################
# SELECTION FUNCTIONS
######################

# will run code to set the cmp_chr to whatever class is randomly selected
def computer_selection():
    computer = random.randint(_LOW,
                              _MAX_CHARACTERS)  # It's a simple way of denoting a random choice for what the 'computer' will get for their character
    if computer == 1:
        character = Assassin()
        return character
    elif computer == 2:
        character = Cleric()
        return character
    elif computer == 3:
        character = Fighter()
        return character
    elif computer == 4:
        character = Wizard()
        return character
    else:
        raise ValueError(
            "Error within the computer_selection() function code")  # if I ever revisit the code I'll know that I forgot to update this section if I add more classes


# User's choice will assign plr_chr a class
def user_selection():  # I can make sure the player selects a valid option and then assign the user the right class, creating an instance.
    inp = ""
    while inp not in classes["assassin"] and inp not in classes["cleric"] and inp not in classes[
        "fighter"] and inp not in classes["wizard"] and inp != "h":
        inp = input("Pick either Wizard, Fighter, Cleric, Assassin, or (H) here --> ").lower()
        if inp not in classes["assassin"] and inp not in classes["cleric"] and inp not in classes[
            "fighter"] and inp not in classes["wizard"] and inp != "h":
            print("ERROR! Selection must be one of the letters/names above --- Try again\n")
    if inp in classes["wizard"]:
        player = Wizard()
        return player
    elif inp in classes["fighter"]:
        player = Fighter()
        return player
    elif inp in classes["cleric"]:
        player = Cleric()
        return player
    elif inp in classes["assassin"]:
        player = Assassin()
        return player
    elif inp == "h":
        print(""" "Ah, so you're new 'round here? Let's give you the quick run down-" 
The man continues to speak. You listen carefully and write down what you hear as you go.

Basics:

Each class has specific stats and specialties. Some prefer the offensive while others thrive under the defensive. Some just want to be the most annoying [Not PG!!!] imaginable.
Your goal? Slay your opponent! The last one standing is the victor! Use your selection of combat options wisely as they could mean life or death.
The most advanced and skilled fighters are ones who can accurately read a battle and capitalize on anything they can!

Moves:

You have 3 total options: An attack, a block, and a spell/status effect of sorts. 
Attacks will harm the opponent, bringing you closer to victory with each successful blow.
However, attacks can be mitigated through the power of the block! Blocking will temporarily grant you an extra line of defense for that move, any damage that goes over a shield will result in HP lost.
And last but certainly not least the status move. This move lets you temporarily boost or reduce stats of either yourself or the opponent. Varying based on the champion you select.

There is a triangle method to what move should be used when. Attacks are best used against statuses, statuses against blocks, and blocks against attacks.
Select the right one and celebrate an advantage! If not, keep fighting and learn!

When you select a move, type in the move name as shown in the stat block and it 'should' go through as valid! 
If not, try something similar or double check your spelling.

Extra:

Stats of you and your opponent will be put on display at the start of a fight and after each turn plays out. These show you some important things.
The two biggest ones are the HP and move stats. HP is your health, obviously. If it wasn't obvious enough already, keep it above 0 if you value your life.
Move stats on the other hand are a different beast. Next to the move names will be the stats that each move CURRENTLY has. These are inside the ()'s.
After each turn plays out, the stats will be updated automatically. So no need to track it manually.

"Well. I think that is about everything you need to know. Good luck, and may the strong survive."

Restart the code to play.""")
        sys.exit()
    else:
        raise ValueError("There was an ERROR within the user_selection() function")


# checks if the user is ready to play before starting just in case if they accidentally selected the wrong class
def ready():
    swag = ""
    print("\nAre you ready to fight?\n")
    while swag not in ask_user["ready"] and swag not in ask_user["not"]:
        swag = input(
            "Input READY if you are ready to fight. If not, input NO and the game will stop running. Input it here --> ").lower()
        if swag not in ask_user["ready"] and swag not in ask_user["not"]:
            print(_CHAPTER_LINE)
            print("\nThat is not a valid input. Please input a valid option as explained previously.\n")
    if swag in ask_user["ready"]:
        print("No need to delay further. Good luck.")
    elif swag in ask_user["not"]:
        print("Come back once you are ready to fight.")
        sys.exit()
    else:
        raise ValueError("Error in the ready() function")


#########################
# TURN BY TURN FUNCTIONS
#########################

def turn_layout(counter, player, computer):
    result = f"Turn: {str(counter)}\n\n[PLAYER]\n{player.stat_line()}\n[COMPUTER]\n{computer.stat_line()}"
    return result


# simply formating and looping. Does it HAVE to be a function? Not really, but it makes it easier to update and locate in my opinion.

def player_move_selector(player):
    inp = ""
    x = 0
    print("What move will you pick? (Look over your stat sheet and type out the move name you'd like)")
    while inp not in player.moves["attack"] and inp not in player.moves["block"] and inp not in player.moves["spell"]:
        inp = input("Input move here --> ").lower()
        if inp not in player.moves["attack"] and inp not in player.moves["block"] and inp not in player.moves["spell"]:
            print("That is not a valid move name, please try again.\n")
    if inp in player.moves["attack"]:
        x = 1
    elif inp in player.moves["block"]:
        x = 2
    elif inp in player.moves["spell"]:
        x = 3
    else:
        raise ValueError("Error within the player_move_selector() function")
    return x


# comparing the users input to a set list within a dictionary for each type of move with possible inputs
# the inputs used are a combination of typos, shortenings of words, etc.
# it will then assign a value to 'x' based around what the valid input falls under within the dictionary

def computer_move_selector():
    x = 0
    choice = random.randint(_LOW, _HIGH)
    if choice == 1:
        x = 1
    elif choice == 2:
        x = 2
    elif choice == 3:
        x = 3
    else:
        raise ValueError("Error within the computer_move_selector() function")
    return x


# Nothing complex here, just a simple way to create a value that will be used in a different function to initiate the combat sequence.

# OKAY! So, the usage of both ifs and elifs on the statuses are to make sure that I'm passing in the correct number of parameters into the function.
# The sequence will check what number is assigned to the player based on his or her decision with move selection, this is then ran until located. This is then repeated for the computer's random selection.
# Once selected, it will run the code for each instance's function in the correct order and return it to update the stats of both players.
def combat_sequence(player, computer, p_choice, c_choice):
    if p_choice == 1:
        if c_choice == 1:
            computer.attack(player, True)
            player.attack(computer, True)
            print(f"The {player._NAME} and {computer._NAME} trade blows!")
        elif c_choice == 2:
            computer.block(player, True)
            player.attack(computer, False)
            print(f"The {player._NAME} swings in! But the {computer._NAME} defends the blow!")
        elif c_choice == 3:
            player.attack(computer, True)
            if computer._NAME == "Fighter" or computer._NAME == "Cleric":
                computer.status()
            elif computer._NAME == "Wizard" or computer._NAME == "Assassin":
                computer.status(player)
            print(f"The {player._NAME} strikes the {computer._NAME} while he uses a spell!")
    elif p_choice == 2:
        if c_choice == 1:
            player.block(computer, True)
            computer.attack(player, False)
            print(f"The {player._NAME} successfully blocks the {computer._NAME}'s attack!")
        elif c_choice == 2:
            player.block(computer, False)
            computer.block(player, False)
            print(f"Both the {player._NAME} and {computer._NAME} stare at each other.")
        elif c_choice == 3:
            player.block(computer, False)
            if computer._NAME == "Fighter" or computer._NAME == "Cleric":
                computer.status()
            elif computer._NAME == "Wizard" or computer._NAME == "Assassin":
                computer.status(player)
            print(f"The {player._NAME} blocks. The {computer._NAME} wisely casts.")
    elif p_choice == 3:
        if c_choice == 1:
            computer.attack(player, True)
            if player._NAME == "Fighter" or player._NAME == "Cleric":
                player.status()
            elif player._NAME == "Wizard" or player._NAME == "Assassin":
                player.status(computer)
            print(f"While the {player._NAME} uses a spell, the {computer._NAME} attacks!")
        elif c_choice == 2:
            computer.block(player, False)
            if player._NAME == "Fighter" or player._NAME == "Cleric":
                player.status()
            elif player._NAME == "Wizard" or player._NAME == "Assassin":
                player.status(computer)
            print(f"The {computer._NAME} blocks while the {player._NAME} uses a spell.")
        elif c_choice == 3:
            if computer._NAME == "Fighter" or computer._NAME == "Cleric":
                computer.status()
            elif computer._NAME == "Wizard" or computer._NAME == "Assassin":
                computer.status(player)
            if player._NAME == "Fighter" or player._NAME == "Cleric":
                player.status()
            elif player._NAME == "Wizard" or player._NAME == "Assassin":
                player.status(computer)
            print(f"The {computer._NAME} uses a spell along with the {player._NAME}.")


############
# MAIN FUNC
############

def main():
    print(_CHAPTER_LINE * 3)
    print(f""""Come one and all to the colosseum! Come and witness the highest quality combat you will EVER see with your very own eyes!" 
The crowd erupts in applause and cheer. You can barely hear yourself think. Only one thing to do now, select your champion and guide them to victory!\n\n""")
    print("""Please select one of the following classes below:
- Wizard (W)
- Fighter (F)
- Cleric (C)
- Assassin (A)

Once selected, the battle will immediately commence.
If you are new to the game or need a refresher on the rules, please input the letter H for Help (H).

    Good luck, and may the better fighter win!""")
    plr_chr = user_selection()
    cmp_chr = computer_selection()
    print(_CHAPTER_LINE * 2)
    print("The player has chosen " + plr_chr._NAME + " as their champion!\n")
    print("The opponent has chosen " + cmp_chr._NAME + " as their champion!\n")
    print(""""Alright...it is now time for the battle to commence!"
The crowd roars.

I hope that you are ready.""")
    ready()  # making sure that players are ACTUALLY ready to play
    turn = 0
    while plr_chr.hp > _LOSE and cmp_chr.hp > _LOSE:
        print(_CHAPTER_LINE * 3)
        turn += 1
        layout = turn_layout(turn, plr_chr, cmp_chr)
        print(layout)
        player_move = player_move_selector(plr_chr)
        computer_move = computer_move_selector()
        combat_sequence(plr_chr, cmp_chr, player_move,
                        computer_move)  # I am in pain because of SPELLS. Somehow THAT is my biggest issue {UPDATE!: My issue was that I named the function spells and used a variable named spells. Just had to change it to 'status' for it to work.}
    if plr_chr.hp <= _LOSE:
        print("\n" + (_CHAPTER_LINE * 2))
        print(
            f""""WHAT A MATCH!" The commentator exclaims. "LADIES AND GENTLEMEN, WE HAVE OURSELVES A WINNER! THE {cmp_chr._NAME} HAS WON!"

Your champion died. As you watch in horror at the outcome of the match, you feel a set of hands grab you. You struggle and struggle, but the hands won't let go.
This is now the end of the road for you as you get dragged across the cold stone floor. Each step of the guards dragging you echoes across the damp hallway.

Quite the sad ending to your newly started journey.""")
        sys.exit()
    elif cmp_chr.hp <= _LOSE:
        print("\n" + (_CHAPTER_LINE * 2))
        print(f"""The crowd erupts in cheers as the {cmp_chr._NAME} falls to the ground lifelessly.
"WE HAVE A BRAND NEW VICTOR!" The commentator pridefully shouts. "THE {plr_chr._NAME} HAS EMERGED VICTORIOUS!"

The cheering of the crowd continues as you watch your champion revel in his newfound glory. A voice from behind speaks up.
"No time to stare prisoner. You are being relocated for the next match. Fail to follow these orders and you'll end up like your opponent."
You oblige to the demands of the guard as you value your own life. It seems as if the only way for you to survive this mess is through winning.
Lose once...and you lose your life.""")
        sys.exit()


if __name__ == '__main__':  # nothing to really comment on here...
    main()
