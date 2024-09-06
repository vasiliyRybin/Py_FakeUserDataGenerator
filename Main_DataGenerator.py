import os
import random
import sys
import names

from datetime import datetime
from UserClass import User
from Queries import GetDataForSpecifiedColsAndTable
from DataGenerators import TaxesPayerNumberGenerator, KurwaPassNumberGenerator
from DataProcessors import IsValueExistsInDB, WriteInfoToFile, WriteInfoToDB, WriteInfoToAllOutputSources, CheckUsersTableAvailability, GetAllDataFromSomeTable, MaintainUsersTable

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
    
    ElapsedSeconds = str(ExecutionTime.seconds % 60) if ExecutionTime.seconds % 60 >= 9 else str("0") + str(ExecutionTime.seconds % 60)
    ElapsedMinutes = str(int((ExecutionTime.seconds / 60) % 60)) if (ExecutionTime.seconds / 60) % 60 >= 9 else "0" + str(int((ExecutionTime.seconds / 60) % 60))
    ElapsedHours = str(int(ExecutionTime.seconds / 60 / 60)) if int(ExecutionTime.seconds / 60 / 60) >= 9 else "0" + str(int(ExecutionTime.seconds / 60 / 60))
    return f"{ElapsedHours}:{ElapsedMinutes}:{ElapsedSeconds}.{ElapsedMilliseconds}"


# Here we calculating the completion of task in percents
# It'll display each 5 percents completion of task 
# if you would like to change it, you need to change the 20 in (Amount // 20) part (Higher value - more often you see percentage. Max value - 100)
def CalculateTaskCompletion(Amount):
    DivisionRemainder = Amount // 20
    if DivisionRemainder > 0 and i % DivisionRemainder == 0:
        PercentComplete = (i) * 100 // Amount
        LogToConsole(f"{PercentComplete}% Completed")

