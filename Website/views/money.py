from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import text
import json
from Database.Database import Lore_Session

money = Blueprint('money', __name__)

@money.route('/')
def home():

    return render_template("home.html")

@money.route('/AP')
def  ap():
    ap_query_text = text("Select *, (CAST(total AS float)/CAST(membercount AS float)) as Split FROM (Select id, CAST(irl_date as DATE) as irl_date, ig_date, description, pp, gp, sp, cp, ((pp*10) + gp + (sp/10) + (cp/100)) as total, payee, COUNT(AP_Member_Transactions.AP_id) as membercount, STRING_AGG(AP_Member_Transactions.Party_id, ',') as members FROM AP LEFT JOIN AP_Member_Transactions ON AP.id = AP_Member_Transactions.AP_id GROUP BY AP.id, AP.irl_date, AP.ig_date, AP.description, AP.pp, AP.gp, AP.sp, AP.cp, AP.payee) tbl;")
    ap_query = Lore_Session.execute(ap_query_text).all()
    names = []
    for aq in ap_query:
        split = aq[11].split(',')
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
    return render_template("ap.html",tran_names=names,ap_data=ap_query)

@money.route('/AR')
def  ar():
    ar_query_text = text("Select *, (CAST(total AS float)/CAST(membercount AS float)) as Split FROM (Select id, CAST(irl_date as DATE) as irl_date, ig_date, description, pp, gp, sp, cp, ((pp*10) + gp + (sp/10) + (cp/100)) as total, COUNT(AR_Member_Transactions.AR_id) as membercount, STRING_AGG(AR_Member_Transactions.Party_id, ',') as members FROM AR LEFT JOIN AR_Member_Transactions ON AR.id = AR_Member_Transactions.AR_id GROUP BY AR.id, AR.irl_date, ar.ig_date, ar.description, ar.pp, ar.gp, ar.sp, ar.cp) tbl")
    ar_query = Lore_Session.execute(ar_query_text).all()
    names = []
    for aq in ar_query:
        split = aq[10].split(',')
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

    return render_template("ar.html",tran_names=names,ar_data=ar_query)

@money.route('/Crew')
def  crew():
    return render_template("crew.html")

@money.route('/Magic_Items')
def  magic_items():
    return render_template("magic_items.html")

@money.route('/Party')
def  party():
    return render_template("party.html")

@money.route('/Ships')
def  ships():
    return render_template("ships.html")
