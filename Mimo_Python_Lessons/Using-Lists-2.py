growth_rate_1 = [0.5, 0.7, 0.8]
growth_rate_2 = [0.8, 0.6, 0.6]

print(growth_rate_1 + growth_rate_2)

student_1 = ["Anna", 16, "Kim", 16]
student_2 = ["Joe", 17, "Lee", 15]

print(student_1 + student_2)

members = ["Anna", "Joe", "Kim"]
scores = [57, 60, 32]

print(members + scores)

customers  = ["Jess", "Mike", "Lynn"]
order_number = [3, 1, 2]

orders = customers + order_number
print(orders)

day_1 = [3.5, 2, 4]
day_2 = [7, 1]
overview = day_1 + day_2
print(overview)

code = [3, 0, 2, 2, 0, 1, 0]
print(code.count(0))

flavors = ["vanilla", "chocolate", "strawberry", "vanilla", "vanilla"]
print(flavors.count("vanilla"))

schedule = ["ballet", "swimming", "running", "ballet"]
print("ballet" in schedule)

bought = ["L", "M", "S", "M", "M"]
print(bought.count("M"))
