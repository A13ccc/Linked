# Password validity checker
# Alec Rudisill
# 1st Period

# Importing modules needed
import time as t

# Defining global variables
pass_works = [False, False, False, False, False]

# Function to check validity of the user entered password.
def check_pass(password):
    # Defining local variables
    special_char = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', ']', '{', '}', '|', ':', ';', '<', '>', ',', '.', '/', '?', '~', '`']
    
    # Conditional statement that checks the password against multiple criterias.
    if len(password) < 12:
        length = True
        return False, length, False, False, False
    if not any(char.isdigit() for char in password):
        digit = True
        return False, False, digit, False, False
    if not any(char.isupper() for char in password):
        upper = True
        return False, False, False, upper, False
    if not any(char in special_char for char in password):
        special = True
        return False, False, False, False, special
    return True, False, False, False, False

# Main program loop
while pass_works[0] == False:
    password = list(input("Enter your password: "))

    # Call to the check_pass() function.
    pass_works = check_pass(password)

    # Conditional statement that checks what was wrong with the password and informs the user of what needs change.
    if pass_works[0] == False:
        print(f"Your password, {''.join(password)}, is weak.\n")

        if pass_works[1] == True:
            print("Your password is too short, it needs to be at least 12 characters long. Try again.")
        if pass_works[2] == True:
            print("Your password does not contain a digit. Try again.")
        if pass_works[3] == True:
            print("Your password does not contain an uppercase letter. Try again.")
        if pass_works[4] == True:
            print("Your password does not contain a special character. Try again.")

        # Pausing, allowing the user to read and then clearing the screen so the user can fix their mistake.
        t.sleep(3)

        print("\n" * 100)


# If all conditions are met the password is strong and the user is informed of their success then the program ends.
print(f"Your password, {''.join(password)}, is strong.")