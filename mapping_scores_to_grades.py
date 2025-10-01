#Python dictionary to map numerical scores to their corresponding letter grades (A-E).
def get_letter_grade(score):
    if score >= 75:
        return 'A'
    elif score >= 60:
        return 'B'
    elif score >= 50:
        return 'C'
    elif score >= 40:
        return 'D'
    else:
        return 'E'
score = 69.9
print(f"Score: {score}, Grade: {get_letter_grade(score)}")