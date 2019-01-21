from CoC_API import CoC
from discord.ext import commands
import discord
from configparser import ConfigParser
from datetime import datetime
from discord import Embed
import asyncio


config = ConfigParser(allow_no_value=True)
config.read('carlaConfig.ini')
discord_client = commands.Bot(command_prefix = config['Bot']['Bot_Prefix'])
discord_client.remove_command("help")
coc = CoC(config['Bot']['CoC_Token'])

def def_val(localLvl, remoteLvl, stars):
    dips = [0, 20, 50, 100]
    same = [0, 33, 66, 100]
    if int(localLvl) == int(remoteLvl):
        return same[stars], "<-- Normal"
    if int(localLvl) < int(remoteLvl):
        return dips[stars], "<-- Dip"
    else:
        return "@Goku"

def normal_attack(localLvl, remoteLvl, stars, percentage):
    if stars == 0:
        return 0, f"<-- {localLvl}v{remoteLvl} Fail"
    elif stars == 1:
        if int(percentage) <= 49:
            return percentage, f"<-- {localLvl}v{remoteLvl} Cap"
        else:
            return 49, f"<-- {localLvl}v{remoteLvl} Cap"
    elif stars == 2:
        return percentage, f"<-- {localLvl}v{remoteLvl} 2Star"
    elif stars == 3:
        return 100, f"<-- {localLvl}v{remoteLvl} Max"

def att_val(localLvl, remoteLvl, stars, percentage, clan_name):
    # Same th vs same th
    if int(localLvl) == int(remoteLvl):
        return normal_attack(localLvl, remoteLvl, stars, percentage)

    # 9 vs X
    if int(localLvl) == 9:
        # Against TH10
        if int(remoteLvl) == 10:
            if stars == 3:
                return 125, "<-- 9v10 MAX"
            else:
                return normal_attack(localLvl, remoteLvl, stars, percentage)
        # Against  TH11 or TH12
        if int(remoteLvl) == 11 or int(remoteLvl) == 12:
            if stars == 0:
                return 0, f"<-- {localLvl}v{remoteLvl} Fail"
            elif stars == 1:
                if int(percentage) <= 49:
                    return percentage, f"<-- {localLvl}v{remoteLvl} Cap"
                else:
                    return 49, f"<-- {localLvl}v{remoteLvl} Cap"
            elif stars == 2:
                return 100, f"<-- {localLvl}v{remoteLvl} Reach"
            elif stars == 3:
                return 125, f"<-- {localLvl}v{remoteLvl} Reach"

    #10 v X
    if int(localLvl) == 10:
        # Against TH 12
        if int(remoteLvl) == 12:
            if stars == 0:
                return 0, f"<-- {localLvl}v{remoteLvl} Fail"
            elif stars == 1:
                if int(percentage) <= 49:
                    return percentage, f"<-- {localLvl}v{remoteLvl} Cap"
                else:
                    return 49, f"<-- {localLvl}v{remoteLvl} Cap"
            elif stars == 2:
                return 100, f"<-- {localLvl}v{remoteLvl} Reach"
            elif stars == 3:
                return "@Goku"
        
        # Against TH 11
        if int(remoteLvl) == 11:
            if stars == 0:
                return 0, f"<-- {localLvl}v{remoteLvl} Fail"
            elif stars == 1:
                if int(percentage) <= 49:
                    return percentage, f"<-- {localLvl}v{remoteLvl} Cap"
                else:
                    return 49, f"<-- {localLvl}v{remoteLvl} Cap"
            elif stars == 2:
                return int(percentage) + 10, f"<-- {localLvl}v{remoteLvl} +10"
            elif stars == 3:
                return 125, f"<-- {localLvl}v{remoteLvl} Reach"
    
    if int(localLvl) == 11 and clan_name == 'Reddit Elephino':
        # Against TH 12
        localLvl = 10.5
        if int(remoteLvl) == 12:
            if stars == 0:
                return 0, f"<-- {localLvl}v{remoteLvl} Fail"
            elif stars == 1:
                if int(percentage) <= 49:
                    return percentage, f"<-- {localLvl}v{remoteLvl} Cap"
                else:
                    return 49, f"<-- {localLvl}v{remoteLvl} Cap"
            elif stars == 2:
                return 100, f"<-- {localLvl}v{remoteLvl} Reach"
            elif stars == 3:
                return 125, f"<-- {localLvl}v{remoteLvl} Reach"
        
        # Against TH 11
        if int(remoteLvl) == 11:
            if stars == 0:
                return 0, f"<-- {localLvl}v{remoteLvl} Fail"
            elif stars == 1:
                if int(percentage) <= 49:
                    return percentage, f"<-- {localLvl}v{remoteLvl} Cap"
                else:
                    return 49, f"<-- {localLvl}v{remoteLvl} Cap"
            elif stars == 2:
                return int(percentage) + 10, f"<-- {localLvl}v{remoteLvl} +10"
            elif stars == 3:
                return 125, f"<-- {localLvl}v{remoteLvl} Reach"
    
    if int(localLvl) == 11:
        if int(remoteLvl) == 12:
            if stars == 3:
                return 125, f"<-- {localLvl}v{remoteLvl} Reach"
            else:
                return normal_attack(localLvl, remoteLvl, stars, percentage)


    else:
        return "@Goku", "<-- No definition"
            

