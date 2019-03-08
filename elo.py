import os
import msvcrt
from texttable import Texttable
from classes.profile import Profile

def create_profile(name, elo, constant=False, history=[]):
    profile = Profile(name, elo, constant, history)
    profiles[name] = profile

def load_profiles():
    file = open("data", "r")
    data = file.readlines()
    for profile in data:
        history = []
        splitData = profile.split()
        name = splitData[0]
        elo = float(splitData[1])
        constant = splitData[2]
        if constant == "True":
            constant = True
        else:
            constant = False
        for i in range(4, int(splitData[3])+4):
            history.append(float(splitData[i]))
        create_profile(name, elo, constant, history)

def save_profiles():
    file = open("data", "w+")
    for name in profiles.keys():
        historyData = " ".join([str(x) for x in profiles[name].history])
        file.write(name + " " + str(profiles[name].elo) + " " + str(profiles[name].constant) + " " + str(profiles[name].gameCounter) + " " + historyData + "\n")

def expected(a, b): #expected score
    return 1/(1+10**((b-a)/400))

def calculate_change(exp, score, k=16): #exp = expected score
    return round(k*(score-exp),2)

def options(option=0):
    os.system("cls")
    if   option == 0:
        return "(1) Add game result\n(2) Add match result\n(3) Create profile\n(4) Delete profile\n(5) Show table\n(9) Save and exit\n(0) Menu"
    elif option == 1:
        first = str(input("First player: "))
        while first not in profiles:
            if first == "":
                print(options())
                return "Action cancelled"
            os.system("cls")
            print("Profile doesn't exist, try again")
            first = str(input("First player: "))
        second = str(input("Second player: "))
        while second not in profiles:
            if second == "":
                print(options())
                return "Action cancelled"
            os.system("cls")
            print("Profile doesn't exist, try again")
            second = str(input("Second player: "))
        os.system("cls")
        result = input("Result (from first player's perspective, 1/0.5/0): ")
        if result not in ["1", "0.5", "0"]:
            print(options())
            return "Action cancelled"
        else: result = float(result)
        change = calculate_change(expected(profiles[first].elo, profiles[second].elo), result)
        difference = [0, 0]
        difference[0], difference[1] = profiles[first].update_elo(change), profiles[second].update_elo(-change)
        print(options())
        return (str(first) + " " + str(round((profiles[first].elo-difference[0]), 2)) + " -> " + str(profiles[first].elo) + " (" + str(difference[0]) + ")\n" + 
                str(second) + " " + str(round((profiles[second].elo+difference[1]), 2)) + " -> " + str(profiles[second].elo) + " (" + str(-difference[1]) + ")")
    elif option == 2:
        first = str(input("First player: "))
        while first not in profiles:
            if first == "":
                print(options())
                return "Action cancelled"
            os.system("cls")
            print("Profile doesn't exist, try again")
            first = str(input("First player: "))
        second = str(input("Second player: "))
        while second not in profiles:
            if second == "":
                print(options())
                return "Action cancelled"
            os.system("cls")
            print("Profile doesn't exist, try again")
            second = str(input("Second player: "))
        wins = int(input("Number of wins (for first player): "))
        draws = int(input("Number of draws: "))
        losses = int(input("Number of losses (for first player): "))
        difference = [0, 0]
        if wins >= losses:
            for i in range(wins-losses):
                change = calculate_change(expected(profiles[first].elo, profiles[second].elo), 1)
                difference[0] += profiles[first].update_elo(change)
                difference[1] += profiles[second].update_elo(-change)
        else:
            for i in range(losses-wins):
                change = calculate_change(expected(profiles[first].elo, profiles[second].elo), 0)
                difference[0] += profiles[first].update_elo(change)
                difference[1] += profiles[second].update_elo(-change)
        for i in range(draws):
                change = calculate_change(expected(profiles[first].elo, profiles[second].elo), 0.5)
                difference[0] += profiles[first].update_elo(change)
                difference[1] += profiles[second].update_elo(-change)
        print(options())
        return (str(first) + " " + str(round((profiles[first].elo-difference[0]), 2)) + " -> " + str(profiles[first].elo) + " (" + str(round(difference[0], 2)) + ")\n" + 
                str(second) + " " + str(round((profiles[second].elo-difference[1]), 2)) + " -> " + str(profiles[second].elo) + " (" + str(round(difference[1], 2)) + ")")
    elif option == 3:
        name = str(input("Name: "))
        while name in profiles or name == "":
            if name == "":
                print(options())
                return "Profile creation cancelled"
            os.system("cls")
            print("Profile already exists, try again")
            name = str(input("Name: "))
        elo = float(input("Elo: "))
        constant = int(input("Constant elo? (1 - True, 0 - False): "))
        if constant == 1: constant = True
        else: constant = False
        create_profile(name, elo, constant)
        print(options())
        return "Profile creation successful"
    elif option == 4:
        name = str(input("Name: "))
        if name in profiles:
            del profiles[name]
            print(options())
            return "Profile deletion successful"
        else:
            print(options())
            return "Profile doesn't exist"
    elif option == 5:
        if (profiles != {}):
            names = []
            ratings = []
            table = Texttable()
            for profile in profiles:
                names.append(profile)
                ratings.append(profiles[profile].elo)
            ratings, names = (list(t) for t in zip(*sorted(zip(ratings, names))))
            ratings = ratings[::-1]
            names = names[::-1]
            table.header(["Player", "Elo"])
            for i in range(len(names)):
                table.add_row([names[i], ratings[i]])
            print(options())
            return table.draw()
        else:
            print(options())
            return "No profiles exist"
    elif option == 9:
        save_profiles()
        exit()

if __name__ == "__main__":
    if "profiles" not in locals() and "profiles" not in globals():
        profiles = {}
        load_profiles()
    option = 0
    while True:
        print(options(int(option)))
        option = msvcrt.getch()
        while (not option.isdigit() or int(option) not in [0, 1, 2, 3, 4, 5, 9]):
            print(options())
            print("Option does not exist")
            option = msvcrt.getch()