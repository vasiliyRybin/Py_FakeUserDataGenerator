from datetime import datetime
import os
import random
import sys
import names
import csv

def TaxesPayerNumberGenerator(InvalidTaxPayerRatio):
    while True:
        TaxPayerNumber = 0
        if random.randrange(0, 100) > InvalidTaxPayerRatio:
            TaxPayerNumber = random.randrange(1111111111, 9999999999)
        else:
            TaxPayerNumber = random.randrange(0, 999999999)            
        
        if not any(user.TaxesPayerNumber == TaxPayerNumber for user in Users) :
            return TaxPayerNumber
    
def KurwaPassNumberGenerator():
    while True:
        Letters = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ"
        Letter = Letters[random.randrange(0, len(Letters) - 1)]
        PassNumber = "ZZ" + Letter + str(random.randrange(111111, 999999))   

        if not any(user.PassNumber == PassNumber for user in Users) :
            return PassNumber

def PathToCurrentFile():
    return os.path.abspath(__file__)

def GetCurrentDateTime_FormattedString():
    return str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))   

def CalculateExecutionTime(StartTime):
    EndTime = datetime.now()
    ExecutionTime = EndTime - StartTime
    ElapsedMilliseconds = int(ExecutionTime.microseconds / 1000) if (ExecutionTime.microseconds / 1000) > 99 else "0" + str(int(ExecutionTime.microseconds / 1000))
    ElapsedSeconds = str(ExecutionTime.seconds % 60) if ExecutionTime.seconds > 9 else "0" + str(ExecutionTime.seconds)
    ElapsedMinutes = int(ExecutionTime.seconds / 60) if (ExecutionTime.seconds / 60) > 9 else "0" + str(int(ExecutionTime.seconds / 60))
    ElapsedHours = int((ExecutionTime.seconds / 60) / 60) if int((ExecutionTime.seconds / 60) / 60) > 9 else "0" + str(int(((ExecutionTime.seconds / 60) / 60)))    
    return f"{ElapsedHours}:{ElapsedMinutes}:{ElapsedSeconds}.{ElapsedMilliseconds}"

class User:
    def __init__(self, firstName, lastName, taxesPayerNumber, passNumber):
        self.FirstName = firstName
        self.LastName = lastName
        self.Email = ""
        self.PhoneNumber = "+111111111"
        self.TaxesPayerNumber = taxesPayerNumber
        self.PassNumber = passNumber
  

StartIndex = 0
ExecutionPath = PathToCurrentFile()
FileDirectory = ExecutionPath[StartIndex:ExecutionPath.rfind("\\") + 1]
PathTofile = FileDirectory + "TestData.csv"
PathToLog = FileDirectory + "Log.txt"

try:
    AppName = sys.argv[0]
    Arguments = sys.argv[1:]
    InvalidTaxPayerRatio = None
    DefaultInvalidTaxPayerRatio = 10
    Amount = None
    DefaultAmount = 50
    StartTime = datetime.now()
    EndTime = datetime.now()
    print("Process started at " + GetCurrentDateTime_FormattedString())
    
    for item in Arguments:
        if item.startswith("amount:"):
            value = item.split(":")[1]
            if value.isdigit():
                Amount = int(value)
            else:
                print("Parameter 'amount:' having wrong value. Using default value... \n")
                Amount = DefaultAmount
        elif item.startswith("invalid_tax_id_ratio"):
            value = item.split(":")[1]
            if value.isdigit():
                InvalidTaxPayerRatio = int(value)
            else:
                print("Parameter 'invalid_tax_id_ratio:' having wrong value. Using default value... \n")
                InvalidTaxPayerRatio = DefaultInvalidTaxPayerRatio
            

    if Amount == None:
        print("Parameter 'amount:' was not found. Using default value of 50 \n")
        Amount = DefaultAmount
    elif InvalidTaxPayerRatio == None:
        print("Parameter 'invalid_tax_id_ratio:' was not found. Using default value of 10 \n")
        InvalidTaxPayerRatio = DefaultInvalidTaxPayerRatio
    
    if InvalidTaxPayerRatio > 100:
        InvalidTaxPayerRatio = 100
    elif InvalidTaxPayerRatio < 0:
        InvalidTaxPayerRatio = 1
            
    print("Amount of data to be generated: " + str(Amount) + "\n")

    Users = []

    for _ in range(Amount):
        FirstName = names.get_first_name()
        LastName = names.get_last_name()
        TaxesPayerNumber = TaxesPayerNumberGenerator(InvalidTaxPayerRatio)
        PassNumber = KurwaPassNumberGenerator()
        _user = User(FirstName, LastName, TaxesPayerNumber, PassNumber)
    
        Email = FirstName.lower() + "." + LastName.lower() + "@test.com"
        _user.Email = Email
    
        PhoneNumber = random.randrange(111111119, 999999999)
        _user.PhoneNumber = "'+" + str(PhoneNumber)

        Users.append(_user)


    with open(PathTofile, mode="a+", encoding="utf-8-sig", newline='') as CsvFile:
        FieldNames = ["First name", "Last name", "Phone number", "Email", "Tax payer number", "Pass number", "Comment"]
        writer = csv.DictWriter(CsvFile, fieldnames=FieldNames, extrasaction="ignore", delimiter=";")
        writer.writeheader()
    
        for user in Users:
            writer.writerow(
                             {
                                 "First name": user.FirstName, 
                                 "Last name" : user.LastName,
                                 "Phone number" : user.PhoneNumber,
                                 "Email" : user.Email,
                                 "Tax payer number" : user.TaxesPayerNumber,
                                 "Pass number" : user.PassNumber,
                                 "Comment" : "O kurwa! Popierdolony numer podatnika" if len(str(user.TaxesPayerNumber)) < 10 else "" 
                             }
                           )
    

    print("File with test data was successfully created and can be found in " + PathTofile + "\n")

except Exception as ex:
    print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\t" + str(ex))
    with open(PathToLog, mode="a+", encoding="utf-8") as ErrorLog:
        ErrorLog.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\t" + str(ex))
        ErrorLog.write("\n")
finally:
    TotalExecutionTime = CalculateExecutionTime(StartTime)
    
    print("Process finished at " + GetCurrentDateTime_FormattedString())
    print("Execution time: " + TotalExecutionTime + "\n")