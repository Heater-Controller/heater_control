import time 
from machine import Timer 
from control import *
from time import sleep 


tdss1 = int(input("Enter the desired temperature of special spot 1: "))
tdss2 = int(input("Enter the desired temperature of special spot 2: "))

triangle1 = [1,2,4]
triangle2 = [3,4,2]
current_status = [0,0,0,0,0]

# Initial calculations to get time values 
temp_value = recieve_temp_data()

#Check that all sensors are working 
while sensor_value_check(temp_value) == "False":    
    temp_value = recieve_temp_data()

#Get the calculated superposed time   
#tT1 = calcuate_tT(t1, t2, t3)
#tT2 = calcuate_tT(t4, t5, t6)

#Get the time average time around the special spot 
tss1 = calculate_tss(temp_value[0], temp_value[1], temp_value[2])  
tss2 = calculate_tss(temp_value[3], temp_value[4], temp_value[5])  

#Get the tind time
#tind1 = calculate_tind(tdss1, tss1)
#tind2 = calculate_tind(tdss2, tss2)

"""""
#Get the total time to reach special spot temp
tTotal1 = calculate_tTotal(tind1, tT1)
tTotal2 = calculate_tTotal(tind2, tT2)

#Get the lowest tTotal value 
t_wait = min(tTotal1, tTotal2)

#Initialize tTotal timer interupt to achieve desired temperature 
tTotal_timer = Timer(4)
tT1_timer = Timer(3)
tT2_timer = Timer(2)
tTotal_timer.init(mode = Timer.ONE_SHOT, period = t_wait * 60000, callback = tTotal_timer_callback)
"""

#Begin the control 
relay_status = "on"
temp_control_check1 = "Desired temperature not reached"
temp_control_check2 = "Desired temperature not reached"

while tdss1 != tss1 and tdss2 != tss2:
    
    current_status = send_relay_signal(relay_status, current_status, triangle1)    
    temp_value = recieve_temp_data()
    tss1 = calculate_tss(temp_value[0], temp_value[1], temp_value[2])  
    tss2 = calculate_tss(temp_value[3], temp_value[4], temp_value[5])  
    print("Temp in desired spot 1 = " + str(tdss1) + " - Tss1 value: " + str(tss1) +  " => " + temp_control_check1)
    print("Temp in desired spot 2 = " + str(tdss2) + " - Tss2 value: " + str(tss2) +  " => " + temp_control_check2)


"""""
def tT1_timer_callback(t):
    
    relay_status = "soft_turn_off"
    send_relay_signal(relay_status, relays, triangle1)


def tT2_timer_callback(t):
    
    relay_status = "soft_turn_off"
    send_relay_signal(relay_status, relays, triangle2)
"""

while True:
    
    #Measure thhe temperature and recalculate tss
    temp_value = recieve_temp_data()
    tss1 = calculate_tss(temp_value[0], temp_value[1], temp_value[2])  
    tss2 = calculate_tss(temp_value[3], temp_value[4], temp_value[5])  

    # perform a temperature check to determinne which range we are in. 
    # Above, bellow or withim the desired temperature range 
    temp_control_check1 = check_temp(tdss1, tss1)
    temp_control_check2 = check_temp(tdss2, tss2)

    if temp_control_check1 == "above":
         
        relay_status = "hard_turn_off"
        current_status = send_relay_signal(relay_status, current_status, triangle1)    
        
    elif temp_control_check1 == "below":
        
        relay_status = "soft_turn_on"
        current_status = send_relay_signal(relay_status, current_status, triangle1)    

        # wait for the temperature to increase by 1 with tT 
        #tT1_timer.init(mode = Timer.ONE_SHOT, period = tT1 * 60000, callback = tT1_timer_callback)

    elif temp_control_check1 == "within":

        relay_status = "no_signal"
        current_status = send_relay_signal(relay_status, current_status, triangle1)    

    if temp_control_check2 == "above":
         
        relay_status = "hard_turn_off"
        current_status = send_relay_signal(relay_status, current_status, triangle2)    
        
    elif temp_control_check2 == "below":
        
        relay_status = "soft_turn_on"
        current_status = send_relay_signal(relay_status, current_status, triangle2)    

        # wait for the temperature to increase by 1 with tT 
        #tT2_timer.init(mode = Timer.ONE_SHOT, period = tT2 * 60000, callback = tT2_timer_callback)
    
    elif temp_control_check2 == "Within":
        
        relay_status = "no_signal"
        current_status = send_relay_signal(relay_status, current_status, triangle2)    

    print("Temperature value: " + str(temp_value))
    print("Temp in desired spot 1 = " + str(tdss1) + " - Tss1 value: " + str(tss1) +  " => " + 
        temp_control_check1 + ", Signal = " + relay_status + ", Hard turn off = " + str(current_status[4]))
    print("Temp in desired spot 2 = " + str(tdss2) + " - Tss2 value: " + str(tss2) +  " => " + 
        temp_control_check2 + ", Signal = " + relay_status + ", Hard turn off = " + str(current_status[4]))

        
        

