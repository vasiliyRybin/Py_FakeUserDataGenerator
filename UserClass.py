class User:
    def __init__(self, firstName, lastName, taxesPayerNumber, passNumber):
        self.FirstName = firstName
        self.LastName = lastName
        self.Email = ""
        self.PhoneNumber = "+111111111"
        self.TaxesPayerNumber = taxesPayerNumber
        self.PassNumber = passNumber
        self.Comment = ""

    def __eq__(self, other):
        if isinstance(other, User):
            return (self.TaxesPayerNumber == other.TaxesPayerNumber and
                    self.PassNumber == other.PassNumber)
        return False

    def __hash__(self):
        return hash((self.TaxesPayerNumber, self.PassNumber))