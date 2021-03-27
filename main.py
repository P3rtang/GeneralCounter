import CounterReadClass as CR
import CounterClass as CC
import UI as UI

counters = CR.CounterRead('counters.txt')
counterList = []
for line in counters:
    item = line.split(' ')
    print(item)
    if item[0]:
        counterList.append(CC.Counter(*item[:4]))

# gui_chance = UIM.UiMethods()
gui = UI.Ui(counterList)
