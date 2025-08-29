def add_shipping(cart):
    if cart < 100:
        print(f"Total: {cart + 10}")
    else:
        print(f"Total: {cart}")
add_shipping(45)
add_shipping(200)

def add_shipping(cart):
    if cart < 100:
        print(f"Total: {cart + 10}")
add_shipping(80)

def can_drive(age):
    if age >= 18:
        print ("Yes they can!")
can_drive(19)

def has_low_battery(level):
    if level <= 20:
        print("Low Battery!")
has_low_battery(15)

def get_waiting_list(signups):
    if signups > 200:
        print(f"Waiting list: {signups - 200}")
get_waiting_list(250)
