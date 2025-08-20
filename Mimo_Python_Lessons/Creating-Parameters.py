def greet_ron():
    name = "Ron"
    print(f"Hello, {name}")
greet_ron()
def greet_leslie():
    name = "Leslie"
    print(f"Hello, {name}")
greet_leslie()    

def greet(name):
    print(f"Hello, {name}")
greet("April")
greet("Leslie")

def lamp_status():
    power = True
    print(f"Powered On: {power}")
lamp_status()

def user_status():
    status = "Active"
    username = "Bob"
    print(f"{username} is {status}")
user_status()

def user_status(status):
    print(f"Bob: {status}")
user_status("Active")

def display_half(number):
    half = number / 2
    print(half)
display_half(10)

def double_number(number):
    result = number * 2
    print(result)
double_number(5)
