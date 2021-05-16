#!/usr/bin/python3

import smtplib, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pycoingecko import CoinGeckoAPI
from datetime import datetime, date, timedelta
import collections
cg = CoinGeckoAPI()

#####################################
#### Configure your  alerts here ####
#####################################

# this first list is a list of coins on your watch list
ids = 'ethereum,cardano,vechain,harmony,uniswap,solana,neo,algorand'
# because of the coin_gecko API, we also need to do a little work to get the symbol
id_list = ['ethereum', 'cardano', 'vechain', 'harmony', 'uniswap', 'solana', 'neo', 'algorand']
# if you want to track 1 crypto more closely than the others update this var
main_id = 'ethereum'

#####################################
#### Configure alert frequency   ####
#####################################
# alert frequency is based on what you
# set your crontab to run

#####################################
#### Email/SMS alert information ####
#####################################
sender_address = "enter_your_gmail_here" 
receiver_address = "enter_your_phone_number_here@messaging.sprintpcs.com" 
account_password = "enter_your_gmail_pswd_here"

# compose and send the email-sms alert
# if you're using gmail, you may have to allow insecure apps
def send_alert(body, sub):
    msg = MIMEMultipart()
    msg['From'] = sender_address
    msg['To'] = receiver_address
    msg['Subject'] = sub

    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(sender_address,account_password)
    text = msg.as_string()

    server.sendmail(sender_address, receiver_address, text)
    server.quit()
    
# parse the coins to compose your alert
def parse_coins(coins):
    coins = collections.OrderedDict(sorted(coins.items()))

    msg = ""
    for k, v in coins.items():
        msg = msg + symbol_dict[k] + ": " + str(v['usd']) + "\n" 
    return(msg)

# Called when script starts and at a designated time(s)
def crypto_alert():
    coins = cg.get_price(ids=ids, vs_currencies='usd')
    
    msg = parse_coins(coins)
    sub = 'Crypto Alert'
    send_alert(msg, sub)

# calculate the pp, resistance, and support
def calc_technicals(coin_id):
    coin_tech = cg.get_coin_by_id(id=coin_id, vs_currencies='usd')
    current = coin_tech['market_data']['current_price']['usd']
    high = coin_tech['market_data']['high_24h']['usd']
    low = coin_tech['market_data']['low_24h']['usd']
   
    y = date.today() - timedelta(days=1)
    y = y.strftime('%d-%m-%Y')
    y = str(y)
    close = cg.get_coin_history_by_id(coin_id, y)
    close = close['market_data']['current_price']['usd']
    
    pivot_point = (close + high + low)/3
    r1 = str(round(((2 * pivot_point) - low), 2))
    s1 = str(round(((2 * pivot_point) - high), 2))
    s2 = str(round((pivot_point - (high - low)), 2))
    s3 = str(round((low - 2 * (high - pivot_point)), 2))
    ath = str(coin_tech['market_data']['ath']['usd'])
    ath_ch_pct = str(round(coin_tech['market_data']['ath_change_percentage']['usd'], 2))
    
    msg = 'Now: ' + str(current) + '\nHigh: ' + str(high) + '\nLow: ' + str(low) +'\nATH: ' + ath + '\nR1: ' + r1 + '\nS1: ' + s1 + '\nS2: ' + s2 + '\nS3: ' + s3
    sub = symbol_dict[coin_id] + ' Stats'
    send_alert(msg, sub)
    return(current)

sym = []
# get coins from coin_gecko
coins_list = cg.get_coins_list()

#get the symbols for your watch list
for id in id_list:
    symbol = list(filter(lambda c: c['id'] == id, coins_list))
    sym.append(symbol)

symbol_dict = {}
i = 0
for id in id_list:
    symbol_dict[id] = sym[i][0]['symbol'].upper()
    i = i + 1

# send alert
crypto_alert()
# send technicals for main_id
calc_technicals(main_id)
    