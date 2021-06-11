class Party:
    def __init__(self, name, leader):
        self.name = name
        self.objective = ""
        self.head = leader
        self.manifest = {}
        self.memberint = 1
    
    #Add member to party
    def addMember(self, memberNode, memberID):
        #Switch cases to activate certain based on number of members.
        memberCases = {
            1: self.setMember,
            2: self.setMember,
            3: self.setMember,
        }
        ptsize = self.memberint
        func = memberCases.get(ptsize, lambda: None)
        return func(memberNode, memberID)
    
    #Functions for setting members, used by addMember switch.
    def setMember(self, memberNode, memberID):
        self.manifest[memberID] = memberNode
        self.memberint = self.memberint + 1
        return self

    #Functions for removing members, used by removeMember switch.
    def removeMember(self, memberID):
        del self.manifest[memberID]
        self.memberint = self.memberint - 1
        return self
    
    #Swaps leader role with user in manifest
    def changeLead(self, memberID):
        self.head = self.manifest[memberID]
        return self
    
    #Set objective
    def makeObjective(self, objective):
        self.objective = objective
        return self



