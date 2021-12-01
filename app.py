try:
    from pypresence import Presence
except ModuleNotFoundError:
    input("You didn't install the 'pypresence' module! Please do 'pip install pypresence' in command prompt. Press ENTER to exit.")
    exit()
import json
import os
import sys
import time

TESTRPC = Presence("892160344594710539", pipe=0)
TESTRPC.connect()
TESTRPC.update(start="1367765615", small_image="vsc")

with open("localprofiles.json", "r") as json_file:
    data = json.load(json_file)

def menu(): 
    clear()
    print("--------------------------------------------\n")
    print("---------- Rich Presence Manager -----------\n")
    print("--------------------------------------------\n")
    print("Welcome, " + data["user"]["name"] + "!\n")

    menuInp = input("Please choose an action by typing the number:\n1 - Create Profile\n2 - Load Profile\n3 - Delete Profile\n4 - Rename Myself\n\n>> ")

    if menuInp == "1":
        cpMenu()
    elif menuInp == "2":
        lpMenu()
    elif menuInp == "3":
        dpMenu()
    elif menuInp == "4":
        createName()
    else:
        menu()
    
def cpMenu():
    clear()
    print("CREATING A PROFILE\n")
    Profile_id = input("Please type the name (aka. id) of the profile (max 64 letters)\n>> ").strip()
    if len(Profile_id) > 64: Profile_id = Profile_id[:64]
    Profile_AppId = input("Please type the discord application id of your presence\n>> ")
    Profile_state = input("Please type the state (first line of presence) text\n>> ")
    Profile_details = input("Please type the details (second line of presence) text\n>> ")
    Profile_timestamp = input("Allow timestamp? (Y/N)\n>> ")
    if Profile_timestamp != "Y":
        Profile_timestamp = False
    else:
        Profile_timestamp = True

    for profile in data["profiles"]:
        if profile["id"] == Profile_id:
            input("Profile ID already exists! Please name your profile to something else. Press ENTER to continue.")
            cpMenu()
    data["profiles"].append({
        "id": Profile_id,
        "app_id": Profile_AppId,
        "state": Profile_state,
        "details": Profile_details,
        "timestamp": Profile_timestamp
    })
    updateFile()
    input("Created! Press ENTER to go back to menu.")
    menu()

def lpMenu():
    clear()
    listProfiles()
    opt = input("Please enter the PROFILE ID to load that profile, or type ENTER without typing anything to go back to menu.\n>> ")
    if opt == "":
        menu()
    else:
        for profile in data["profiles"]:
            if profile["id"] == opt:
                StartPresence(profile["id"], profile["app_id"], profile["state"], profile["details"], profile["timestamp"])
        else:
            dpMenu()

def dpMenu():
    clear()
    listProfiles()
    opt = input("Please enter the PROFILE ID to delete that profile, or type ENTER without typing anything to go back to menu.\n>> ")
    if opt == "":
        menu()
    else:
        for profile in data["profiles"]:
            if profile["id"] == opt:
                data["profiles"].remove(profile)
                updateFile()
        else:
            dpMenu()

def createName():
    name = input("Please type your name (max 64 letters)\n>> ")
    name = name.strip()
    if len(name) > 64:
        input("Your name cannot be longer than 64 letters, press ENTER to retry.")
        createName()
    else:
        data["user"]["name"] = name
        updateFile()
        menu()

def StartPresence(id, appid, state, details, timestamp):
    clear()
    try:
        RPC = Presence(appid, pipe=0)
        RPC.connect()
        ts = None
        if timestamp == True: ts = time.time()
        RPC.update(state=state, details=details, start=ts)
    except Exception as err:
        print("An error happened while setting up your presence. This might be because you setted it wrong (like invalid application id etc.)\n\nERROR INFO:")
        print(err)
        input("\nPress ENTER to go back to menu.")
        menu()
    else:
        input("Connected, press ENTER to stop the presence and go back to menu.")
        RPC.close()
        menu()



def clear():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # if machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def updateFile():
    with open("localprofiles.json", "w") as json_file:
        json.dump(data, json_file, indent=4, sort_keys=False)

def listProfiles():
    indx = 0
    print("PROFILES:\n")
    for profile in data["profiles"]:
        indx += 1
        print(">> PROFILE NUMBER " + str(indx) + " <<\n")
        print("Profile ID: " + profile["id"])
        print("Application ID: " + profile["app_id"])
        print("State Text: " + profile["state"])
        print("Details Text: " + profile["details"])
        print("Allow Timestamp: " + str(profile["timestamp"]))

        print("\n")
    if indx == 0: print("You don't have any profiles yet!")

def show_exception_and_exit(exc_type, exc_value, tb):
    clear()
    print("--  ERROR  --")
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press ENTER to exit.")
    exit()

sys.excepthook = show_exception_and_exit

if (data["user"]["name"] == None):
    createName()
else:
    menu()