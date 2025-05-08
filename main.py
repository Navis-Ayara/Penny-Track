import json
import os
from time import sleep
from collections import defaultdict
from datetime import datetime

import rich.panel
import rich.console
import inquirer
import matplotlib.pyplot as plt
import numpy as np

from database import add_entry, get_entries, database

class PennyTracker:
    console = rich.console.Console()
    panel = rich.panel.Panel.fit(
        "[bold yellow]Penny Track [/ bold yellow]\nA personal finance CLI\n\nCommands: add | view | report | analytics | exit",
        border_style="white"
    )

    with open("categories.json", "r") as file:
        categories = json.load(file)
        categories = [category.capitalize() for category in categories]
        
    @classmethod
    def start(cls):
        while True:
            cls.show_panel()
            choice = input("> ")
            cls.clear_terminal()
            match choice:
                case "add":
                    category = cls.select_category()
                    amount = cls.get_amount()
                    add_entry(category, amount)
                    cls.clear_terminal()
                    print("Records have been updated successfully!")
                case "view":
                    entries = get_entries()
                    cls.create_table(entries)
                    input("Press Enter to continue...")
                    cls.clear_terminal()
                case "report":
                    if len(database) == 0:
                        print("No records found.")
                        input("Press Enter to continue...")
                        cls.clear_terminal()
                    else:
                        
                        print("Analytics report generated successfully!")
                case "exit":
                    cls.clear_terminal()
                    print("Exiting PennyTracker now")
                    sleep(2)
                    break
                case "analytics":
                    """
                    Since it's just a practice project, the plot shows all entries over time
                    """
                    grouped_data = defaultdict(list)
                    for entry in get_entries():
                        category = entry["category"]
                        date = datetime.strptime(entry["date"], "%Y-%m-%d")
                        amount = float(entry["amount"])
                        grouped_data[category].append((date, amount))

                    # Plot each category
                    plt.figure(figsize=(10, 6))
                    for category, data in grouped_data.items():
                        # Sort data by date
                        data.sort(key=lambda x: x[0])
                        dates, amounts = zip(*data)
                        plt.plot(dates, amounts, label=category)

                    # Add labels, title, and legend
                    plt.xlabel("Date")
                    plt.ylabel("Amount")
                    plt.title("Spending Over Time by Category")
                    plt.legend()
                    plt.grid(True)
                    plt.show()
                    cls.clear_terminal()
                case _:
                    print(f"'{choice}' is an unknown option")

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
                choices=[
                    category.capitalize() for category in cls.categories
                ] + ["New category"],
            )
        ]

        answer = inquirer.prompt(question)
        if answer:
            if answer['option'] == "New category":
                category_name = input("Enter a new category name: ")
                cls.add_category(category_name)
                return category_name
            else:
                return answer["option"]
        else:
            cls.clear_terminal()
            cls.select_category()
    
    @classmethod
    def add_category(cls, category_name :str):
        if category_name.capitalize() not in cls.categories:
            cls.categories.append(category_name)
            with open("categories.json", "w") as file:
                json.dump(cls.categories, file)
            print(f"Category '{category_name}' added successfully!")
        else:
            print(f"Category '{category_name}' already exists.")
            cls.select_category()
            
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
            cls.clear_terminal()
            cls.get_amount()

    @classmethod
    def create_table(cls, entries):
        if entries:
            table = rich.table.Table(title="Records")
            table.add_column("Category", style="cyan")
            table.add_column("Amount", style="magenta")
            table.add_column("Date", style="green")

            for entry in entries:
                table.add_row(entry["category"], str(entry["amount"]), entry["date"])

            cls.console.print(table)
        else:
            print("No records found.")

def main():
    PennyTracker.clear_terminal()
    PennyTracker.start()

if __name__ == "__main__":
    main()
