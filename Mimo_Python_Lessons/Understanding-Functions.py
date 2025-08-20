def get_final_price(price, tax):
    return price + tax
price = get_final_price(30, 1.5)
print(price)

def create_email(name):
    return name + "@hotmail.com"
email = create_email("jo")
print(email)

def get_telephone(prefix, number):
    return prefix + number
def calculate_sum(num_1, num_2):
    return num_1 + num_2

def is_freezing(temperature):
    return temperature < 0
freezing = is_freezing(-3)
print(freezing)

def calculate_sum(num_1, num_2):
    return num_1 + num_2
def calculate_difference(num_1, num_2):
    return num_1 - num_2

def display_item_price(item, price):
    print(f"{item}: ${price}")
display_item_price("chocolate", 3)

def generate_username(name, b_day):
    return (f"{name}_{b_day}")
user = generate_username("ty", 17)
print(user)

def get_free_seats(booked, total):
    return total - booked
free = get_free_seats(13, 20)
print(free)

def get_successor(number):
    return number + 1
def get_predecessor(number):
    return number - 1

successor = get_successor(1)
print(successor)
predecessor = get_predecessor(1)
print(predecessor)
