import smtplib, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pycoingecko import CoinGeckoAPI
from datetime import datetime
import collections
cg = CoinGeckoAPI()

# email information
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
    print('email sent')
    
# using coin_gecko, get the price of your watch list
def get_coins():
    coins = cg.get_price(ids=ids, vs_currencies='usd')
    return(coins)

# parse the coins to compose your alert
def parse_coins(coins):
    coins = collections.OrderedDict(sorted(coins.items()))

    msg = ""
    for k, v in coins.items():
        msg = msg + symbol_dict[k] + ": " + str(v['usd']) + "\n" 

    return(msg)

# runs at a designated time each morning
def good_morning():
    coins = get_coins()
    
    msg = parse_coins(coins)
    sub = 'Good morning'
    send_alert(msg, sub)

    return(coins)

# this first list is a list of coins on your watch list
ids = 'ethereum,cardano,vechain,harmony,uniswap,solana,neo,algorand'
# because of the coin_gecko API, we also need to do a little work to get the symbol
id_list = ['ethereum', 'cardano', 'vechain', 'harmony', 'uniswap', 'solana', 'neo', 'algorand']
# pct_chng set variable to check percent change
pct_chng = 5.0
# dlr_chng set variable to check a dollar change
dlr_chng = 50.0

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

# run the alert program... always.
run = True

# instantiate and send 1 alert when the script first starts
coins = good_morning()
print('coins instantiated')

# set the time each day you want at least 1 alert to trigger
time1 = datetime.now().time()
# default is 08:30-08:32 according to your raspi
time1 = time1.replace(hour=8, minute=30, second=0, microsecond=0)
time2 = datetime.now().time()
time2 = time2.replace(hour=8, minute=31, second=59, microsecond=0)

while run:
    # checks the daily trigger / good_morning time
    now = datetime.now()
    if now.time() > time1 and now.time() < time2:
        coins = good_morning()
        print('good_morning sent at ' + str(now))
    
    # gets the price for your watch list for comparison
    n_coins = get_coins()
    
    # I'm interested in ETH, so I set a separate trigger (+/-$50) for ETH
    eth_chng = n_coins['ethereum']['usd'] - coins['ethereum']['usd']
    if abs(eth_chng) >= dlr_chng:
        msg = parse_coins(n_coins)
        if eth_chng > 0:
            sub = 'ETH Up'
        else:
            sub = 'ETH Down'
        send_alert(msg, sub)
        coins = get_coins()
        print('Compare price updated ' + str(now))
    else:
        # all other alerts based on a percent change
        for k, v in n_coins.items():
            p1 = coins[k]['usd']
            p2 = v['usd']
            pct = ((p2-p1)/p1)*100
            # change pct_change to what you want to track
            if abs(pct) >= pct_chng:
                t = str(k)
                msg = parse_coins(n_coins)
                if pct > 0:
                    sub = symbol_dict[k] + ' Up'
                else:
                    sub = symbol_dict[k] + ' Down'
                send_alert(msg, sub)
                coins = get_coins()
                print(t + ' percent change ' + str(now))
    # time to pause/sleep before running again
    time.sleep(100)
    
        
        