import json
from sqlalchemy import text
from Database.Database import Lore_Session
#from Database import Lore_Session

def get_etharus_date():
    eth_date = json.load(open('LoreKeeper\etharus_date.json'))
    #eth_date = json.load(open('/etc/LoreKeeper/etharus_date.json')) #-> Use on Server
    #date_parse = f"{eth_date['season']} {eth_date['date']}, {eth_date['year']}{eth_date['era']}"
    date_parse = [eth_date['season'],eth_date['date'],eth_date['year'],eth_date['era']]

    return date_parse

def get_party_funds():
    ap_query_text = text("Select id, CAST((pp*10) + gp + (CAST(sp AS float)/10) + (CAST(cp AS float)/100) AS float) as total, COUNT(AP_Member_Transactions.AP_id) as membercount, STRING_AGG(AP_Member_Transactions.Party_id, ',') as members FROM AP LEFT JOIN AP_Member_Transactions ON AP.id = AP_Member_Transactions.AP_id GROUP BY AP.id, AP.pp, AP.gp, AP.sp, AP.cp;")
    ap_query = Lore_Session.execute(ap_query_text).all()
    ar_query_text = text("Select id, CAST((pp*10) + gp + (CAST(sp AS float)/10) + (CAST(cp AS float)/100) AS float) as total, COUNT(AR_Member_Transactions.AR_id) as membercount, STRING_AGG(AR_Member_Transactions.Party_id, ',') as members FROM AR LEFT JOIN AR_Member_Transactions ON AR.id = AR_Member_Transactions.AR_id GROUP BY AR.id, ar.pp, ar.gp, ar.sp, ar.cp;")
    ar_query = Lore_Session.execute(ar_query_text).all()
    ar_sum = 0
    ap_sum = 0
    total_sum = 0

    for arq in ar_query:
        ar_sum += arq[1]

    for apq in ap_query:
        ap_sum += apq[1]

    total_sum = round(ar_sum - ap_sum,2)

    return total_sum

def get_active_party():
    query = text("SELECT id, name, active FROM Party WHERE active = 1;")
    results = Lore_Session.execute(query).all()

    return results

def get_ap_trans():
    ap_query_text = text("Select *, (total/CAST(membercount AS float)) as Split FROM (Select id, CAST(irl_date as DATE) as irl_date, ig_date, description, pp, gp, sp, cp, CAST(((pp*10) + gp + (CAST(sp AS float)/10) + (CAST(cp AS float)/100)) AS float) as total, payee, COUNT(AP_Member_Transactions.AP_id) as membercount, STRING_AGG(AP_Member_Transactions.Party_id, ',') as members FROM AP LEFT JOIN AP_Member_Transactions ON AP.id = AP_Member_Transactions.AP_id GROUP BY AP.id, AP.irl_date, AP.ig_date, AP.description, AP.pp, AP.gp, AP.sp, AP.cp, AP.payee) tbl ORDER BY id DESC;")
    ap_query = Lore_Session.execute(ap_query_text).all()
    names = []
    for apq in ap_query:
        split = apq[11].split(',')
        temp = ''
        i=0
        while i < len(split):
            temp += str((Lore_Session.execute(text(f"SELECT name FROM Party WHERE id = {split[i]}")).all())[0][0])
            if i == (len(split) - 1): 
                pass
            else:
                temp += ', '
            i += 1
        names.append(temp)
    return ap_query, names

def get_ap_trans_simple():
    ap_query_text = text("Select id, total, (total/CAST(membercount AS float)) as Split FROM (Select id, CAST(irl_date as DATE) as irl_date, ig_date, description, pp, gp, sp, cp, CAST(((pp*10) + gp + (CAST(sp AS float)/10) + (CAST(cp AS float)/100)) AS float) as total, payee, COUNT(AP_Member_Transactions.AP_id) as membercount, STRING_AGG(AP_Member_Transactions.Party_id, ',') as members FROM AP LEFT JOIN AP_Member_Transactions ON AP.id = AP_Member_Transactions.AP_id GROUP BY AP.id, AP.irl_date, AP.ig_date, AP.description, AP.pp, AP.gp, AP.sp, AP.cp, AP.payee) tbl;")
    ap_query = Lore_Session.execute(ap_query_text).all()

    return ap_query 

