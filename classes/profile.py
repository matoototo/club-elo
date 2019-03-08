class Profile:
    def update_elo (self, change):
        if (not self.constant): #used by engines with known strength, anchor
            self.history.append(self.elo)
            if (self.elo < 2100): #to adjust for k-factor changes as per USCF's logistic distribution 
                change = change*2
            elif (self.elo < 2400):
                change = change*1.5
            self.elo = round(self.elo+change, 2)
            self.history.append(self.elo)
            self.gameCounter = self.gameCounter+1
            return change
        else: return 0
    def __init__ (self, name, startElo, constant=False, history=[]):
        self.name = name
        self.elo = startElo
        self.constant = constant
        self.history = history
        self.gameCounter = len(history)