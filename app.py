try:
    from pypresence import Presence
except ModuleNotFoundError:
    input("You didn't install the 'pypresence' module! Please do 'pip install pypresence' in command prompt. Press ENTER to exit.")
    exit()
import json
import os
import sys
import time

#TESTRPC = Presence("892160344594710539", pipe=0)
#TESTRPC.connect()
#TESTRPC.update(start="1367765615", small_image="vsc", buttons=[{"label": "test", "url": "https://github.com/xtahaq"}])

with open("localprofiles.json", "r") as json_file:
    data = json.load(json_file)

def menu(): 
    clear()
    print("---------------------------------------------\n")
    print("--- Discord Rich Presence Manager by Taha ---\n")
    print("---------------------------------------------\n")
    print("Welcome, " + data["user"]["name"] + "!\n")

    menuInp = input("Please choose an action by typing the number:\n1 - Create Profile\n2 - Load Profile\n3 - Delete Profile\n4 - Rename Myself\n5 - Exit\n\n>> ")

    if menuInp == "1":
        cpMenu()
    elif menuInp == "2":
        lpMenu()
    elif menuInp == "3":
        dpMenu()
    elif menuInp == "4":
        createName()
    elif menuInp == "5":
        exit()
    else:
        menu()
    
def cpMenu():
    clear()
    print("CREATING A PROFILE\n")
    Profile_id = input("Please type the name (aka. id) of the profile (max 64 letters)\n>> ").strip()
    if len(Profile_id) > 64: Profile_id = Profile_id[:64]
    for profile in data["profiles"]:
        if profile["id"] == Profile_id:
            input("Profile ID already exists! Please name your profile to something else. Press ENTER to continue.")
            return cpMenu()
    buttons = []
    Profile_AppId = input("Please type the discord application id of your presence\n>> ")
    Profile_details = input("Please type the details (first line of presence) text\n>> ")
    Profile_state = input("Please type the state (second line of presence) text\n>> ")
    Profile_Limage = input("Please type the large image name\n>> ")
    Profile_Ltext = input("Please type the large image text (appears when you hover over the large image)\n>> ")
    Profile_Simage = input("Please type the small image name\n>> ")
    Profile_Stext = input("Please type the small image text (appears when you hover over the small image)\n>> ")
    Profile_timestamp = input("Allow timestamp? (Y/N)\n>> ")
    if Profile_timestamp != "Y":
        Profile_timestamp = False
    else:
        Profile_timestamp = True

    Profile_buttonL = input("Please type the text of first button (type nothing or 'none' to skip)\n>> ")
    if Profile_buttonL != "" or Profile_buttonL != "none":
        Profile_buttonU = input("Please type the redirect URL of first button\n>> ")
        buttons.append({"label": Profile_buttonL, "url": Profile_buttonU})
        Profile_buttonL = input("Please type the text of second button (type nothing or 'none' to skip)\n>> ")
        if Profile_buttonL != "" or Profile_buttonL != "none":
            Profile_buttonU = input("Please type the redirect URL of second button\n>> ")
            buttons.append({"label": Profile_buttonL, "url": Profile_buttonU})

    data["profiles"].append({
        "id": Profile_id,
        "app_id": Profile_AppId,
        "state": Profile_state,
        "details": Profile_details,
        "large_image": Profile_Limage,
        "large_text": Profile_Ltext,
        "small_image": Profile_Simage,
        "small_text": Profile_Stext,
        "timestamp": Profile_timestamp,
        "buttons": buttons
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
                StartPresence(profile["id"], profile["app_id"], profile["state"], profile["details"], profile["large_image"], profile["large_text"], profile["small_image"], profile["small_text"], profile["timestamp"], profile["buttons"])
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

def StartPresence(id, appid, state, details, li, lt, si, st, timestamp, bs):
    clear()
    try:
        RPC = Presence(appid, pipe=0)
        RPC.connect()
        ts = None
        if timestamp == True: ts = time.time()
        RPC.update(state=state, details=details, large_image=li, large_text=lt, small_image=si, small_text=st, start=ts, buttons=bs)
    except Exception as err:
        print("An error happened while setting up your presence. This might be because you setted it wrong (like invalid application id etc.)\n\nERROR INFO:")
        print(err)
        input("\nPress ENTER to go back to menu.")
        menu()
    else:
        input("Connected, press ENTER to stop the presence and go back to menu. - Current profile: " + id)
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
        print("Large Image Name: " + profile["large_image"])
        print("Large Image Text: " + profile["large_text"])
        print("Small Image Name: " + profile["small_image"])
        print("Small Image Text: " + profile["small_text"])
        print("Allow Timestamp: " + str(profile["timestamp"]))
        print("Button Objects: " + str(profile["buttons"]))

        print("\n")
    if indx == 0: print("You don't have any profiles yet!\n")

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