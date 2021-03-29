import tkinter as tk
from tkinter import messagebox
import re
import importlib, inspect

from PlayerController import playerController
from RandomBot import randomBot
from Standard1V1Bot import standard1v1Bot
import WinConditions as wincons
from NimInstance import NimInstance

class nimApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Nim Game")
        self.start_frame = startFrame(master = self)
        self.option_frame = optionFrame(master = self)
        self.load_frame = tk.Frame()
        tk.Label(self.load_frame, text="...").pack()
        self.current_frame = self.start_frame
        self.current_frame.pack()

    def switchToTargetFrame(self, target_frame):
        self.current_frame.pack_forget()
        target_frame.pack()
        self.current_frame = target_frame

    # Begins a new game of Nim with currently selected players and settings
    def newGame(self):
        self.block = tk.BooleanVar(self)

        game_settings = self.option_frame.getSettings()
        player_list = self.start_frame.getPlayerList().copy()

        while(len(player_list) > 1):
            game_round = NimInstance(game_settings[0].copy(), game_settings[1].copy(), game_settings[2])
            turn = -1

            #Players altenate turns until a terminal condition is met.
            while not game_round.checkForWin():
                turn = (turn + 1)%len(player_list)
                self.block.set(True)
                player_list[turn].playTurn(game_round)
                self.wait_variable(self.block)

            #Check if game is Misere or not. If not, last turn wins immediately
            if not game_settings[2]:
                
                # If no turns were played (i.e. starting position is win condition)
                #then first player wins by default.
                if turn < 0:
                    break

                player_list[0] = player_list[turn] #sets the last person to make a move to the front of the list
                break #Once the loop is exited, front of the list wins.

            #Otherwise, player to play last turn gets eliminated
            if len(player_list) > 2:
                self.block.set(True)
                self.switchToTargetFrame(messageFrame(self, msg=player_list[turn].getName() + " was eliminated!", btn_msg="Ok", block=self.block, btn_callback_frame=self.load_frame))
                self.wait_variable(self.block)

            # Need to check for this in case starting piles is a win condition...
            if turn > -1:
                player_list.pop(turn)
            else:
                player_list.pop(0)

        #Show Victory Screen
        self.switchToTargetFrame(messageFrame(self, msg=player_list[0].getName() + " wins!", btn_msg="Return", block=self.block, btn_callback_frame=self.start_frame))

    #Callback for human playercontrollers
    def humanTurn(self, name, nim_instance):
        self.switchToTargetFrame(playerChoiceFrame(self, name, nim_instance, self.playerChoice))

    #Callback for bot playercontrollers
    def botTurn(self, name, nim_instance, choice):
        pile_list = nim_instance.peek_list()
        plural = "s" if choice[1] > 1 else ""
        nim_instance.takeFromPile(*choice)
        self.switchToTargetFrame(botMessageFrame(self, msg=name + " took " + str(choice[1]) + " object" + plural + " from pile " + str(choice[0]+1), block=self.block, btn_callback_frame=self.load_frame, pile_list=pile_list, choice=choice))

    #Callback for button in playerChoiceFrame
    def playerChoice(self, nim_instance, pile_num, amount):
        nim_instance.takeFromPile(pile_num, amount)
        self.block.set(False)


class startFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.parent = master

        #Frame for adding human players
        self.name_entry_frame = tk.LabelFrame(self, text="Add Human Player")
        self.name_entry_frame.grid(row = 0)
        self.name_entry_value = tk.StringVar()
        self.name_entry_value.trace_add("write", self.validateHumanAdd)
        self.name_entry_field = tk.Entry(self.name_entry_frame, textvariable = self.name_entry_value)
        self.name_entry_field.pack(side = tk.LEFT)
        self.name_entry_button = tk.Button(self.name_entry_frame, text="Add", command = self.addHumanPlayer, state = tk.DISABLED)
        self.name_entry_button.pack()

        #Frame for adding bots
        self.bot_entry_frame = tk.LabelFrame(self, text="Add a bot")
        self.bot_entry_frame.grid(row = 1)
        self.bot_list = list()

        # Factory for bots
        # Inspired by: https://stackoverflow.com/a/55067404 viewed March 28, 2021
        for _, cls in inspect.getmembers(importlib.import_module("NimBots"), inspect.isclass):
            if cls.__module__ == 'NimBots':
                self.bot_list.append(tk.Button(self.bot_entry_frame, text=cls.getDescription(), command = lambda c=cls: self.addBot(c), state=tk.DISABLED))

        #Add bot buttons to frame
        for bot in self.bot_list:
            bot.pack()
        
        #An Entry and its controls for naming bots
        self.bot_entry_value = tk.StringVar()
        self.bot_entry_value.trace_add("write", self.validateBotAdd)
        tk.Label(self.bot_entry_frame, text="Bot Name:").pack(side=tk.LEFT)
        self.bot_entry_field = tk.Entry(self.bot_entry_frame, textvariable=self.bot_entry_value)
        self.bot_entry_field.pack(side=tk.LEFT)

        #Frame for viewing currently selected players
        self.player_view_frame = tk.LabelFrame(self, text="Current Players")
        self.player_view_frame.grid(row = 0, rowspan = 2, column = 1, sticky = "news")
        self.dummy_label = tk.Label(self.player_view_frame, text = " ")
        self.dummy_label.pack()
        self.dummy_label.destroy()
        self.player_count = tk.IntVar()
        self.player_count.set(0)
        self.player_count.trace_add("write", self.validatePlayerCount)
        self.player_list = list()

        #Frame for GUI Controls
        self.control_frame = tk.Frame(self)
        self.control_frame.grid(row = 3, columnspan = 2)
        self.start_play_button = tk.Button(self.control_frame, text="Play!", state=tk.DISABLED, command = self.parent.newGame)
        self.start_play_button.pack(side = tk.LEFT)
        self.options_button    = tk.Button(self.control_frame, text="Options", command = lambda: self.parent.switchToTargetFrame(self.parent.option_frame))
        self.options_button.pack(side = tk.LEFT)
        self.quit_button       = tk.Button(self.control_frame, text="Exit", command = self.parent.quit)
        self.quit_button.pack()

    # Checks name entry and deactivates add human button if blank
    def validateHumanAdd(self, *args):
        #print(str(len(self.name_entry_value.get())))
        if len(self.name_entry_value.get()) < 1:
            self.name_entry_button["state"] = tk.DISABLED
        else:
            self.name_entry_button["state"] = tk.NORMAL

    # Checks bot name entry and deactivates add bot button if blank  
    def validateBotAdd(self, *args):
        if len(self.bot_entry_value.get()) < 1:
            for button in self.bot_list:
                button["state"] = tk.DISABLED
        else:
            for button in self.bot_list:
                button["state"] = tk.NORMAL

    # Deactivates start game button if there are no players
    # (single player games are allowed for testing purposes)
    def validatePlayerCount(self, *args):
        if self.player_count.get() < 1:
            self.start_play_button["state"] = tk.DISABLED
        else:
            self.start_play_button["state"] = tk.NORMAL

    # Adds a human playercontroller to the list of players
    def addHumanPlayer(self):
        pc = playerController(self.name_entry_field.get(), self.player_count.get(), self.parent.humanTurn)
        self.player_list.append(pc)
        self.addPlayer(pc)
        self.name_entry_field.delete(0, tk.END)

    # Adds a computer playercontroller to the list of players
    def addBot(self, bot_type):
        pc = bot_type(self.bot_entry_value.get() + " bot", self.player_count.get(), self.parent.botTurn)
        self.player_list.append(pc)
        self.addPlayer(pc)
        self.bot_entry_field.delete(0, tk.END)

    # Updates GUI components when a playercontroller is added to the player list
    def addPlayer(self, pc):
        new_player_frame = tk.Frame(self.player_view_frame)
        new_player_frame.pack()
        tk.Label(new_player_frame, text = pc.getName()).pack(side = tk.LEFT)
        tk.Button(new_player_frame, text = "Remove", command = lambda: self.removePlayer(new_player_frame, pc)).pack()
        self.player_count.set(self.player_count.get() + 1)

    # Removes a player from the player list and updates GUI components
    # (button callback)
    def removePlayer(self, player_frame, pc):
        player_frame.destroy()
        self.player_list.remove(pc)
        self.player_count.set(self.player_count.get() - 1)

        removed_rank = pc.getRank()
        for player in self.player_list:
            if player.getRank() > removed_rank:
                player.decrementRank()

    # Returns the player list
    def getPlayerList(self):
        return self.player_list
        
class optionFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.parent = master
        self.pile_list = list()
        self.rule_list = list()

        #Control for adding piles
        self.pile_frame = tk.Frame(self)
        self.pile_frame.grid(row=0)
        self.pile_list_frame = tk.LabelFrame(self.pile_frame, text = "Piles")
        self.pile_list_frame.grid(row=0, columnspan=2)

        #Validation for entry box
        self.pile_value = tk.StringVar()
        self.pile_value.trace_add("write", self.validatePileAdd)
        self.pile_vcmd = self.pile_frame.register(self.validatePileEntry)
        self.pile_entry = tk.Entry(self.pile_frame, validate='key', validatecommand=(self.pile_vcmd, '%S'), textvariable = self.pile_value)
        self.pile_entry.grid(row=1, column=0)

        #Entry button for new piles
        self.pile_button = tk.Button(self.pile_frame, text = "Add Pile", state = tk.DISABLED, command = self.pileButtonPress)
        self.pile_button.grid(row=1, column=1)

        #Control for adding rules
        self.rule_frame = tk.Frame(self)
        self.rule_frame.grid(row=0, column=1) 
        self.rule_list_frame = tk.LabelFrame(self.rule_frame, text = "Rules")
        self.rule_list_frame.grid(row = 0, columnspan = 2)

        #Absolute default. Cannot be removed.
        self.addOption(self.rule_list_frame, wincons.RULE_1, self.rule_list, removable=False)

        #Entry box for rules
        self.rule_value = tk.StringVar()
        self.rule_value.trace_add("write", self.validateRuleAdd)
        self.rule_entry = tk.Entry(self.rule_frame, textvariable = self.rule_value)
        self.rule_entry.grid(row=1, column=0)

        #Button for adding rules
        self.rule_button = tk.Button(self.rule_frame, text = "Add Rule", state = tk.DISABLED, command = self.ruleButtonPress)
        self.rule_button.grid(row=1, column=1)

        self.return_button = tk.Button(self, text="Return", command = lambda: self.parent.switchToTargetFrame(self.parent.start_frame))
        self.return_button.grid(row = 2, columnspan=2, sticky=tk.E)
        self.pile_amount = tk.IntVar()
        self.pile_amount.set(0)
        self.pile_amount.trace_add("write", self.validateReturnButton)

        #Default Pile
        self.addOption(self.pile_list_frame, 9, self.pile_list, decrement=True) 

        #Control Buttons
        self.control_frame = tk.Frame(self)
        self.control_frame.grid(row=1, columnspan=2)
        self.game_type = tk.BooleanVar()
        self.game_type.set(True)
        tk.Radiobutton(self.control_frame, text="Misère", variable=self.game_type, value=True).grid(row=0, sticky=tk.W)
        tk.Radiobutton(self.control_frame, text="Standard", variable=self.game_type, value=False).grid(row=0, column=1, sticky=tk.W)

        tk.Button(self.control_frame, text="Add Defaults", command = self.addDefaults).grid(row=0, column=2, sticky=tk.E)

    # Deactivates add pile button if entry field is blank
    def validatePileAdd(self, *args):
        if len(self.pile_value.get()) < 1:
            self.pile_button["state"] = tk.DISABLED
        else:
            self.pile_button["state"] = tk.NORMAL

    # Allows only digits to be entered in the pile entry field
    def validatePileEntry(self, text):
        return text.isdigit()

    # Adds a starting pile to the game settings (button callback)
    def pileButtonPress(self):
        self.addOption(self.pile_list_frame, int(self.pile_value.get()), self.pile_list, decrement=True)
        self.pile_entry.delete(0, tk.END)

    # Disables add rule button if entry field is blank
    def validateRuleAdd(self, *args):
        if len(self.rule_value.get()) < 1:
            self.rule_button["state"] = tk.DISABLED
        else:
            self.rule_button["state"] = tk.NORMAL

    def validateRuleEntry(self, *args):
        pass

    # Adds a new rule in the form of a list of ints, if that rule is new (button callback)
    def ruleButtonPress(self):
        try:
            new_rule = [int(num) for num in re.findall("[0-9]+", self.rule_entry.get())]
        except Exception:
            messagebox.showerror(title="Error!", message="Invalid input")
            return

        self.addOption(self.rule_list_frame, new_rule, self.rule_list)

        self.rule_entry.delete(0, tk.END)
    
    # Updates gui and list in the corresponding targets
    def addOption(self, target, option, target_list, removable = True, decrement = False):
        if option in target_list:
            return
        else:
            target_list.append(option)
            if decrement:
                self.pile_amount.set(self.pile_amount.get() + 1)

        new_option_frame = tk.Frame(target)
        new_option_frame.pack()
        tk.Label(new_option_frame, text = str(option)).pack(side = tk.LEFT)
        
        if removable:
            tk.Button(new_option_frame, text = "Remove", command = lambda: self.removeOption(new_option_frame, option, target_list, decrement)).pack()

    # Removes an element from the corresponding gui element (target) and game setting list (target_list)
    def removeOption(self, target, option, target_list, decrement):
        target.destroy()
        target_list.remove(option)

        if decrement:
            self.pile_amount.set(self.pile_amount.get() - 1)

    # Adds the two default rules give by class (2, 2) and (1, 2, 3)
    def addDefaults(self):
        for next_rule in wincons.getDefaults():
            self.addOption(self.rule_list_frame, next_rule, self.rule_list)

    # Deactivates the return to main menu button if the pile list is empty
    def validateReturnButton(self, *args):
        if self.pile_amount.get() < 1:
            self.return_button["state"] = tk.DISABLED
        else:
            self.return_button["state"] = tk.NORMAL

    # Returns the current game settings
    def getSettings(self):
        return (self.pile_list, self.rule_list, self.game_type.get())

