def display(first_name):
    print(first_name)
display("Alex")

def display_full_name(first, last):
    print(first + "" + last)
display_full_name("Alex", "Morgan")

def show_winners(first, second, third):
    print("First place: " + first)
    print("Second place: " + second)
    print("Third place: " + third)
show_winners("Kim", "Lee", "Ava")

def show_winners(first, second):
    print("1st: " + first)
    print("2nd: " + second)

show_winners("Helen", "Joe")

def combine(first, second, third):
    return first + second + third
result = combine("big", "bad", "wolf")
print(result)

def create_email(name, year):
    return name + year + "@hutmail.com"

email = create_email("jo", "1998")
print(email)

def add_prefix(prefix, word):
    return prefix + word
new_word = add_prefix("re", "do")
print(new_word)

def show_queue(current, up_next):
    print("now playing: " + current)
    print("up next: " + up_next)
show_queue("Hey Joe", "Purple Haze")

def mix(first, second, third):
    print(first + second + third)
mix("Peter", "Piper", "Picked")
