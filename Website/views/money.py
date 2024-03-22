from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy import text
import json
from Database.Database import Lore_Session
from Database.Parse import *
from Database.Input import *

money = Blueprint('money', __name__)

@money.route('/', methods=['GET', 'POST'])
def home():
    party_funds = get_party_funds()
    indiv_funds = get_all_individual_funds()
    eth_date = get_etharus_date()
    if request.method == 'POST':
        seasons = ['Spring', 'Summer', 'Fall', 'Autumn']
        if "coin_deposit" in request.form:
            if request.form.get('cdesc') == None:
                pass
            else:
                set_ar_transaction(request.form.get('cdesc'),request.form.get('pp') or 0,request.form.get('gp') or 0,request.form.get('sp') or 0,request.form.get('cp') or 0,request.form.get('cmembers'))
        elif "coin_withdraw" in request.form:
            if request.form.get('cdesc') == None:
                pass
            else:
                set_ap_transaction(request.form.get('cdesc'),request.form.get('pp') or 0,request.form.get('gp') or 0,request.form.get('sp') or 0,request.form.get('cp') or 0,request.form.get('cmembers'),request.form.get('cpayee'))
        elif "store_item" in request.form:
            if request.form.get('iname') == None:
                pass
            else:
                deposit_magic_item(request.form.get('iname'),request.form.get('inotes'),'Active', request.form.get('irarity') or None,request.form.get('imaker') or None,request.form.get('ilink') or None,request.form.get('imembers') or None, None,None)
        elif "date-update" in request.form:
            set_etharus_date(request.form.get('mseason') or eth_date[0],request.form.get('mday') or eth_date[1],request.form.get('myear') or eth_date[2])
            return redirect(url_for('money.home'))
        #elif "decrement-date" in request.form:
        #    eth_season = eth_date[0]
        #    eth_day = eth_date[1] - 1
        #    eth_year = eth_date[2]
        #    if eth_day == 0:
        #        eth_day = 91
        #        i = 0
        #        for s in seasons:
        #            if eth_date[0] != s:
        #                i += 1
        #                break
        #        eth_season = seasons[i]
        #        if eth_date[0] == 'Spring':
        #            eth_year = int(eth_date[2]) - 1
        #    set_etharus_date(eth_season,eth_day,eth_year)
        #
        #elif "increment-date" in request.form:
        #    eth_season = eth_date[0]
        #    eth_day = eth_date[1] + 1
        #    eth_year = eth_date[2]
        #    if eth_day == 91:
        #        eth_day = 0
        #        i = 0
        #        for s in seasons:
        #            if eth_date[0] != s:
        #                i += 1
        #                break
        #        eth_season = seasons[i+1]
        #        if eth_date[0] == 'Winter':
        #            eth_year = int(eth_date[2]) + 1
        #    set_etharus_date(eth_season,eth_day,eth_year)
    magic_items,magic_owner = get_magic_items()
    active_party = get_active_party()
    party_items = []
    stored_items = []
    sorted_items = []
    
    i = 0
    for mi in magic_items:
        if mi[8] == 'Active' and magic_owner[i][0] == 'Party Stash':
            party_items.append(('Party',mi[3],mi[4],mi[5],mi[7]))
        elif mi[8] == 'Storage':
            stored_items.append(('Stored',mi[3],mi[4],mi[5],mi[7]))
        i += 1

    for act in active_party:
        temp_items = []
        i = 0
        print(act[1])
        for mi in magic_items:
            print(f"{mi[3]}:{magic_owner[i][1]}")
            if act[1] == magic_owner[i][1]:
                sorted_items.append((act[1],mi[3],mi[4],mi[5],mi[7]))
            i += 1
    for si in sorted_items:
        print(si)

            
    return render_template("home.html", party_funds=party_funds, indiv_funds=indiv_funds, eth_date=eth_date, magic_items=sorted_items,active_party=active_party,party_items=party_items,stored_items=stored_items)

@money.route('/AP')
def  ap():
    ap_data, names = get_ap_trans()

    return render_template("ap.html",tran_names=names,ap_data=ap_data)

@money.route('/AR')
def  ar():
    ar_data, names = get_ar_trans()

    return render_template("ar.html",tran_names=names,ar_data=ar_data)

@money.route('/Crew')
def  crew():
    return render_template("crew.html")

@money.route('/Magic_Items')
def  magic_items():
    mi_data, owner = get_magic_items()
    return render_template("magic_items.html",mi_data=mi_data,owner=owner)

@money.route('/Party')
def  party():
    return render_template("party.html")

@money.route('/Ships')
def  ships():
    return render_template("ships.html")
