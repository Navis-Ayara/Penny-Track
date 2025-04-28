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

    @staticmethod
    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @classmethod
    def show_panel(cls):
        cls.console.print(cls.panel)

    @classmethod
    def select_category(cls):
        cls.categories.append("new category")
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
    def start(cls):
        while True:
            choice = input("> ")

            match choice:
                case "add":
                    PennyTracker.clear_terminal()
                    category = cls.select_category()
                    amount = int(input("Amount: "))
                    PennyTracker.clear_terminal()
                    print("Records have been updated successfully!")
                    PennyTracker.show_panel()
                case "view":
                    pass
                case "report":
                    pass
                case "exit":
                    PennyTracker.clear_terminal()
                    print("Exiting PennyTracker now")
                    sleep(2)
                    break
                case "analytics":
                    pass
                case _:
                    print(f"'{choice}' is an unknown option")

def main():
    PennyTracker.clear_terminal()
    PennyTracker.show_panel()

    PennyTracker.start()

if __name__ == "__main__":
    main()
