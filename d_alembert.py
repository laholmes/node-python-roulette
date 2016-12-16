import sys
import random

# startingFunds = float(sys.argv[1])
# wagerSize = float(sys.argv[2])
# wagerCount = float(sys.argv[3])
# daSampSize = float(sys.argv[4])

counter = 1
ret = 0.0
da_busts = 0.0
da_profits = 0.0

def rollDice():
    roll = random.randint(1,100)

    if roll <= 50:
        return False
    elif roll >= 51:
        return True

def dAlembert(funds,initial_wager,wager_count):
    global ret
    global da_busts
    global da_profits

    value = funds
    wager = initial_wager
    currentWager = 1
    previousWager = 1
    previousWagerAmount = initial_wager

    while currentWager <= wager_count:
        if previousWager == 1:
            if wager == initial_wager:
                pass
            else:
                wager -= initial_wager

            if rollDice():
                value += wager
                previousWagerAmount = wager
            else:
                value -= wager
                previousWager = 0
                previousWagerAmount = wager

                if value <= 0:
                    da_busts += 1
                    break

        elif previousWager == 0:
            wager = previousWagerAmount + initial_wager
            if(value - wager) <= 0:
                wager = value

            if rollDice():
                value += wager
                previousWager = 1
                previousWagerAmount = wager
            else:
                value -= wager
                previousWagerAmount = wager

                if value <= 0:
                    da_busts += 1
                    break

        currentWager += 1

    ret += value

    if value > funds:
        da_profits += 1

# while counter <= daSampSize:
#     dAlembert(startingFunds, wagerSize, wagerCount)
#     counter += 1

#     results = {
#         'totalInvested': daSampSize*startingFunds,
#         'totalReturn': ret,
#         'roi': ret - (daSampSize*startingFunds),
#         'bustRate': (da_busts/daSampSize) * 100.00,
#         'profitRate': (da_profits/daSampSize) * 100.00
#     }

# sys.stdout.write(str(results))
# print(str(results))
# sys.stdout.flush()
# sys.exit(0)

def simulate(startingFunds, wagerSize, wagerCount, daSampSize):
    counter = 1

    while counter <= daSampSize:
        dAlembert(startingFunds, wagerSize, wagerCount)
        counter += 1

    results = {
        'totalInvested': daSampSize*startingFunds,
        'totalReturn': ret,
        'roi': ret - (daSampSize*startingFunds),
        'bustRate': (da_busts/daSampSize) * 100.00,
        'profitRate': (da_profits/daSampSize) * 100.00
    }
    return results

