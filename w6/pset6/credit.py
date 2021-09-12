# list_check = [{"AMEX": [34, 37]}, {"MASTERCARD", [51, 52, 53, 54, 55]}, {"Visa", [4]}]
from cs50 import get_int
import re 


def main():

    card = get_int("Numer: ")

    card_type = check_two_first(str(card))
    if (card_type == "INVALID"):
        print("INVALID")
        return

    sum = 0
    while card > 0:
        sum += card % 10
        card = int(card / 10)  # next number       
        n = card % 10 * 2
        card = int(card / 10)  # next number  

        # if 2 numbers => 12 => 1+2 
        if n > 9:
            sum += (n % 10) + int(n / 10)
        else:
            sum += n

    if (int(sum % 10) == 0):
        print(card_type)
    else:
        print("INVALID")


# American Express numbers start with 34 or 37 
# most MasterCard numbers start with 51, 52, 53, 54, 55
# and all Visa numbers start with 4
def check_two_first(number):
    """Check first two numbers """
    if number[0] == "4":
        return "VISA"   
    
    num = re.search(number[0:2], "^(51|52|53|54|55)")
    if num != None:
        return "MASTERCARD"    
    
    num = re.search(number[0:2], "^(34|37)")
    if num != None:
        return "AMEX"
    
    return "INVALID"


if __name__ == "__main__":
    main()