def get_specific_ap_trans(requested_id):
    ap_query_text = text(f"Select *, (total/CAST(membercount AS float)) as Split FROM (Select id, CAST(irl_date as DATE) as irl_date, ig_date, description, pp, gp, sp, cp, CAST(((pp*10) + gp + (CAST(sp AS float)/10) + (CAST(cp AS float)/100)) AS float) as total, payee, COUNT(AP_Member_Transactions.AP_id) as membercount, STRING_AGG(AP_Member_Transactions.Party_id, ',') as members FROM AP LEFT JOIN AP_Member_Transactions ON AP.id = AP_Member_Transactions.AP_id WHERE id = {requested_id} GROUP BY AP.id, AP.irl_date, AP.ig_date, AP.description, AP.pp, AP.gp, AP.sp, AP.cp, AP.payee) tbl;")
    ap_query = Lore_Session.execute(ap_query_text).all()
    names = []
    for apq in ap_query:
        split = apq[11].split(',')
        temp = ''
        i=0
        while i < len(split):
            temp += str((Lore_Session.execute(text(f"SELECT name FROM Party WHERE id = {split[i]}")).all())[0][0])
            if i == (len(split) - 1): 
                pass
            else:
                temp += ', '
            i += 1
        names.append(temp)
    return ap_query, names

def get_specific_ap_trans_simple(requested_id):
    ap_query_text = text(f"Select id, total, (total/CAST(membercount AS float)) as Split FROM (Select id, CAST(irl_date as DATE) as irl_date, ig_date, description, pp, gp, sp, cp, CAST(((pp*10) + gp + (CAST(sp AS float)/10) + (CAST(cp AS float)/100)) AS float) as total, payee, COUNT(AP_Member_Transactions.AP_id) as membercount, STRING_AGG(AP_Member_Transactions.Party_id, ',') as members FROM AP LEFT JOIN AP_Member_Transactions ON AP.id = AP_Member_Transactions.AP_id WHERE id = {requested_id} GROUP BY AP.id, AP.irl_date, AP.ig_date, AP.description, AP.pp, AP.gp, AP.sp, AP.cp, AP.payee) tbl;")
    ap_query = Lore_Session.execute(ap_query_text).all()

    return ap_query

def get_ar_trans():
    ar_query_text = text("Select *, (total/CAST(membercount AS float)) as Split FROM (Select id, CAST(irl_date as DATE) as irl_date, ig_date, description, pp, gp, sp, cp, CAST(((pp*10) + gp + (CAST(sp AS float)/10) + (CAST(cp AS float)/100)) AS float) as total, COUNT(AR_Member_Transactions.AR_id) as membercount, STRING_AGG(AR_Member_Transactions.Party_id, ',') as members FROM AR LEFT JOIN AR_Member_Transactions ON AR.id = AR_Member_Transactions.AR_id GROUP BY AR.id, AR.irl_date, ar.ig_date, ar.description, ar.pp, ar.gp, ar.sp, ar.cp) tbl ORDER BY id DESC;")
    ar_query = Lore_Session.execute(ar_query_text).all()
    names = []
    for arq in ar_query:
        split = arq[10].split(',')
        temp = ''
        i=0
        while i < len(split):
            temp += str((Lore_Session.execute(text(f"SELECT name FROM Party WHERE id = {split[i]}")).all())[0][0])
            if i == (len(split) - 1): 
                pass
            else:
                temp += ', '
            i += 1
        names.append(temp)
    
    return ar_query,names

def get_ar_trans_simple():
    ar_query_text = text("Select id, total, (total/CAST(membercount AS float)) as Split FROM (Select id, CAST(irl_date as DATE) as irl_date, ig_date, description, pp, gp, sp, cp, CAST(((pp*10) + gp + (CAST(sp AS float)/10) + (CAST(cp AS float)/100)) AS float) as total, COUNT(AR_Member_Transactions.AR_id) as membercount, STRING_AGG(AR_Member_Transactions.Party_id, ',') as members FROM AR LEFT JOIN AR_Member_Transactions ON AR.id = AR_Member_Transactions.AR_id GROUP BY AR.id, AR.irl_date, ar.ig_date, ar.description, ar.pp, ar.gp, ar.sp, ar.cp) tbl;")
    ar_query = Lore_Session.execute(ar_query_text).all()
    
    return ar_query

def get_specific_ar_trans(requested_id):
    ar_query_text = text(f"Select id, total, (total/CAST(membercount AS float)) as Split FROM (Select id, CAST(irl_date as DATE) as irl_date, ig_date, description, pp, gp, sp, cp, CAST(((pp*10) + gp + (CAST(sp AS float)/10) + (CAST(cp AS float)/100)) AS float) as total, COUNT(AR_Member_Transactions.AR_id) as membercount, STRING_AGG(AR_Member_Transactions.Party_id, ',') as members FROM AR LEFT JOIN AR_Member_Transactions ON AR.id = AR_Member_Transactions.AR_id WHERE id = {requested_id} GROUP BY AR.id, AR.irl_date, ar.ig_date, ar.description, ar.pp, ar.gp, ar.sp, ar.cp) tbl;")
    ar_query = Lore_Session.execute(ar_query_text).all()
    names = []
    for arq in ar_query:
        split = arq[10].split(',')
        temp = ''
        i=0
        while i < len(split):
            temp += str((Lore_Session.execute(text(f"SELECT name FROM Party WHERE id = {split[i]}")).all())[0][0])
            if i == (len(split) - 1): 
                pass
            else:
                temp += ', '
            i += 1
        names.append(temp)
    
    return ar_query,names

