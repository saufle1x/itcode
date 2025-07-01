import sms
import time  

number = '+79999999999'  
counter = 0
max_messages = 3  

while counter < max_messages:
    sms.send(number, 'ХПХХППХХП')
    counter += 1
    time.sleep(1)
