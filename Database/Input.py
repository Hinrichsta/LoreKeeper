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
            json.dump(eth_date, outfile)
        return "Success"

def set_ap_transaction(trans):
    if trans[6] == 'Party':
        party_query = text("SELECT id FROM Party WHERE active = 1;")
    else:
        party_query = text(f"SELECT id FROM Party WHERE name = {trans[6]}")
    
    active_party = Lore_Session.execute(party_query).all()
    party_ids = []
    for ap in active_party:
        party_ids.append(ap[0])
    
    eth_date = get_etharus_date()
    ap_insert = text(f"INSERT INTO AP (irl_date, ig_date, description, pp, gp, sp, cp, payee) VALUES ('{date.today()}', '{eth_date}', '{trans[0]}', {trans[1]}, {trans[2]}, {trans[3]}, {trans[4]}, '{trans[5]}')")
    ap_query = text("SELECT id FROM  AP WHERE id = (SELECT MAX(id)  FROM AP)")
    Lore_Session.execute(ap_insert)
    ap_id = Lore_Session.execute(ap_query).all()[0]
    for pid in party_ids:
        Lore_Session.execute(text(f"INSERT INTO AP_Member_Transactions(AP_id, Party_id) VALUES({ap_id[0]},{pid})"))

    Lore_Session.commit()
    

def set_ar_transaction(trans):
    if trans[6] == 'Party':
        party_query = text("SELECT id FROM Party WHERE active = 1;")
    else:
        party_query = text(f"SELECT id FROM Party WHERE name = {trans[6]}")
    
    active_party = Lore_Session.execute(party_query).all()
    party_ids = []
    for ap in active_party:
        party_ids.append(ap[0])
    
    eth_date = get_etharus_date()
    ar_insert = text(f"INSERT INTO AR (irl_date, ig_date, description, pp, gp, sp, cp) VALUES ('{date.today()}', '{eth_date}', '{trans[0]}', {trans[1]}, {trans[2]}, {trans[3]}, {trans[4]})")
    ar_query = text("SELECT id FROM  AR WHERE id = (SELECT MAX(id)  FROM AR)")
    Lore_Session.execute(ar_insert)
    ar_id = Lore_Session.execute(ar_query).all()[0]
    for pid in party_ids:
        Lore_Session.execute(text(f"INSERT INTO AR_Member_Transactions(AR_id, Party_id) VALUES({ar_id[0]},{pid})"))

    Lore_Session.commit()