def funk(x):
    return x['name'].lower()

@discord_client.event
async def on_ready():
    print(f'\n\nLogged in as: {discord_client.user.name} - {discord_client.user.id}\nVersion: {discord.__version__}\n')
    await discord_client.change_presence(status=discord.Status.online, activity=discord.Game("Pfft"))

@discord_client.command()
async def stop(ctx):
    await discord_client.logout()



@discord_client.command()
async def dump(ctx, clan, day):
    if clan.title() in config['Clan Tags'].keys():
        # Vars
        clan_tag = config['Clan Tags'][clan.title()]
        res = coc.get_clanLeagueGroup(clan_tag)
        count = 0
        all_tags = []

        if day == "all":
            all_tags = [ battle for war_day in res.json()['rounds'] for battle in war_day['warTags'] if battle != "#0"]
        elif day.isdigit():
            if int(day) - 1 in range(0, 7):
                all_tags = [ battle for battle in res.json()['rounds'][int(day) - 1]['warTags'] ]
                count = int(day) - 1
            else:
                await ctx.send("Date out of range.")
                return
        else:
            await ctx.send("Error.")
            return

        if len(all_tags) == 0:
            await ctx.send(f"No data has returned for day {count}. Please try again later.")
            return

        for warTag in all_tags:
            ress = coc.get_clanLeagueWars(warTag)
            if ress.json()['state'] == 'warEnded':
                found = False
                side = ''
                if ress.json()['clan']['tag'] == clan_tag:
                    found = True
                    side = 'clan'

                elif ress.json()['opponent']['tag'] == clan_tag:
                    found = True
                    side = 'opponent'
                if found:
                    count +=1

                    if side == 'clan':
                        opp = 'opponent'
                    elif side == 'opponent':
                        opp = 'clan'

                    tm = datetime.strptime(ress.json()['warStartTime'].split('T')[0], "%Y%m%d")
                    tmm = tm.strftime("%d %b %Y")
                    tmmm = f"{ress.json()[side]['name']} vs {ress.json()[opp]['name']}\nWar Day: {count}"


                    desc = (f"Attacks: {ress.json()[side]['attacks']}/15\n"
                    f"Total Stars: {ress.json()[side]['stars']}\n"
                    f"{tmm}")

                    embed = Embed(color=0x8A2BE2, title = tmmm, description = desc)
                    await ctx.send(embed = embed)
                    output =''
                    enemyList = [ (enemy['tag'],enemy['townhallLevel']) for enemy in ress.json()[opp]['members'] ]
                    teamList = ress.json()[side]['members']
                    teamList.sort(key=funk) 
                    for user in teamList:
                        if 'attacks' in user.keys() or 'bestOpponentAttack' in user.keys():
                            output += ("------------------------\n")
                            output += (f"User:    {user['name']}\n")
                            output += (f"Tag:     {user['tag']}\n")
                            output += (f"THlvl:   {user['townhallLevel']}\n")

                            if 'attacks' in user.keys():
                                localLvl = user['townhallLevel']
                                remoteLvl = [ value[1] for value in enemyList if value[0] == user['attacks'][0]['defenderTag'] ][0]
                                output += "    ---ATTACK---\n"
                                output += (f"     {user['townhallLevel']} VS {[ value[1] for value in enemyList if value[0] == user['attacks'][0]['defenderTag'] ][0]}\n")
                                output += (f"     Attack:  {user['attacks'][0]['destructionPercentage']}%\n")
                                output += (f"     Stars:   {user['attacks'][0]['stars']}\n")
                                output += (f"     Value:   {att_val(localLvl, remoteLvl, user['attacks'][0]['stars'], user['attacks'][0]['destructionPercentage'], ress.json()[side]['name'])}\n")

                            else:
                                output += "    ---ATTACK---\n"
                                output += (f"     Attack:  0%\n")
                                output += (f"     Stars:   0\n")
                                output += (f"     Value:   0\n")

                            if 'bestOpponentAttack' in user.keys():
                                output += "    ---DEFENSE---\n"
                                localLvl = user['townhallLevel']
                                remoteLvl = [ value[1] for value in enemyList if value[0] == user['bestOpponentAttack']['attackerTag'] ][0]
                                output += (f"     {localLvl} VS {remoteLvl}\n")
                                output += (f"     Defense: {user['bestOpponentAttack']['destructionPercentage']}%\n")
                                output += (f"     Stars:   {user['bestOpponentAttack']['stars']}\n")
                                output += (f"     Value:   {def_val(localLvl, remoteLvl, user['bestOpponentAttack']['stars'])}\n")
                                
                            else:
                                output += "    ---DEFENSE---\n"
                                output += (f"     Defense: 0%\n")
                                output += (f"     Stars:   0\n")
                                output += (f"     Value:   0\n")
                            
                            if len(output) >= 1600:
                                await ctx.send(f"```{output}```")
                                output = ''

                        else:
                            continue
                    await ctx.send(f"```{output}```")
