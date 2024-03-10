from sqlalchemy import text
from Database.Database import Lore_Session
#from Database import Lore_Session

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


def get_ap_trans():
    ap_query_text = text("Select *, (total/CAST(membercount AS float)) as Split FROM (Select id, CAST(irl_date as DATE) as irl_date, ig_date, description, pp, gp, sp, cp, CAST(((pp*10) + gp + (CAST(sp AS float)/10) + (CAST(cp AS float)/100)) AS float) as total, payee, COUNT(AP_Member_Transactions.AP_id) as membercount, STRING_AGG(AP_Member_Transactions.Party_id, ',') as members FROM AP LEFT JOIN AP_Member_Transactions ON AP.id = AP_Member_Transactions.AP_id GROUP BY AP.id, AP.irl_date, AP.ig_date, AP.description, AP.pp, AP.gp, AP.sp, AP.cp, AP.payee) tbl;")
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
    ar_query_text = text("Select *, (total/CAST(membercount AS float)) as Split FROM (Select id, CAST(irl_date as DATE) as irl_date, ig_date, description, pp, gp, sp, cp, CAST(((pp*10) + gp + (CAST(sp AS float)/10) + (CAST(cp AS float)/100)) AS float) as total, COUNT(AR_Member_Transactions.AR_id) as membercount, STRING_AGG(AR_Member_Transactions.Party_id, ',') as members FROM AR LEFT JOIN AR_Member_Transactions ON AR.id = AR_Member_Transactions.AR_id GROUP BY AR.id, AR.irl_date, ar.ig_date, ar.description, ar.pp, ar.gp, ar.sp, ar.cp) tbl;")
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

def get_individual_funds():
    ap_trans = get_ap_trans_simple()
    ar_trans = get_ar_trans_simple()
    indiv_totals = []
    party_mems = Lore_Session.execute(text("SELECT id, name, active FROM Party;")).all()

    for pm in party_mems:
        ap_indiv = 0
        ar_indiv = 0
        for apt in ap_trans:
            mem_trans = Lore_Session.execute(text(f"SELECT AP_id, Party_id FROM AP_Member_Transactions WHERE AP_id = {apt[0]};"))
            for mt in mem_trans:
                if pm[0] == mt[1]:
                    ap_indiv += apt[2]
        for art in ar_trans:
            mem_trans = Lore_Session.execute(text(f"SELECT AR_id, Party_id FROM AR_Member_Transactions WHERE AR_id = {art[0]};"))
            for mt in mem_trans:
                if pm[0] == mt[1]:
                    ar_indiv += art[2]
        indiv_totals += [[pm[1],round(ar_indiv-ap_indiv,2), pm[2]]]
    return indiv_totals

