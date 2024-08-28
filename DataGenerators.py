import random

def TaxesPayerNumberGenerator(InvalidTaxPayerRatio, ValidTaxesPayerNumber_LowerValue, ValidTaxesPayerNumber_MaxValue):
    if random.randrange(0, 100) > InvalidTaxPayerRatio:
        return random.randrange(ValidTaxesPayerNumber_LowerValue, ValidTaxesPayerNumber_MaxValue)
    else:
        #Here's would be generated invalid TaxPayerNumber
        return random.randrange(0, ValidTaxesPayerNumber_LowerValue - 1) 
    
def KurwaPassNumberGenerator():
    Letters = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ"
    Letter = Letters[random.randrange(0, len(Letters) - 1)]
    return "ZZ" + Letter + str(random.randrange(100000, 999999))   