# Creates a simple frame that displays a message and contains a button for returning to the 
# target frame (btn_callback_frame). Can also take a variable to block on (block) as it waits
# for user input on the return button press.
class messageFrame(tk.Frame):
    def __init__(self, master=None, msg="", btn_msg="Ok", block=None, btn_callback_frame=None):
        tk.Frame.__init__(self, master)

        self.parent = master

        tk.Label(self, text=msg).pack()
        tk.Button(self, text=btn_msg, command=lambda: self.button_callback(block, btn_callback_frame)).pack()

    def button_callback(self, block, btn_callback_frame):
        self.parent.switchToTargetFrame(btn_callback_frame)
        block.set(False)
        self.destroy()

# Extends the message frame class to display the current game piles and a bots
# last turn on that game pile.
class botMessageFrame(messageFrame):
    def __init__(self, master=None, msg="", btn_msg="Ok", block=None, btn_callback_frame=None, pile_list=None, choice=None):
        messageFrame.__init__(self, master=master, msg=msg, btn_msg=btn_msg, block=block, btn_callback_frame=btn_callback_frame)

        pile_frame = tk.LabelFrame(self, text="Piles:")
        pile_frame.pack(side=tk.BOTTOM)

        for i in range(len(pile_list)):
            tk.Label(pile_frame, text="Pile " + str(i+1) + ": " + str(pile_list[i])).grid(row=i, column=0)
            if i == choice[0]:
                tk.Label(pile_frame, text=" -" + str(choice[1]), fg="red").grid(row=i, column=1)


# Creates a frame which allows a human player to choose which pile to draw
# from and how many objects to take.
class playerChoiceFrame(tk.Frame):
    def __init__(self, master, name, nim_instance, btn_callback):
        tk.Frame.__init__(self, master)

        self.btn_callback = btn_callback
        self.nim_instance = nim_instance

        tk.Label(self, text=name + "\'s turn!").pack()

        tk.Label(self, text="Choose Pile:").pack()

        self.pile_frame = tk.Frame(self)
        self.pile_frame.pack()
        self.game_state = nim_instance.peek_list()
        self.player_selection = tk.IntVar()

        for i in range(len(self.game_state)):
            tk.Radiobutton(self.pile_frame, text=str(self.game_state[i]), variable=self.player_selection, value=i, command=lambda: self.selection_amount.set("")).grid(row=i//3, column=i%3)

        self.control_frame = tk.Frame(self)
        self.control_frame.pack()


        #Validation for entry box
        self.selection_amount = tk.StringVar()
        self.selection_amount.trace_add("write", self.validateSelection)
        self.amount_vcmd = self.pile_frame.register(self.validateAmountEntry)
        self.amount_entry = tk.Entry(self.control_frame, validate='key', validatecommand=(self.amount_vcmd, '%S'), textvariable = self.selection_amount)
        self.amount_entry.pack(side=tk.LEFT)

        self.select_button = tk.Button(self.control_frame, text="Take", command=self.makeSelection)
        self.select_button.pack()

    # Deactivates the select button if entry field is blank
    def validateSelection(self, *args):
        if len(self.selection_amount.get()) < 1:
            self.select_button['state'] = tk.DISABLED
        else:
            self.select_button['state'] = tk.NORMAL

    # Only allows user to enter digits in the range [1, pile_size]
    def validateAmountEntry(self, text):
        return text.isdigit() and int(text) > 0 and int(text) <= self.game_state[self.player_selection.get()]

    # Button callback. Will enter the callback and destroy this frame.
    def makeSelection(self):
        self.btn_callback(self.nim_instance, self.player_selection.get(), int(self.selection_amount.get()))
        self.destroy()