import os
import random
import sys
import names

def PathToCurrentFile():
    return os.path.abspath(__file__)

class User:
    def __init__(self, firstName, lastName):
        self.FirstName = firstName
        self.LastName = lastName
        self.Email = ""
        self.PhoneNumber = "+111111111"
    
AppName = sys.argv[0]
Arguments = sys.argv[1:]
Amount = None
DefaultAmount = 50

for item in Arguments:
    if item.startswith("amount:"):
        value = item.split(":")[1]
        if value.isdigit():
            Amount = int(value)
        else:
            print("Parameter 'amount:' having wrong value. Using default value (dolboyob ne znaet chto takoe chisla lol, idi nahuj teper')")
            Amount = DefaultAmount
            

if Amount == None:
    print("Parameter 'amount:' was not found. Using default value")
    Amount = DefaultAmount

Users = []

for _ in range(Amount):
    FirstName = names.get_first_name()
    LastName = names.get_last_name()
    _user = User(FirstName, LastName)
    
    Email = FirstName.lower() + "." + LastName.lower() + "@test.com"
    _user.Email = Email
    
    PhoneNumber = random.randrange(123456789, 999999999)
    _user.PhoneNumber = "+" + str(PhoneNumber)

    Users.append(_user)
    
'''
for _user in Users:
    Divisor = "\t\t"
    FirstLastNameLength = len(_user.FirstName + " " + _user.LastName)
    if FirstLastNameLength > 15:
        Divisor = "\t"
    else:
        Divisor = "\t\t"

    print(_user.FirstName + " " + _user.LastName + Divisor + _user.PhoneNumber + "  " + _user.Email)
'''

StartIndex = 0
ExecutionPath = PathToCurrentFile()
FileDirectory = ExecutionPath[StartIndex:ExecutionPath.rfind("\\") + 1]
PathTofile = FileDirectory + "TestData.csv"

File = open(PathTofile, "a+")
for _user in Users:
    File.write(_user.FirstName + ";" + _user.LastName + ";" + _user.PhoneNumber + ";" + _user.Email + ";" + "\n");

print("File with test data been written and located in " + PathTofile)
File.close()