# App main initialization
try:
    Letters = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ"
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
    InMemoryProcessing = None
    DbBulkInsert = None
    
    DefaultValue_DbBulkInsert = True
    DefaultValue_InMemoryProcessing = True
    DefaultValue_Amount = 5000
    DefaultValue_InvalidTaxPayerRatio = 10
    DefaultValue_OutputTo = 1
    
    LogToConsole("Process started" + "\n")
    
    #Arguments verification part
    for item in Arguments:
        
        if item.startswith("amount:"):
            value = item.split(":")[1]
            if value.isdigit():
                Amount = int(value)
            else:
                LogToConsole(f"Parameter 'amount:' having wrong value. Using default value of {DefaultValue_Amount} \n")
                Amount = DefaultValue_Amount
        
        #Parameter, responsible for amount of generated (in percents) invalid TaxID. When invalid tax ID was generated, we creating comment, telling that we having wrong TaxID
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
                
        # 0 - Checking for uniqueness of values (Email, TaxId and PassNumber) in DB. Good for small amounts of data (lower than 50000)
        # 1 - Checking for uniqueness of values (Email, TaxId and PassNumber) in RAM. Faster than DB checking, good for huge amounts of data (more than 50000)
        elif item.startswith("in_memory_processing"):
            value = item.split(":")[1]
            if value.strip().isdigit():
                InMemoryProcessing_Value = int(value)
                if InMemoryProcessing_Value == 0: InMemoryProcessing = False
                else: InMemoryProcessing = DefaultValue_InMemoryProcessing
            else:
                LogToConsole(f"Parameter 'in_memory_processing:' having wrong value. Using default value of {DefaultValue_InMemoryProcessing} \n")
                InMemoryProcessing = DefaultValue_InMemoryProcessing
                
        # 0 - Will insert each generated user right after the generation
        # 1 - First of all we'll collect the set of users and then will write them to the DB (on big amounts of data consuming a lot of RAM)
        elif item.startswith("data_bulk_insert"):
            value = item.split(":")[1]
            if value.strip().isdigit():
                DbBulkInsert_Value = int(value)
                if DbBulkInsert_Value == 0: DbBulkInsert = False
                else: DbBulkInsert = DefaultValue_DbBulkInsert
            else:
                LogToConsole(f"Parameter 'data_bulk_insert:' having wrong value. Using default value of {DefaultValue_DbBulkInsert} \n")
                DbBulkInsert = DefaultValue_DbBulkInsert
            

    if Amount == None or Amount <= 0:
        LogToConsole(f"Parameter 'amount:' was not found or having wrong value. Using default value of {DefaultValue_Amount} \n")
        Amount = DefaultValue_Amount
    
    if InvalidTaxPayerRatio == None or InvalidTaxPayerRatio > 100 or InvalidTaxPayerRatio < 0:
        LogToConsole(f"Parameter 'invalid_tax_id_ratio:' was not found or having wrong value. Using default value of {DefaultValue_InvalidTaxPayerRatio} \n")
        InvalidTaxPayerRatio = DefaultValue_InvalidTaxPayerRatio
    
    if OutputTo == None or OutputTo > 2 or OutputTo < 0:
        LogToConsole(f"Parameter 'output_to:' was not found or having wrong value. Using default value of {DefaultValue_OutputTo} \n")
        OutputTo = DefaultValue_OutputTo        
    
    if InMemoryProcessing == None:
        LogToConsole(f"Parameter 'in_memory_processing:' was not found or having wrong value. Using default value of {DefaultValue_InMemoryProcessing} \n")
        InMemoryProcessing = DefaultValue_InMemoryProcessing

    if DbBulkInsert == None:
        LogToConsole(f"Parameter 'data_bulk_insert:' was not found or having wrong value. Using default value of {DefaultValue_DbBulkInsert} \n")
        DbBulkInsert = DefaultValue_DbBulkInsert
    #End of arguments verification part
    
    
    IsUsersTableExists = CheckUsersTableAvailability(Paths["PathToDB"])  
    if not IsUsersTableExists and not InMemoryProcessing:     
        LogToConsole(f"Users table is unreachable. in_memory_processing set to default value {DefaultValue_InMemoryProcessing}")
        InMemoryProcessing = DefaultValue_InMemoryProcessing
        
    LogToConsole("Amount of data to be generated: " + str(Amount))
    LogToConsole(f"Current operating mode: {'In-Memory' if InMemoryProcessing is True else 'DB'}" + f". Bulk insertion of generated data: {'Activated' if DbBulkInsert is True else 'Deactivated'}" + "\n")

    Users = set()
    TaxesPayerNumbersSet = set()
    PassNumbersSet = set()
       
    Old_TaxesPayerNumbersSet = set()
    Old_PassNumbersSet = set()
    Old_EmailsSet = set()        
    
    if IsUsersTableExists and InMemoryProcessing is True:
            UsersData = GetAllDataFromSomeTable(Paths["PathToDB"], "TaxID, PassNumber, Email", "Users")
            [Old_TaxesPayerNumbersSet.add(record[0]) for record in UsersData]
            [Old_PassNumbersSet.add(record[1]) for record in UsersData]
            [Old_EmailsSet.add(record[2]) for record in UsersData]
            
    
    i = StartIndex       
    while i < Amount:
        IsTaxIdAlreadyExists = False        
        taxes_payer_number = TaxesPayerNumberGenerator(InvalidTaxPayerRatio, ValidTaxesPayerNumber_LowerValue, ValidTaxesPayerNumber_MaxValue)
        
        if InMemoryProcessing is False: IsTaxIdAlreadyExists = IsValueExistsInDB(Paths["PathToDB"], "Users", "TaxID", taxes_payer_number)
        elif InMemoryProcessing is True: IsTaxIdAlreadyExists = taxes_payer_number in Old_TaxesPayerNumbersSet

        if IsTaxIdAlreadyExists is False:
            TaxesPayerNumbersSet.add(taxes_payer_number)
            i = len(TaxesPayerNumbersSet)
    LogToConsole("Unique tax numbers were generated")
    
    i = StartIndex
    while i < Amount:    
        IsPassNumberAlreadyExists = False
        pass_number = KurwaPassNumberGenerator(Letters)

        if InMemoryProcessing is False: IsPassNumberAlreadyExists = IsValueExistsInDB(Paths["PathToDB"], "Users", "PassNumber", pass_number) 
        elif InMemoryProcessing is True: IsPassNumberAlreadyExists = pass_number in Old_PassNumbersSet
        
        if IsPassNumberAlreadyExists is False:
            PassNumbersSet.add(pass_number)
            i = len(PassNumbersSet)
    LogToConsole("Unique pass numbers were generated" + "\n")
     
    TaxesPayerNumbersList = list(TaxesPayerNumbersSet)
    PassNumbersList = list(PassNumbersSet)

    # deleting the initial sets to free the memory
    del Old_PassNumbersSet
    del Old_TaxesPayerNumbersSet
    del TaxesPayerNumbersSet
    del PassNumbersSet
     
    i = StartIndex
    while i < Amount:   
        FirstName = names.get_first_name()
        LastName = names.get_last_name()
        TaxesPayerNumber = TaxesPayerNumbersList[i]
        PassNumber = PassNumbersList[i]
        _user = User(FirstName, LastName, TaxesPayerNumber, PassNumber)
    
        Email = FirstName.lower() + "." + LastName.lower() + "@test.com"          
        IsEmailExists = False
        
        while True:             
            if InMemoryProcessing is True: IsEmailExists = Email in Old_EmailsSet
            else: IsEmailExists = IsValueExistsInDB(Paths["PathToDB"], "Users", "Email", Email) or (Email in Old_EmailsSet)
            
            if IsEmailExists is False:
                _user.Email = Email
                if DbBulkInsert is True or InMemoryProcessing is True: 
                    Old_EmailsSet.add(Email)
                break
            
            else:
                Postfix = ''.join(random.sample(Letters, 5)).lower()
                Email = FirstName.lower() + "." + LastName.lower() + "_" + Postfix.lower() + "@test.com"
                
        PhoneNumber = random.randrange(111111111, 999999999)
        _user.PhoneNumber = "'+" + str(PhoneNumber)
        _user.Comment = "O kurwa! Popierdolony numer podatnika" if TaxesPayerNumber < ValidTaxesPayerNumber_LowerValue else "" 

        Users.add(_user)
        
        if not DbBulkInsert:
           if OutputTo == 0: WriteInfoToFile(Users, Paths["PathToCSV"])
           elif OutputTo == 1: WriteInfoToDB(Users, Paths["PathToDB"])
           elif OutputTo == 2: WriteInfoToAllOutputSources(Users, Paths)
           
           Users.clear()
           i += 1
        else:
            i = len(Users)
        CalculateTaskCompletion(Amount)

    if DbBulkInsert:     
        if OutputTo == 0:
            WriteInfoToFile(Users, Paths["PathToCSV"])
            LogToConsole("File with test data was successfully created and can be found in " + Paths["PathToCSV"] + "\n")
        elif OutputTo == 1:
            WriteInfoToDB(Users, Paths["PathToDB"])
            LogToConsole("File with test data was successfully created/updated and can be found in " + Paths["PathToDB"] + "\n")
        elif OutputTo == 2:
            WriteInfoToAllOutputSources(Users, Paths)
            LogToConsole("Files with test data was successfully created/updated and can be found in " + FileDirectory + "\n")
        

except Exception as ex:
    LogToConsole(str(ex))
    with open(Paths["PathToLog"], mode="a+", encoding="utf-8") as ErrorLog:
        ErrorLog.write(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\t" + str(ex))
        ErrorLog.write("\n")
finally:
    TotalExecutionTime = CalculateExecutionTime(StartTime)
    
    if IsUsersTableExists:
        MaintainUsersTable(Paths["PathToDB"], "IX_Email", "Users", "Email")
        MaintainUsersTable(Paths["PathToDB"], "IX_TaxID", "Users", "TaxID")
        MaintainUsersTable(Paths["PathToDB"], "IX_PassNumber", "Users", "PassNumber")

    LogToConsole("Process finished")
    LogToConsole("Execution time: " + TotalExecutionTime + "\n")