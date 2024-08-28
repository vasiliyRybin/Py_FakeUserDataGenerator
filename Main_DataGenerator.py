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

def LogToConsole(Message):
    print(GetCurrentDateTime_FormattedString() + "     " + Message)

def CalculateExecutionTime(StartTime):
    #"2024-08-28 15:43:00"
    #StartTime = datetime(year= 2024, month= 8, day= 28, hour= 15, minute= 43, second=0)
    EndTime = datetime.now()
    ExecutionTime = EndTime - StartTime
    ElapsedMilliseconds = "000"
    
    if (ExecutionTime.microseconds % 1000) > 99:
        ElapsedMilliseconds = int(ExecutionTime.microseconds % 1000)
    elif (ExecutionTime.microseconds % 1000) > 9:
        ElapsedMilliseconds = "0" + str(int(ExecutionTime.microseconds % 1000))
    else:
        ElapsedMilliseconds = "00" + str(int(ExecutionTime.microseconds % 1000))
    
    ElapsedSeconds = str(ExecutionTime.seconds % 60) if ExecutionTime.seconds % 60 > 9 else str("0") + str(ExecutionTime.seconds % 60)
    ElapsedMinutes = int((ExecutionTime.seconds / 60) % 60) if (ExecutionTime.seconds / 60) % 60 > 9 else "0" + str(int((ExecutionTime.seconds / 60) % 60))
    ElapsedHours = int(ExecutionTime.seconds / 60 / 60) if int(ExecutionTime.seconds / 60 / 60) > 9 else "0" + str(int(ExecutionTime.seconds / 60 / 60))
    return f"{ElapsedHours}:{ElapsedMinutes}:{ElapsedSeconds}.{ElapsedMilliseconds}"


#App main initialization
try:
    StartTime = datetime.now()
    EndTime = datetime.now()
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
    DefaultValue_Amount = 5000
    DefaultValue_InvalidTaxPayerRatio = 10
    DefaultValue_OutputTo = 1
    
    LogToConsole("Process started")
    
    #Arguments verification part
    for item in Arguments:
        
        if item.startswith("amount:"):
            value = item.split(":")[1]
            if value.isdigit():
                Amount = int(value)
            else:
                LogToConsole(f"Parameter 'amount:' having wrong value. Using default value of {DefaultValue_Amount} \n")
                Amount = DefaultValue_Amount
        
        elif item.startswith("invalid_tax_id_ratio"):
            value = item.split(":")[1]
            if value.isdigit():
                InvalidTaxPayerRatio = int(value)
            else:
                LogToConsole(f"Parameter 'invalid_tax_id_ratio:' having wrong value. Using default value of {DefaultValue_InvalidTaxPayerRatio} \n")
                InvalidTaxPayerRatio = DefaultValue_InvalidTaxPayerRatio
        
        # 0 - write to CSV file
        # 1 - Write to DB
        # 2 - Both options (To CSV and DB)        
        elif item.startswith("output_to"):
            value = item.split(":")[1]
            if value.isdigit():
                OutputTo = int(value)
            else:
                LogToConsole(f"Parameter 'invalid_tax_id_ratio:' having wrong value. Using default value of {DefaultValue_OutputTo} \n")
                OutputTo = DefaultValue_OutputTo
            

    if Amount == None or Amount <= 0:
        LogToConsole(f"Parameter 'amount:' was not found or having wrong value. Using default value of {DefaultValue_Amount} \n")
        Amount = DefaultValue_Amount
    
    if InvalidTaxPayerRatio == None or InvalidTaxPayerRatio > 100 or InvalidTaxPayerRatio < 0:
        LogToConsole(f"Parameter 'invalid_tax_id_ratio:' was not found or having wrong value. Using default value of {DefaultValue_InvalidTaxPayerRatio} \n")
        InvalidTaxPayerRatio = DefaultValue_InvalidTaxPayerRatio
    
    if OutputTo == None or OutputTo > 2 or OutputTo < 0:
        LogToConsole(f"Parameter 'output_to:' was not found or having wrong value. Using default value of {DefaultValue_OutputTo} \n")
        OutputTo = DefaultValue_OutputTo
    #End of arguments verification part
        
    LogToConsole("Amount of data to be generated: " + str(Amount) + "\n")

    Users = set()
    TaxesPayerNumbersSet = set()
    PassNumbersSet = set()

    while len(TaxesPayerNumbersSet) < Amount:
        taxes_payer_number = TaxesPayerNumberGenerator(InvalidTaxPayerRatio, ValidTaxesPayerNumber_LowerValue, ValidTaxesPayerNumber_MaxValue)
        TaxesPayerNumbersSet.add(taxes_payer_number)

    LogToConsole("Unique tax numbers were generated")
    while len(PassNumbersSet) < Amount:        
        pass_number = KurwaPassNumberGenerator()
        PassNumbersSet.add(pass_number)
    
    LogToConsole("Unique pass numbers were generated")
     
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
            LogToConsole(f"{PercentComplete}% Completed")


    if OutputTo == 0:
        WriteInfoToFile(Users, Paths["PathToCSV"])
        LogToConsole("File with test data was successfully created and can be found in " + Paths["PathToCSV"] + "\n")
    elif OutputTo == 1:
        WriteInfoToDB(Users, Paths["PathToDB"])
        LogToConsole("File with test data was successfully created and can be found in " + Paths["PathToDB"] + "\n")
    elif OutputTo == 2:
        WriteInfoToAllOutputSources(Users, Paths)
        LogToConsole("Files with test data was successfully created and can be found in " + FileDirectory + "\n")
        

except Exception as ex:
    LogToConsole(str(ex))
    with open(Paths["PathToLog"], mode="a+", encoding="utf-8") as ErrorLog:
        ErrorLog.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\t" + str(ex))
        ErrorLog.write("\n")
finally:
    TotalExecutionTime = CalculateExecutionTime(StartTime)
    
    LogToConsole("Process finished")
    LogToConsole("Execution time: " + TotalExecutionTime + "\n")