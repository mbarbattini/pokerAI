class UserInput:
    
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def askUserCharInput(prompt, charOptions):
        while True:
            decision = input(prompt)
            if decision not in charOptions:
                print("Invalid input.")
                continue
            else:
                return decision


    @staticmethod
    def askUserFloatInput(prompt):
        while True:
            try:
                decision = float(input(prompt))
            except ValueError:
                print("Please enter a valid number.")
                continue
            else:
                return decision