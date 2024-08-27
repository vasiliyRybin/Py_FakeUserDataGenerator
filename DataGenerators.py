import random

def TaxesPayerNumberGenerator(Users, InvalidTaxPayerRatio, ValidTaxesPayerNumber_LowerValue, ValidTaxesPayerNumber_MaxValue):
    while True:
        TaxesPayerNumber = None
        if random.randrange(0, 100) > InvalidTaxPayerRatio:
            TaxesPayerNumber = random.randrange(ValidTaxesPayerNumber_LowerValue, ValidTaxesPayerNumber_MaxValue)
        else:
            #Here's would be generated invalid TaxPayerNumber
            TaxesPayerNumber = random.randrange(0, ValidTaxesPayerNumber_LowerValue - 1) 
        
        if not any(user.TaxesPayerNumber == TaxesPayerNumber for user in Users):
            return TaxesPayerNumber
    
def KurwaPassNumberGenerator(Users):    
    while True:
        Letters = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ"
        Letter = Letters[random.randrange(0, len(Letters) - 1)]
        PassNumber = "ZZ" + Letter + str(random.randrange(100000, 999999))   

        if not any(user.PassNumber == PassNumber for user in Users):
            return PassNumber