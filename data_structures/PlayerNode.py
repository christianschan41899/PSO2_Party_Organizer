class PlayerNode:
    def __init__(self, username, id, mentionstr):
        self.user = username
        self.id = id
        self.mention = mentionstr
        self.partyid = None
    
    #Joining a party
    def changePartyID(self, partyID):
        self.partyid = partyID
        return self
    
