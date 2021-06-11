import discord
import random
from discord.ext import commands
from data_structures.PlayerNode import PlayerNode
from data_structures.Party import Party

#Will store all parties created
party_dict = {}
partied_users = {}

#Commands related to parties
class PartyCMNDs(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #Create party
    @commands.command()
    async def mkpt(self, context, *, ptName):
        userid = context.author.id
        if userid in partied_users:
            await context.send("You are already in a party!")
        else:
            leader = PlayerNode(context.author.display_name, context.author.id, context.author.mention)
            new_pt = Party(ptName, leader)
            new_pt.setMember(leader, userid)
            leader.changePartyID(userid)
            party_dict[userid] = new_pt
            partied_users[userid] = leader
            await context.send(f'Party "{ptName}" created!')
    
    #See your party
    @commands.command()
    async def mypt(self, context):
        userid = context.author.id
        if userid in partied_users:
            currentpt = party_dict[userid]
            if userid in currentpt.manifest:
                message_string = f'Your party is "{currentpt.name}" \nMembers are:'
                for key in currentpt.manifest:
                    message_string = message_string + f"\n-{currentpt.manifest[key].user}"
                await context.send(message_string)
        else:
            await context.send("You do not belong to a party! Make one with '$mkpt' command!")
    
    #Join party another user has joined. If full or you are in another party, send a message
    @commands.command()
    async def joinpt(self, context, *, mention):
        userid = int(mention[3:-1])
        if context.author.id in partied_users:
            await context.send("You are already in a party!")
        elif userid not in partied_users:
            await context.send("That user does not currently belong to a party!")
        else:
            user = partied_users[userid]
            currentpt = party_dict[user.partyid]
            if currentpt.memberint >= 4:
                await context.send(f'"{currentpt.name}" is full!')
            else:
                newMember = PlayerNode(context.author.display_name, context.author.id, context.author.mention)
                currentpt.addMember(newMember, context.author.id)
                partied_users[context.author.id] = context.author.display_name
                await context.send(f'{context.author.mention} joined "{currentpt.name}".')
    
    #disband party
    @commands.command()
    async def disband(self, context):
        authorid = context.author.id
        if authorid in party_dict:
            for key in party_dict[authorid].manifest:
                #Both the manifest and partied users use the member id so it should be ok to do this.
                del partied_users[key]
            del party_dict[authorid]
            await context.send("Party disbanded!")
        else:
            await context.send("You are not currently leading any party you can disband!")

    #Leave party
    @commands.command()
    async def leavept(self, context):
        authorid = context.author.id
        if authorid in partied_users:
            user = partied_users[authorid]
            currentpt = party_dict[user.partyid]
            #If author is the only party member, delete the reference to the party in dictionary
            if currentpt.memberint == 1:
                del party_dict[authorid]
            elif currentpt.head.id == authorid:
                #Remove author from party
                currentpt = party_dict[authorid]
                currentpt.removeMember(authorid)
                #Select random leader from IDs that exist as manifest keys and change lead using that id
                newLeaderID = random.choice(currentpt.manifest.keys())
                currentpt.changeLead(newLeaderID)
                #Since parties in party_dict are placed according to leader's user id, add a new 
                #entry with the new leader id as the key and delete the older entry
                party_dict[newLeaderID] = currentpt
                del party_dict[authorid]
                #Since the party has a new id and party members store that id, change their partyid
                for key in currentpt.manifest:
                    currentpt.manifest[key].changePartyID(newLeaderID)
            else:
                party_dict[authorid].removeMember(authorid)
            user.changePartyID(None)
            del partied_users[authorid]
            await context.send(f'Left your party!')
        else:
            await context.send("You do not currently have a party to leave from!")
    
    #Swap leaders
    @commands.command()
    async def swaplead(self, context, *, mention):
        userid = int(mention[3:-1])
        authorid = context.author.id
        if (authorid in party_dict) and (userid in party_dict[authorid].manifest):
            #Get author's lead party and swap leaders using the built in function
            currentpt = party_dict[authorid]
            currentpt.changeLead(userid)
            #Since parties in party_dict are placed according to leader's user id, add a new 
            #entry with the new leader id as the key and delete the older entry
            party_dict[userid] = currentpt
            del party_dict[authorid]
            #Since the party has a new id and party members store that id, change their partyid
            for key in currentpt.manifest:
                currentpt.manifest[key].changePartyID(userid)
            await context.send(f"{mention} is now the party leader.")
        else:
            await context.send("That user is not in your party!")
    
    @commands.command()
    async def setObjective(self, context, *, objective):
        authorid = context.author.id
        if authorid in party_dict:
            party_dict[authorid].makeObjective(objective)
            await context.send(f"Objective for party: {objective} set")
        else:
            await context.send("You need to be a party leader to set the party's objective.")
    
    @commands.command()
    async def sortie(self, context):
        authorid = context.author.id
        if authorid in party_dict:
            currentpt = party_dict[authorid]
            message_string = f'{context.author.display_name} requesting sortie.\nMISSION: {currentpt.objective}\n'
            for key in currentpt.manifest:
                message_string = message_string + f"{currentpt.manifest[key].mention}"
            message_string = message_string + " requesting ready up."
            await context.send(message_string)
        else:
            await context.send("No party to sortie with.")


#Disbands party if leaver is last person (i.e. the leader)
#Left outside class because it doesn't affect it, only some variables in its container scope.

def setup(client):
    client.add_cog(PartyCMNDs(client))