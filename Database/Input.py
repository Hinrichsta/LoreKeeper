import json
from sqlalchemy import text, insert
from Database.Database import Lore_Session, AP, AP_Members, AR, AR_Members
from Database.Parse import get_etharus_date
#from Database import Lore_Session, AP, AP_Members, AR, AR_Members
#from Parse import get_etharus_date
from datetime import date

def set_etharus_date(season,date,year):
    seasons = ('Spring', 'Summer', 'Fall', 'Autumn', 'Winter')
    if season.casefold() not in (s.casefold() for s in seasons):
        return "Error: Season"
    elif int(date) > 92:
        return "Error: Date"
    else:
        eth_date = {
            "season": season,
            "date": date,
            "year": year,
            "era": "AG"
        }
        
        with open('LoreKeeper\etharus_date.json', 'w') as outfile:
        #with open('/etc/LoreKeeper/etharus_date.json', 'w') as outfile: -> Use on Server
            json.dump(eth_date, outfile)
        return "Success"

def set_ap_transaction(description, platinum, gold, silver, copper, member, payee):
    if member == 'Party':
        party_query = text("SELECT id FROM Party WHERE active = 1;")
    else:
        party_query = text(f"SELECT id, name FROM Party WHERE name = '{member}'")
    
    active_party = Lore_Session.execute(party_query).all()
    party_ids = []
    for ap in active_party:
        party_ids.append(ap[0])
    
    eth_date = get_etharus_date()
    ap_insert = text(f"INSERT INTO AP (irl_date, ig_date, description, pp, gp, sp, cp, payee) OUTPUT INSERTED.id, INSERTED.description VALUES ('{date.today()}', '{eth_date}', '{description}', {platinum}, {gold}, {silver}, {copper}, '{payee}')")

    result = Lore_Session.execute(ap_insert).all()[0]
    for pid in party_ids:
        Lore_Session.execute(text(f"INSERT INTO AP_Member_Transactions(AP_id, Party_id) VALUES({result[0]},{pid})"))

    Lore_Session.commit()

    return result
    
def set_ar_transaction(description, platinum, gold, silver, copper, member):
    if member == 'Party':
        party_query = text("SELECT id FROM Party WHERE active = 1;")
    else:
        party_query = text(f"SELECT id, name FROM Party WHERE name = '{member}'")
    
    active_party = Lore_Session.execute(party_query).all()
    party_ids = []
    for ap in active_party:
        party_ids.append(ap[0])
    
    eth_date = get_etharus_date()
    ar_insert = text(f"INSERT INTO AR (irl_date, ig_date, description, pp, gp, sp, cp) OUTPUT INSERTED.id, INSERTED.description VALUES ('{date.today()}', '{eth_date}', '{description}', {platinum}, {gold}, {silver}, {copper})")

    result = Lore_Session.execute(ar_insert).all()[0]
    for pid in party_ids:
        Lore_Session.execute(text(f"INSERT INTO AR_Member_Transactions(AR_id, Party_id) VALUES({result[0]},{pid})"))

    Lore_Session.commit()

    return result

def deposit_magic_item(name, notes, status, rarity=None, maker=None, link=None, party_owner=None, ship_owner=None, crew_owner=None):
    column = ''
    owner = ''
    if party_owner != None:
        column = 'powner'
        owner = party_owner
    elif ship_owner != None:
        column = 'showner'
        owner = ship_owner
    elif crew_owner != None:
        column = 'cowner'
        owner = crew_owner
    else:
        pass

    mi_insert = text(f"INSERT INTO Magic_Items (irl_date, ig_date, name, notes, rarity, maker, link, status, {{column}}) OUTPUT INSERTED.id, INSERTED.name VALUES('{date.today()}', '{eth_date}', '{name}', '{notes}', '{rarity}', '{maker}', '{link}', '{status}')")
    eth_date = get_etharus_date()

    results = Lore_Session.execute(mi_insert).all()[0]
    Lore_Session.commit()

    return results