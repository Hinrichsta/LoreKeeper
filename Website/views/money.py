from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy import text
import json
from Database.Database import Lore_Session
from Database.Parse import *
from Database.Input import *

money = Blueprint('money', __name__)

@money.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        #trans = [request.form.get('cdesc'),request.form.get('pp') or 0,request.form.get('gp') or 0,request.form.get('sp') or 0,request.form.get('cp') or 0,request.form.get('cpayee'),request.form.get('cmembers')]

        #i = 0
        #while i < len(trans):
        #    print(trans[i])
        #    print(type(trans[i]))
        #    if trans[i] != ' ':
        #        pass
        #    else:
        #        trans[i] == 0
        #    i += 1

        if "coin_deposit" in request.form:
            set_ar_transaction(request.form.get('cdesc'),request.form.get('pp') or 0,request.form.get('gp') or 0,request.form.get('sp') or 0,request.form.get('cp') or 0,request.form.get('cmembers'))
        elif "coin_withdraw" in request.form:
            set_ap_transaction(request.form.get('cdesc'),request.form.get('pp') or 0,request.form.get('gp') or 0,request.form.get('sp') or 0,request.form.get('cp') or 0,request.form.get('cmembers'),request.form.get('cpayee'))
        elif "store_item" in request.form:
            pass

    party_funds = get_party_funds()
    indiv_funds = get_all_individual_funds()
    return render_template("home.html", party_funds=party_funds, indiv_funds=indiv_funds)

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
    return render_template("magic_items.html")

@money.route('/Party')
def  party():
    return render_template("party.html")

@money.route('/Ships')
def  ships():
    return render_template("ships.html")
