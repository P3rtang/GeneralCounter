from tkinter import *
import pokemonMethodClass as PM
import CounterReadClass as CR

import CounterClass


def dexnavChanceInc(step, neg_chance, chain=0):
    if step <= 100:
        step_chance = step * 6 / 100 / 10000
    elif step <= 200:
        step_chance = ((step - 100) * 2 + 600) / 100 / 10000
    else:
        step_chance = (step - 200 + 800) / 100 / 10000

    if chain == 50:
        neg_chance *= (1 - step_chance) ** 5
    elif chain == 100:
        neg_chance *= (1 - step_chance) ** 10
    else:
        neg_chance *= (1 - step_chance)
    return neg_chance


def dexnavChanceDec(step, neg_chance, chain=0):
    if step < 100:
        step_chance = step * 6 / 100 / 10000
    elif step < 200:
        step_chance = ((step - 100) * 2 + 600) / 100 / 10000
    else:
        step_chance = (step - 200 + 800) / 100 / 10000

    if chain == 49:
        neg_chance /= (1 - step_chance) ** 5
    elif chain == 99:
        neg_chance /= (1 - step_chance) ** 10
    else:
        neg_chance /= (1 - step_chance)
    return neg_chance


class UiMethods:
    def __init__(self, counter_list):
        methods = CR.CounterRead('methods.txt')
        self.method_list = []
        self.chain = 1
        self.font = []
        for f in range(1, 101):
            self.font.append(("Helvetica", f"{f}", "bold"))

        for ind, line in enumerate(methods):
            if line != '':
                item = line.split(' ')
                self.method_list.append(PM.Method(counter_list[ind].id,
                                                  counter_list[ind].name,
                                                  counter_list[ind].value,
                                                  counter_list[ind].jump,
                                                  *item))

        self.root = Tk()

        self.mainFrame = Frame(self.root)
        self.mainFrame.pack()

        self.chance = Label(self.mainFrame, text=0, font=("Helvetica", "25"))
        self.chance.pack()

        self.root.overrideredirect(False)  # windowless
        self.root.wm_attributes("-topmost", True)

        self.root.geometry('+0+122')

        self.root.bind('<Button-1>', self.optionMenu)

    def optionMenu(self, _counter):
        def applyOption():
            # changing the counter values
            self.chain = int(set_count.get()) if set_count.get() else self.chain
            self.chance.config(text=f'{self.chance["text"].split(" - ")[0]} - {self.chain}')

        option_menu = Toplevel(self.root)

        Label(option_menu, text='set chain', font=self.font[20]).pack()
        set_count = Entry(option_menu, font=self.font[16], justify='center')
        set_count.pack()
        set_count.focus_force()

        button_frame = Frame(option_menu)
        button_frame.pack()

        cancel = Button(button_frame, text='CANCEL', font=self.font[16], command=option_menu.destroy)
        apply = Button(button_frame, text='APPLY', font=self.font[16], command=applyOption)

        cancel.grid(row=0, column=0, ipadx=8, sticky='w')
        apply.grid(row=0, column=1, ipadx=17, sticky='e')

    def update(self, counter: CounterClass.Counter, dec=False, chain_lost=False):
        # store the method for which values need to be calculated
        global cur_chance
        method = self.method_list[counter.id - 1].method_id
        if chain_lost:
            self.chain = 0
        elif dec:
            self.chain -= 1
        else:
            self.chain += 1

        # normal random encounter with odds store in method.odds method is stored in method_list
        if method == 0:
            cur_chance = 1 - (1 - 1 / self.method_list[counter.id - 1].odds) ** counter.value
            self.chance.config(text=f'{round(cur_chance * 100, 3)}%')

        elif method == 1:
            if not dec and not chain_lost:
                cur_chance = dexnavChanceInc(counter.value, self.method_list[counter.id - 1].odds, self.chain)

                self.method_list[counter.id - 1].odds = cur_chance

            if dec and not chain_lost:
                cur_chance = dexnavChanceDec(counter.value, self.method_list[counter.id - 1].odds, self.chain)

                self.method_list[counter.id - 1].odds = cur_chance

            if chain_lost:
                cur_chance = self.method_list[counter.id - 1].odds
                self.chain %= 100

            self.chance.config(text=f'{round((1 - cur_chance) * 100, 3)}% - {self.chain}')


if __name__ == '__main__':
    neg_chance_start = 1
    chain_start = 0
    for n in range(1, 1000):
        chain_start += 1
        neg_chance_start = dexnavChanceInc(n, neg_chance_start, chain_start)
        print(chain_start, neg_chance_start)
        chain_start %= 100
