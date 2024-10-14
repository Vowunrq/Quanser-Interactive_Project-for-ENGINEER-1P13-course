ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P3B' # Enter the project identifier i.e. P2A or P2B

# SERVO TABLE CONFIGURATION
short_tower_angle = 315 # enter the value in degrees for the identification tower 
tall_tower_angle = 90 # enter the value in degrees for the classification tower
drop_tube_angle = 180 # enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# BIN CONFIGURATION
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 

bin1_offset = 0.13 # offset in meters
bin1_color = [1,0,0] # e.g. [1,0,0] for red
bin1_metallic = False

bin2_offset = 0.13
bin2_color = [0,1,0]
bin2_metallic = False

bin3_offset = 0.13
bin3_color = [0,0,1]
bin3_metallic = False

bin4_offset = 0.13
bin4_color = [1,1,1]
bin4_metallic = False
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
if project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
else:
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color],[bin1_metallic,bin2_metallic, bin3_metallic,bin4_metallic]]
    configuration_information = [table_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bot = qbot(0.1,ip_address,QLabs,project_identifier,hardware)
##---------------------------------------------------------------------------------------
## STUDENT CODE BEGINS
##---------------------------------------------------------------------------------------

#Note: The functions from OZ() to third() are not part of the mandatory functions of the project. However, for code and visual simplicity, I have made certain lines of code into their own functions.
#OZ() is inputed 2 times within the transfer() function and 1 time within the return_home() function.
#botCloser() and botTakeOff shortens the distance between the bot and arm. To make the program visually appealing, I have made these two functions separately.
#armTrans(counter) allows the arm to move in specific locations.
#first(), second(), and third() are the positions of each containers that are to be placed upon the hopper. These are created to be edited easily if there are logical errors. 

#follow the yellow brick road
def OZ():
    speed = 0.1                                                 #place holder for bot's speed
    
    [a,b] = bot.line_following_sensors()                        #declare each one light sensor as 'a' and the other as 'b'
        
    if a == 1 and b == 1:                                       #if a and b are both 1, bot will go forward with the same speed
        bot.set_wheel_speed([speed, speed])
    elif a == 1:                                                #if a is 1, bot will turn as only the wheel on the b side will roll while the one on side a does not.
        bot.set_wheel_speed([0.0, speed])
    elif b == 1:                                                #same thing as above, but for b
        bot.set_wheel_speed([speed, 0.0])
    else:                                                       #if bot cannot sense yellow line, it is lost (this should not be passed unless the program is ruined)
        bot.stop()

#bot prepares to get closer to the arm
def botCloser():
    bot.rotate(100)
    time.sleep(1)
    bot.forward_distance(0.15)
    time.sleep(1)
    bot.rotate(-200)
    time.sleep(1)

#bot prepares to leave with containers
def botTakeOff():
    bot.forward_distance(0.05)
    time.sleep(1)
    bot.rotate(100)
    time.sleep(1)

#careful positioning of arm for loading each container
def armTrans(counter):
    arm.move_arm(0.65, 0, 0.26)                                 #position arm to grab container
    time.sleep(2)                                               #This resets the arm and prevents errors (sometimes the arm grippers will just phase through the containers if it moves too fast)
    arm.control_gripper(38)                                     #grab container
    time.sleep(2)
    arm.move_arm(0.5, 0, 0.3)                                   #making sure the container doesn't hit anything
    time.sleep(2)
    arm.move_arm(0.2, 0.0, 0.55)                                #reposition arm with container
    time.sleep(2)
    arm.rotate_base(-88)                                        #rotates arm to look at bot
    time.sleep(2)

    if counter == 1:                                            #calls first, second, or third functions depending on the counter value
        first()
    elif counter == 2:
        second()
    else:
        third()
    
    time.sleep(1)
    arm.home()                                                  #reposition arm
    time.sleep(1)

#first position of arm
def first():
    arm.move_arm(0.06, -0.545, 0.5)                             #about to drop container onto bot [position 1]
    time.sleep(1)
    arm.control_gripper(-25)                                    #drops container onto bot
    time.sleep(1)
    arm.move_arm(0.06, -0.4, 0.5)                               #carefully back up

#second position of arm
def second():
    arm.move_arm(-0.035, -0.543, 0.5)                           #about to drop container onto bot [position 2]
    time.sleep(1)
    arm.control_gripper(-25)                                    #drops container onto bot
    time.sleep(1)
    arm.move_arm(-0.035, -0.2, 0.5)                             #carefully back up

#third position of arm
def third():
    arm.move_arm(-0.12, -0.55, 0.5)                             #about to drop container onto bot [position 3]
    time.sleep(1)
    arm.control_gripper(-25)                                    #drops container onto bot
    time.sleep(1)
    arm.move_arm(-0.12, -0.5, 0.6)                              #carefully back up
    time.sleep(1)
    arm.move_arm(-0.12, -0.4, 0.6)                              #extra careful


#Project functions------------------------------------------------------------------------------------------------------------------------------------

#dispense function to summon a random container
def dispense():
    container = random.randint(1,6)                                         #creating random container
    material, mass, Bin = table.dispense_container(container, True)         #declaring material, mass, and Bin accordingly to the values given by the dispense_container function that already exists in the system
    print(material, " ", mass, " ", Bin)                                    #print the values for debug and checking
    return material, mass, Bin                                              #return the values

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#load function to transfer specific containers onto the hopper
def load(empty, MASS):

    counter = 0                                             #counter, tempBin, and tempMass are declared as default
    tempBin = ""
    tempMass = 0
    
    Bin = empty                                             #Bin shall be empty (literally or just the value held within the variable)
    mass = MASS                                             #mass will equal MASS brought from main function like above
    
    while True:
        counter += 1                                        #counter will go up from 1 to 3 (if it goes above, the program is ruined)

        if empty == " ":                                    #if empty is literally empty...
            material, mass, Bin = dispense()                #dispense function is called and material, mass, and Bin are declared
            empty = "full"                                  #declare empty as full because a container exists.

        tempMass += mass                                    #tempMass is the sum of the each mass of containers that are dispensed

        if counter == 1:                                                            #if loading container the first time, the bot will...
            botCloser()                                                             #get closer
            tempBin = Bin                                                           #and tempBin will be set as Bin to compare it with the next bin
            armTrans(counter)                                                       #calls armTrans after setting the parameter with the counter value to allow the arm to move in specific positions
            empty = " "                                                             #declare empty as empty because the container is removed
            
        elif (counter == 2 or counter == 3) and tempBin == Bin and tempMass < 90:   #if 2nd or 3rd container load, see if the bins are the same and the total mass doesn't exceed 90g
            armTrans(counter)                                                       
            empty = " "                                                             
            
        else:                                                                       #if bot's ready...
            botTakeOff()                                                            #bot takes off
            return tempBin, Bin, mass                                               #break out of infinite loop

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#transfer function to move the bot adjacent to a specified bin
def transfer(tempBin):
    
    if tempBin == 'Bin01':                                  #if tempBin is Bin01, the color of bin is red
        R = 1
        G = 0
        B = 0
    elif tempBin == 'Bin02':                                #if tempBin is Bin02, the color of bin is green
        R = 0
        G = 1
        B = 0
    elif tempBin == 'Bin03':                                #if tempBin is Bin03, the color of bin is blue
        R = 0
        G = 0
        B = 1
    else:                                                   #if tempBin is Bin04, the color of bin is white
        R = 1
        G = 1
        B = 1

    bot.activate_color_sensor()                                     #activate color sensor
    bot.activate_line_following_sensor()                            #activate line following sensor

    #loop to follow the yellow brick road while sensing for the bin it requires
    while True:
        [red, green, blue], [x, y, z] = bot.read_color_sensor()     #declare the color sensor into the designated variables. Declare the x,y,z coordinates of the bin.

        OZ()                                                        #follow, follow, follow, follow, follow the yellow brick road
        
        if red == R and green == G and blue == B:                   #bot will stop if it detects the correct colour
            bot.stop()                                              
            print("color")                                          #debug or to check if this has been passed
            break                                                   #break out of loop

    #loop to get adjacent to the bin
    while True:
        OZ()                                                        

        bot.activate_ultrasonic_sensor()                            #activate ultrasonic sensor
        
        close = bot.read_ultrasonic_sensor()                        #reading the ultrasonic sensor and declaring close as the value
        print(close)
        
        bot.deactivate_ultrasonic_sensor()                          #deactivate ultrasonic sensor (the bot seems to move a bit more in a straight line if the ultrasonic sensor activates and deactivates constantly rather than to let it activate forever, so this was/is necessary)             

        if close <= 0.06:                                           #if the bot's distance between itself and the bin is less than or equal to 0.06m, it will stop and make further adjustments. 
            bot.stop()
            time.sleep(1)
            bot.forward_distance(0.08)
            bot.rotate(-15)
            return

#-----------------------------------------------------------------------------------------------------------------------------------------------------

#deposit function for the bot to release all containers into bin
def deposit():
    bot.activate_linear_actuator()                          #activate linear actuator
    time.sleep(1)
    bot.dump()                                              #dump containers
    time.sleep(1)
    bot.deactivate_linear_actuator()                        #deactivate linear actuator
    time.sleep(1)

#-----------------------------------------------------------------------------------------------------------------------------------------------------

#return home function for the bot to return to its original position
def return_home(x, y, z):

    xR = x + 0.1                                            #the bot cannot stop precisely at the original position, so it will stop within these set of x and y coordinate range 
    xL = x - 0.1
    yU = y + 0.1
    yD = y - 0.1

    bot.activate_line_following_sensor()                    #activate line following sensor 

    while True:
        OZ()                                                #follow, follow, follow, follow, follow the yellow brick road
    
        X, Y, Z = bot.position()                            
        if xL < X < xR and yD < Y < yU:                     #if bot is near the original position, stop
            bot.stop()
            break
    
    time.sleep(1)
    
    bot.forward_distance(0.11)                              #further adjustments to arrive at home (almost): translation and rotation
    time.sleep(1)
    bot.rotate(-10)                                         
    time.sleep(1)

    bot.deactivate_line_following_sensor()                  #deactivate line following sensor

#-----------------------------------------------------------------------------------------------------------------------------------------------------

#main function aka the work function
def main():
    x, y, z = bot.position()                                #the values will be brought from the main function and be recorded within x, y, and z
    
    Bin = " "                                               #initially declare Bin for the load function
    mass = 0                                                #Same as above but for mass
    
    #Ask user if they want to see the project
    while True:
        user = input("Type \"yes\" to watch the recycling robot do its job. Otherwise, type \"no\": ")
        
        if user == "yes":
            tempBin, Bin, mass = load(Bin, mass)            #load function: If this is not the first cycle, the container has already been displaced previously, so the parameters hold the bin type and mass value. It returns the tempBin (for the bot to move near and deposit), Bin and mass (to return new values for the Bin and mass variables)
            transfer(tempBin)                               #transfer function: with tempBin, the bot will figure out which bin to go to.
            deposit()                                       #deposit function
            return_home(x, y, z)                            #return function: the starting position has been recorded and will allow the bot to return to it.
            print("Finished!\n")
        elif user == "no":
            return                                          #end
        else:
            print("<ERROR: Cannot recognize input>")        #Error message for the while loop to repeat

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------




