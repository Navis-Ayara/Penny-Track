import os
from time import sleep

import rich.panel
import rich.console
import inquirer

class PennyTracker:
    console = rich.console.Console()
    panel = rich.panel.Panel.fit(
        "[bold yellow]Penny Track [/ bold yellow]\nA personal finance CLI\n\nCommands: add | view | report | analytics | exit",
        border_style="white"
    )

    categories = [
        "housing",
        "utilities",
        "transportation",
        "groceries",
    ]
    categories.append("New category")

    @staticmethod
    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @classmethod
    def show_panel(cls):
        cls.console.print(cls.panel)

    @classmethod
    def select_category(cls):
        question = [
            inquirer.List(
                "option",
                message="Choose a category",
                choices=[category.capitalize() for category in cls.categories]
            )
        ]

        answer = inquirer.prompt(question)
        if answer:
            if answer['option'] == "New category":
                category_name = input("Enter a new category name: ")
                return category_name
            else:
                return answer["option"]
            
    @classmethod
    def get_amount(cls):
        question = [
            inquirer.Text(
                "amount",
                message="Enter the amount",
                validate=lambda _, x: x.isdigit() or x == "",
                default="1"
            )
        ]

        answer = inquirer.prompt(question)
        if answer and answer["amount"] != "0":
            try:
                amount = float(answer["amount"])
                return amount
            except ValueError:
                print("Invalid amount. Please enter a number.")
                cls.get_amount()
        else:
            print("Amount cannot be zero.")
            cls.get_amount()
        
    @classmethod
    def start(cls):
        while True:
            cls.show_panel()
            choice = input("> ")

            match choice:
                case "add":
                    cls.clear_terminal()
                    category = cls.select_category()
                    amount = cls.get_amount()
                    cls.clear_terminal()
                    print("Records have been updated successfully!")
                case "view":
                    cls.clear_terminal()
                    print("View records")
                case "report":
                    cls.clear_terminal()
                case "exit":
                    cls.clear_terminal()
                    print("Exiting PennyTracker now")
                    sleep(2)
                    break
                case "analytics":
                    cls.clear_terminal()
                    print("Analytics")
                case "help":
                    cls.clear_terminal()
                    print("Help")
                case _:
                    print(f"'{choice}' is an unknown option")

def main():
    PennyTracker.clear_terminal()
    PennyTracker.start()

if __name__ == "__main__":
    main()
