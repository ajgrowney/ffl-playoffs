
class Player:
    def __init__(self, name_inp, team_inp, position_inp):
        name = name_inp
        team = team_inp
        position = position_inp

class Quarterback(Player):
    def __init__(self,name_inp,team_inp, position_inp):
        Player.__init__(name_inp,team_inp,position_inp)


class RunningBack(Player):
    def __init__(self,name_inp,team_inp, position_inp):
        Player.__init__(name_inp,team_inp,position_inp)
        

class WideReceiver(Player):
    def __init__(self,name_inp,team_inp, position_inp):
        Player.__init__(name_inp,team_inp,position_inp)


class TightEnd(Player):
    def __init__(self,name_inp,team_inp, position_inp):
        Player.__init__(name_inp,team_inp,position_inp)

class Kicker(Player):
    def __init__(self,name_inp,team_inp, position_inp):
        Player.__init__(name_inp,team_inp,position_inp)

class DefenseSpecialTeams():
    def __init__(self,team_inp):
        team = team_inp
