import os
import random
import sys
import names

from datetime import datetime
from UserClass import User
from DataGenerators import TaxesPayerNumberGenerator, KurwaPassNumberGenerator
from DataWriters import WriteInfoToFile, WriteInfoToDB, WriteInfoToAllOutputSources

def PathToCurrentFile():
    return os.path.abspath(__file__)

def GetCurrentDateTime_FormattedString():
    return str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))   

def CalculateExecutionTime(StartTime):
    EndTime = datetime.now()
    ExecutionTime = EndTime - StartTime
    ElapsedMilliseconds = int(ExecutionTime.microseconds / 1000) if (ExecutionTime.microseconds / 1000) > 99 else "0" + str(int(ExecutionTime.microseconds / 1000))
    ElapsedSeconds = str(ExecutionTime.seconds % 60) if ExecutionTime.seconds > 9 else str("0") + str(ExecutionTime.seconds)
    ElapsedMinutes = int(ExecutionTime.seconds / 60) if (ExecutionTime.seconds / 60) > 9 else "0" + str(int(ExecutionTime.seconds / 60))
    ElapsedHours = int((ExecutionTime.seconds / 60) / 60) if int((ExecutionTime.seconds / 60) / 60) > 9 else "0" + str(int(((ExecutionTime.seconds / 60) / 60)))    
    return f"{ElapsedHours}:{ElapsedMinutes}:{ElapsedSeconds}.{ElapsedMilliseconds}"


#App main initialization
try:
    StartIndex = 0
    ExecutionPath = PathToCurrentFile()
    FileDirectory = ExecutionPath[StartIndex:ExecutionPath.rfind("\\") + 1]

    Paths = {
                "PathToDB" : FileDirectory + "TestUserData.db",
                "PathToCSV" : FileDirectory + "TestUserData.csv",
                "PathToLog" : FileDirectory + "Log.txt"
            }

    
    ValidTaxesPayerNumber_LowerValue = 1000000000
    ValidTaxesPayerNumber_MaxValue = 9999999999
    AppName = sys.argv[0]
    Arguments = sys.argv[1:]
    InvalidTaxPayerRatio = None
    Amount = None
    OutputTo = None
    DefaultAmount = 50
    DefaultInvalidTaxPayerRatio = 10
    DefaultOutputTo = 0
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
        
        # 0 - write to CSV file
        # 1 - Write to DB
        # 2 - Both options (To CSV and DB)        
        elif item.startswith("output_to"):
            value = item.split(":")[1]
            if value.isdigit():
                OutputTo = int(value)
            else:
                print("Parameter 'invalid_tax_id_ratio:' having wrong value. Using default value... \n")
                OutputTo = DefaultInvalidTaxPayerRatio
            

    if Amount == None:
        print("Parameter 'amount:' was not found. Using default value of 50 \n")
        Amount = DefaultAmount
    elif InvalidTaxPayerRatio == None:
        print("Parameter 'invalid_tax_id_ratio:' was not found. Using default value of 10 \n")
        InvalidTaxPayerRatio = DefaultInvalidTaxPayerRatio
    elif OutputTo == None:
        print("Parameter 'output_to:' was not found. Using default value of 0 \n")
        InvalidTaxPayerRatio = DefaultInvalidTaxPayerRatio
    
    if InvalidTaxPayerRatio > 100:
        InvalidTaxPayerRatio = 100
    elif InvalidTaxPayerRatio < 0:
        InvalidTaxPayerRatio = 1
            
    print("Amount of data to be generated: " + str(Amount) + "\n")

    Users = set()
    TaxesPayerNumbersSet = set()
    PassNumbersSet = set()

    while len(TaxesPayerNumbersSet) < Amount:
        taxes_payer_number = TaxesPayerNumberGenerator(InvalidTaxPayerRatio, ValidTaxesPayerNumber_LowerValue, ValidTaxesPayerNumber_MaxValue)
        TaxesPayerNumbersSet.add(taxes_payer_number)

    print(GetCurrentDateTime_FormattedString() + "     " + "Unique tax numbers were generated")
    while len(PassNumbersSet) < Amount:        
        pass_number = KurwaPassNumberGenerator()
        PassNumbersSet.add(pass_number)
    
    print(GetCurrentDateTime_FormattedString() + "     " + "Unique pass numbers were generated")
     
    TaxesPayerNumbersList = list(TaxesPayerNumbersSet)
    PassNumbersList = list(PassNumbersSet)

    # deleting the initial sets to free the memory
    del TaxesPayerNumbersSet
    del PassNumbersSet
    
    i = 0   
    while i < Amount:
        FirstName = names.get_first_name()
        LastName = names.get_last_name()
        TaxesPayerNumber = TaxesPayerNumbersList[i]
        PassNumber = PassNumbersList[i]
        _user = User(FirstName, LastName, TaxesPayerNumber, PassNumber)
    
        Email = FirstName.lower() + "." + LastName.lower() + "@test.com"
        _user.Email = Email
    
        PhoneNumber = random.randrange(111111111, 999999999)
        _user.PhoneNumber = "'+" + str(PhoneNumber)

        _user.Comment = "O kurwa! Popierdolony numer podatnika" if TaxesPayerNumber < ValidTaxesPayerNumber_LowerValue else "" 

        Users.add(_user)
        i = len(Users)

        # Here we calculating the completion of task in percents
        # It'll display each 5 percents completion of task 
        # if you would like to change it, you need to change the 20 in (Amount // 20) part (Higher value - more often you see percentage. Max value - 100)
        if (i) % (Amount // 20) == 0:
            PercentComplete = (i) * 100 // Amount
            print( GetCurrentDateTime_FormattedString() + "     " + f"{PercentComplete}% Completed")


    if OutputTo == 0:
        WriteInfoToFile(Users, Paths["PathToCSV"])
        print("File with test data was successfully created and can be found in " + Paths["PathToCSV"] + "\n")
    elif OutputTo == 1:
        WriteInfoToDB(Users, Paths["PathToDB"])
        print("File with test data was successfully created and can be found in " + Paths["PathToDB"] + "\n")
    elif OutputTo == 2:
        WriteInfoToAllOutputSources(Users, Paths)
        print("Files with test data was successfully created and can be found in " + FileDirectory + "\n")
        

except Exception as ex:
    print(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\t" + str(ex))
    with open(Paths["PathToLog"], mode="a+", encoding="utf-8") as ErrorLog:
        ErrorLog.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\t" + str(ex))
        ErrorLog.write("\n")
finally:
    TotalExecutionTime = CalculateExecutionTime(StartTime)
    
    print("Process finished at " + GetCurrentDateTime_FormattedString())
    print("Execution time: " + TotalExecutionTime + "\n")