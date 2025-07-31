class QuizGame:
    def __init__(self):
        self.questions = [
            "What is the capital of Nigeria?",
            "Who is the president of Nigeria?", 
            "What is the role of EFCC in Nigeria?"
        ]
        self.answers = [
            "Abuja",
            "Ahmed Bola Tinubu", 
            "Investigating Financial Crimes"
        ]
        self.score = 0
    
    def ask_question(self, question):
        answer = input(question + " ")
        correct_answer = self.answers[self.questions.index(question)]
        if answer.strip().lower() == correct_answer.strip().lower():
            print("Correct!")
            self.score += 1
        else:
            print(f"Incorrect - the correct answer is {correct_answer}")
    
    def play(self):
        for question in self.questions:
            self.ask_question(question)
        print(f"Game Over! Your final score is {self.score} out of {len(self.questions)}")
    
    def display_rules(self):
        print("Welcome to the Quiz Game!")
        print("You will be asked a series of questions.")
        print("For each question, type your answer and press Enter.")
        print("Let's start!\n")
    
    def run(self):
        self.display_rules()
        self.play()

if __name__ == "__main__":
    game = QuizGame()
    game.run()
