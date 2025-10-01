# Program to determine school level based on age
name = input("Enter your name: ")
age = int(input("Enter your age: "))

if 13 <= age <= 18:
    level = "Secondary"
elif 19 <= age <= 23:
    level = "Undergraduate"
elif age > 23:
    level = "Postgraduate"
else:
    level = "Not in the defined school levels"

print(f"Hello {name}, your school level is: {level}")
