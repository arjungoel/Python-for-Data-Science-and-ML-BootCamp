# Create a function that grabs the email website domain from a string in the form user@domain.com and return domain.com


def getDomain(email):
    return email.split("@")[1]

print(getDomain("arjungoel1995@gmail.com"))