@dump.error 
async def dump_handler(ctx, error):
    await ctx.send(embed = discord.Embed(title="ERROR", description=error.__str__(), color=0xFF0000))                   


@discord_client.command()
async def scoresheet(ctx, clan):
    if clan.title() in config['Clan Tags'].keys():
        clan_tag = config['Clan Tags'][clan.title()]
        res = coc.get_clanLeagueGroup(clan_tag)
        count = 0
        all_tags = [ battle for war_day in res.json()['rounds'] for battle in war_day['warTags'] if battle != "#0"]

        scoreDict = [] # Dict with all of our data
        for warTag in all_tags:
            ress = coc.get_clanLeagueWars(warTag)
            if ress.json()['state'] == 'warEnded':
                found = False
                side = ''
                if ress.json()['clan']['tag'] == clan_tag:
                    found = True
                    side = 'clan'

                elif ress.json()['opponent']['tag'] == clan_tag:
                    found = True
                    side = 'opponent'

                if found:
                    count +=1       # Keeps track of the days

                    if side == 'clan':
                        opp = 'opponent'
                    elif side == 'opponent':
                        opp = 'clan'

                    tm = datetime.strptime(ress.json()['warStartTime'].split('T')[0], "%Y%m%d")
                    tmm = tm.strftime("%d %b %Y")


                    output =''
                    enemyList = [ (enemy['tag'],enemy['townhallLevel']) for enemy in ress.json()[opp]['members'] ]
                    teamList = ress.json()[side]['members']
                    teamList.sort(key=funk)

                    # Default dictionary
                    scoreDict.append({
                        "Day" : count,
                        "Date" : tmm,
                        "Home" : ress.json()[side]['name'],
                        "Away" : ress.json()[opp]['name'],
                        "Scores" : []
                    })

                    index = len(scoreDict) - 1
                    for user in teamList:
                        if 'attacks' in user.keys() or 'bestOpponentAttack' in user.keys():
                            # user['name']
                            # user['tag']
                            # user['townhallLevel']

                            if 'attacks' in user.keys():
                                localLvl = user['townhallLevel']
                                remoteLvl = [ value[1] for value in enemyList if value[0] == user['attacks'][0]['defenderTag'] ][0]

                                attackScore = att_val(localLvl, remoteLvl, user['attacks'][0]['stars'], user['attacks'][0]['destructionPercentage'], ress.json()[side]['name'])[0]

                            else:
                                attackScore = 0

                            if 'bestOpponentAttack' in user.keys():
                                localLvl = user['townhallLevel']
                                remoteLvl = [ value[1] for value in enemyList if value[0] == user['bestOpponentAttack']['attackerTag'] ][0]
                                defenseScore = def_val(localLvl, remoteLvl, user['bestOpponentAttack']['stars'])[0]
                                
                            else:
                                defenseScore = 0
                            
                            scoreDict[index]['Scores'].append({
                                "Name" : user['name'],
                                "Tag"  : user['tag'],
                                "TH"   : user['townhallLevel'],
                                "Day"  : count,
                                "Att"  : attackScore,
                                "Def"  : defenseScore
                            })
                            

                        else:
                            continue
        folks = []
        for day in scoreDict:
            for user in day['Scores']:
                if (user['Name'],user['Tag']) not in folks:
                    folks.append((user['Name'],user['Tag']))

        scoresheet = []
        for user in folks:
            scoresheet.append({
                "Name" : user[0],
                "Tag": user[1],
                "Scores" : []
            })

        for user in scoresheet:
            for day in scoreDict:
                for clanmate in scoreDict['Scores']:
                    if user['Tag'] == clanmate['Tag']:
                        user['Scores'].append({
                            "Day" : 
                        })


@scoresheet.error 
async def scoresheet_handler(ctx, error):
    await ctx.send(embed = discord.Embed(title="ERROR", description=error.__str__(), color=0xFF0000))  


if __name__ == "__main__":
    discord_client.run(config['Bot']['Bot_Token'])