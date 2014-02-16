import sys, subprocess
from time import *
from common import *
from pprint import *

def error(error=''):
	print 'Error:',error
	sys.exit(1)

def parse_csv(what):
    if what.count(',') == 0:
        return list([what])
    return val.split(',')

a = sys.argv
var = {'-s' : 'btc'}

d = {}
for i in range(a.__len__()):
    try: 
        if a[i].startswith('-'):
            try:
                d.update({a[i]:a[i+1]})
            except:
                d.update({a[i]:''})
    except: None

for item in d.iteritems():
    key = item.__getitem__(0)
    val = item.__getitem__(1)
    var[key] = parse_csv(val)

# sec = var.get('-s')

pprint(var)
# sys.exit(0)
from pycoinex import *

def show_profit():
    orig_amt = None
    for i in c.bals.__iter__():
        if i['currency_name'].upper()=='BTC': 
            orig_amt = i['amount']/1e8
            break
    time.sleep(1.5)
    print '\nAvailable Balances:\n'
    new_bals = c.available()
    print_json(new_bals)
    new_amt = new_bals['BTC']
    print '\nEarnings This Session: %.8f BTC\n' % (new_amt-orig_amt)

def sell(pri, sec, amount=0.0):
    mkt_name = '_'.join([pri,sec])
    print '\nMarket Name:', mkt_name

    # Get current account balance
    cur_name = pri.upper()
    bals = c.bals
    bal = None
    for b in bals:
        if b['currency_name'] == cur_name:
            bal = b['amount']/1e8
            break
    if bal == 0: error('Not enough funds in balance!')
    elif bal is None: error('Currency Not Found!')
    print 'Balance is: %.8f %s' % (bal, cur_name)

    # Find the market id number
    id = c.findid(mkt_name)
    if id == -1: error('Market Not Found!')
    print 'Market ID:', id

    # Get the highest buying price
    rate = c.highestBidOrder(id)
    print 'Highest Buy Price: %.8f %s' % (rate,sec.upper())

    # Display the potential sale
    amount = float(amount)
    if amount > 0: amt = amount
    else: amt = bal
    sale = amt*rate
    print 'Selling %.8f %s' % (amt,pri.upper())
    print 'Sale Amount: %.8f %s\n' % (sale,sec.upper())

    # Make the sale
    if var.has_key('-i'): cfrm='Y'
    else: cfrm = raw_input('Continue? ')
    if cfrm.upper() == 'Y':
        order = c.order(id, amt, rate=rate)
        order_data = order.json()['order']
        order_data['amount'] = order_data['amount']/1e8
        order_data['rate'] = order_data['rate']/1e8
        
        print '\nOrder Details:\n'
        print_json(order_data)
        print
        
    else: print '\nOrder cancelled.'

mkts = var.get('-p')
amts = var.get('-a')
smkt = var.get('-s')

if amts is None:
    amts = []
    for j in range(mkts.__len__()): amts.extend('0')
elif amts.__len__() > 1:
    if mkts.__len__() is not amts.__len__(): error('Argument lengths do not match.')

for i in range(mkts.__len__()):
    try:
        time.sleep(4)
        if type(smkt) is list:
            sell(mkts[i], smkt[i], amts[i])
        else: sell(mkts[i], smkt, amts[i])
    except Exception as e:
        print 'Error encountered:',e

show_profit()
