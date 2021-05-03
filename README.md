This repo will help you set a script on your raspberry pi (or set it to run on your terminal in the background) to send an alert to your phone any time a crypto in your watch list moves.

The easiest way is to create a GMail account for use with this program, and have it send emails to your mobile phone. Each of the major phone companies have an extension where you can send an email to your phone number and it will come through as an SMS. For example, Sprint's is formatted like the following: 1234567890@messaging.sprintpcs.com.

If using GMail, you will have to enable insecure apps; there are several articles online detailling how best to do that.

Make sure you update the following variables:
* sender_address - your gmail address
* receiver_address - your mobile phone number with your carrier's email gateway appended
* account_password - your gmail address's password
* ids - string of the cryptos in your watchlist
* id_list - list of the cryptos in your watchlist
* pct_chng - you will be alerted when a crypto in your watchlist moves by +/- this percent. Default = 5%
* dlr_chng - alert you if a crypto (default is ETH) moves by +/- this amount in fiat. Default is 50 USD
* alert_on_changes - True if you want to get alerts based on pct_chng/dlr_chng; False if you only want alerts at certain times throughout the day
* alert_start_hour - hour when you want to receive a daily alert
* alert_start_minute - minute when you want to receive a daily alert

Note - alert_on_changes, alert_start_hour, and alert_start_minute are in preparation for a future iteration where you will be able to designate specific times to receive alerts


Future enhancements:
* All-time high alerts
* Alerts when a major support / resistance level is reached
* "Quiet time" where you can set a time range to not send alerts
