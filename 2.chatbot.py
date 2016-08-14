import aiml
import os
from sqlwala import *
#the aiml package only works with Python 2. Py3kAiml on GitHub is a Python 3 alternative.
kernel = aiml.Kernel()   #create the aiml object

#When you start to have a lot of AIML files, it can take a long time to learn. This is where brain files come in. After the bot learns all the AIML files it can save its brain directly to a file which will drastically speed up load times on subsequent runs.

# Press CTRL-C to break this loop
if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
    kernel.saveBrain("bot_brain.brn")

def chatBotResponse(message):
    #message = raw_input("Enter your message to the bot: ")
    if message == "quit":
        exit()
    elif message == "save":
        kernel.saveBrain("bot_brain.brn")
        return "Duly noted and saved !! "
    else:
        bot_response = kernel.respond(message)//aiml 
        if bot_response == "NOT FOUND" or message[:6] == "search":
            #print("Deep learning...please wait....")
            if message[:6] == "search":
                retVal = sqlChat(message[7:])
                return retVal[0]
            else:
                retVal = sqlChat(message)
                return retVal[0]

        else:
            return bot_response

if __name__ == '__main__':
    while True:
        ans = chatBotResponse(raw_input(">>> "))
        print("Roid >>> " + str(ans))