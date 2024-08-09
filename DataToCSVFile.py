from datetime import datetime
import os
import random
import sys
import names
import csv

def PathToCurrentFile():
    return os.path.abspath(__file__)

class User:
    def __init__(self, firstName, lastName):
        self.FirstName = firstName
        self.LastName = lastName
        self.Email = ""
        self.PhoneNumber = "+111111111"
  

StartIndex = 0
ExecutionPath = PathToCurrentFile()
FileDirectory = ExecutionPath[StartIndex:ExecutionPath.rfind("\\") + 1]
PathTofile = FileDirectory + "TestData.csv"
PathToLog = FileDirectory + "Log.txt"

try:
    AppName = sys.argv[0]
    Arguments = sys.argv[1:]
    Amount = None
    DefaultAmount = 50
    
    #test = 0 / 0

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
        _user.PhoneNumber = "'+" + str(PhoneNumber)

        Users.append(_user)


    with open(PathTofile, mode="a+", encoding="utf-8", newline='') as CsvFile:
        FieldNames = ["First name", "Last name", "Phone number", "Email"]
        writer = csv.DictWriter(CsvFile, fieldnames=FieldNames, extrasaction="ignore", delimiter=";")
        writer.writeheader()
    
        for user in Users:
            writer.writerow(
                             {
                                 "First name": user.FirstName, 
                                 "Last name" : user.LastName,
                                 "Phone number" : user.PhoneNumber,
                                 "Email" : user.Email
                             }
                           )
    

    print("File with test data was successfully created and can be found in " + PathTofile)

except Exception as ex:
    with open(PathToLog, mode="a+", encoding="utf-8") as ErrorLog:
        ErrorLog.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\t" + str(ex))
        ErrorLog.write("\n")




    
'''

File = open(PathTofile, "a+")
for _user in Users:
    File.write(_user.FirstName + ";" + _user.LastName + ";'" + _user.PhoneNumber + ";" + _user.Email + ";" + "\n");

print("File with test data been written and located in " + PathTofile)
File.close()


for _user in Users:
    Divisor = "\t\t"
    FirstLastNameLength = len(_user.FirstName + " " + _user.LastName)
    if FirstLastNameLength > 15:
        Divisor = "\t"
    else:
        Divisor = "\t\t"

    print(_user.FirstName + " " + _user.LastName + Divisor + _user.PhoneNumber + "  " + _user.Email)
'''