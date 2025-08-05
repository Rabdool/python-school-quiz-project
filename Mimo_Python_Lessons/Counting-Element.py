answers = ["yes", "no", "sometimes", "yes", "no"]
print(answers.count("yes"))

free_seats = [False, False, True, True, False]
print(free_seats.count(True))

free_seats = [False, False, True, True, False]
seats_count = free_seats.count(True)

print(seats_count)

ingredients = ["flour", "butter", "sugar", "eggs"]

print("sugar" in ingredients)
print("chocolate" in ingredients)

has_suger = "sugar" in ingredients
print(has_suger)

missions = ["Moon", "Mars", "ISS", "Mars"]
print(missions.count("Mars"))

flavors = ["vanilla", "chocolate", "strawberry", "vanilla", "vanilla"]
print(flavors.count("vanilla"))

temperatures = [40, 32, 32, 38]
print(temperatures.count(32))

cleaning_duty = ["Luke", "Sue", "Joe", "Joe"]
luke = cleaning_duty.count("Luke")
print(luke)

winnig_numbers = [2, 36, 40, 13]
print(13 in winnig_numbers)
print(0 in winnig_numbers)

has_13 = 13 in winnig_numbers
print(has_13)
