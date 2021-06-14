def createSpendChart(categories):
  categories_names = []  # x_axis
  separate_spend = []
  percentBySpend = []

  # fill the 2 lists above
  for category in categories:
    total = 0
    categories_names.append(category.name)
    for item in category.ledger:
      if item['amount'] < 0:
          total -= item['amount']
          separate_spend.append(total)

  graph = "Percentage spent by category\n"
  labels = range(100, -10, -10)
  totalSpent = sum(separate_spend)

  for spend in separate_spend:
    percent = (round(spend / totalSpent, 2)) * 100
    percentBySpend.append(percent)

  for label in labels:
    graph += str(label).rjust(3) + "|"
    for percent in percentBySpend:
      if percent >= label:
        graph += " o "
      
      else:
        graph += "   "

    graph += " \n"

  graph += ("    " + ("---" * len(categories_names)) + "-\n")

  max_length = len(categories_names[0])
  for name in categories_names:
    if len(name) > max_length:
      max_length = len(name)
  
  for i in range(max_length):
    graph += "    "
    for name in categories_names:
      if len(name) > i:
        graph += " " + name[i] + " "
      else:
        graph += "   "
    
    if i != (max_length - 1):
      graph += " \n"
    else:
      graph += " "
  
  return graph

class Category:
    def __init__(self, name):
        self.name = name
        self.ledger =[]
    
    def __str__(self):
        title = str(self.name).center(30, "*") + "\n"
        items = ""
        total = 0
        for item in self.ledger:
            items += f"{item['description'][:23]:23}" + f"{item['amount']:>7.2f}" + "\n"
            total += item['amount']
        output = title + items + "Total: {:.2f}".format(total)
        return output

    def check_funds(self, amount):
        balance = 0
        for item in self.ledger:
            balance += item["amount"]
        
        return balance >= amount
    
    def deposit(self, amount, description=""):
         self.ledger.append({"amount": amount, "description": description})
    
    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        balance = 0
        for item in self.ledger:
            balance += item["amount"]
        return balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
          description = "Transfer to " + category.name 
          self.ledger.append({"amount": -amount, "description": description})
          category.deposit(amount, "Transfer from " + self.name)
          return True
        return False
 
business = Category("Business")
food = Category("Food")
entertainment = Category("Entertainment")

food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")

food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)

print(createSpendChart([business, food, entertainment]))