def get_specific_ar_trans_simple(requested_id):
    ar_query_text = text(f"Select *, (total/CAST(membercount AS float)) as Split FROM (Select id, CAST(irl_date as DATE) as irl_date, ig_date, description, pp, gp, sp, cp, CAST(((pp*10) + gp + (CAST(sp AS float)/10) + (CAST(cp AS float)/100)) AS float) as total, COUNT(AR_Member_Transactions.AR_id) as membercount, STRING_AGG(AR_Member_Transactions.Party_id, ',') as members FROM AR LEFT JOIN AR_Member_Transactions ON AR.id = AR_Member_Transactions.AR_id WHERE id = {requested_id} GROUP BY AR.id, AR.irl_date, ar.ig_date, ar.description, ar.pp, ar.gp, ar.sp, ar.cp) tbl;")
    ar_query = Lore_Session.execute(ar_query_text).all()
    
    return ar_query

def get_all_individual_funds():
    ap_trans = get_ap_trans_simple()
    ar_trans = get_ar_trans_simple()
    indiv_totals = []
    party_mems = get_active_party()

    for pm in party_mems:
        ap_indiv = 0
        ar_indiv = 0

        for apt in ap_trans:
            mem_trans = Lore_Session.execute(text(f"SELECT AP_id, Party_id FROM AP_Member_Transactions WHERE AP_id = {apt[0]} and Party_id = {pm[0]};")).all()
            if len(mem_trans) != 0:
                if pm[0] == mem_trans[0][1]:
                    ap_indiv += apt[2]

        for art in ar_trans:
            mem_trans = Lore_Session.execute(text(f"SELECT AR_id, Party_id FROM AR_Member_Transactions WHERE AR_id = {art[0]} and Party_id = {pm[0]};")).all()
            if len(mem_trans) != 0:
                if pm[0] == mem_trans[0][1]:
                    ar_indiv += art[2]


        indiv_totals += [[pm[1],round(ar_indiv-ap_indiv,2), pm[2]]]
    
    return indiv_totals

def get_individual_fund(member):
    ap_trans = get_ap_trans_simple()
    ar_trans = get_ar_trans_simple()
    indiv_total = []
    party_mem = Lore_Session.execute(text(f"SELECT id, name FROM Party WHERE name = '{member}';")).all()[0]
    ap_indiv = 0
    ar_indiv = 0

    for apt in ap_trans:
        mem_trans = Lore_Session.execute(text(f"SELECT AP_id, Party_id FROM AP_Member_Transactions WHERE AP_id = {apt[0]} and Party_id = {party_mem[0]};")).all()
        if len(mem_trans) != 0:
            if party_mem[0] == mem_trans[0][1]:
                ap_indiv += apt[2]

    for art in ar_trans:
        mem_trans = Lore_Session.execute(text(f"SELECT AR_id, Party_id FROM AR_Member_Transactions WHERE AR_id = {art[0]} and Party_id = {party_mem[0]};")).all()
        if len(mem_trans) != 0:
            if party_mem[0] == mem_trans[0][1]:
                ar_indiv += art[2]

    indiv_total += [party_mem[1],round(ar_indiv-ap_indiv,2)]
    
    return indiv_total

def get_magic_items():
    mi_query_text = text("SELECT * FROM Magic_Items ORDER BY id DESC")
    mi_query = Lore_Session.execute(mi_query_text).all()
    owner = []
    for mq in mi_query:
        if mq[9] != None:
            owner.append(['Party', Lore_Session.execute(text(f"SELECT name FROM Party WHERE id = {mq[9]}")).all()[0][0]])
        elif mq[10] != None:
            owner.append(['Ship', Lore_Session.execute(text(f"SELECT name FROM Ships WHERE id = {mq[9]}")).all()[0][0]])
        elif mq[11] != None:
            owner.append(['Crew', Lore_Session.execute(text(f"SELECT name FROM Crew WHERE id = {mq[9]}")).all()[0][0]])
        else:
            owner.append(['Party Stash', None])

    return mi_query, owner

def get_individual_magic_items(member):
    member_id = (Lore_Session.execute(text(f"SELECT id,name FROM Party WHERE name = '{member}'")).all()[0][0])
    mi_query_text = text(f"SELECT * FROM Magic_Items WHERE powner = {member_id} ORDER BY id DESC")
    mi_query = Lore_Session.execute(mi_query_text).all()

    return mi_query