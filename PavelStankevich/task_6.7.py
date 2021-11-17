# Task 6.7
#
# Implement a class Money to represent value and currency.
# You need to implement methods to use all basic arithmetics expressions 
# (comparison, division, multiplication, addition and subtraction).
# Tip: use class attribute exchange rate which is dictionary and stores 
# information about exchange rates to your default currency:
# 
# exchange_rate = {
#     "EUR": 0.93,
#     "BYN": 2.1,
#     ...
# }


from functools import total_ordering

@total_ordering
class Money:
    """
    The Money object contains value and currency. It supports
    basic arithmetic operations on the same objects and numbers.
    """
    exchange_rate = {
        "USD": 1,
        "EUR": 0.85,
        "BYN": 2.5,
        "JPY": 110.4,
    }
  
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency
        self.rates = {key: value / self.exchange_rate[currency] * \
                      amount for key, value in self.exchange_rate.items()}
  
    def __repr__(self):
        return f"Money(amount={self.amount:.2f}, currency={self.currency})"
  
    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"
      
    def __add__(self, other):
        if isinstance(other, Money):
            result = self.amount + other.rates[self.currency]
        elif isinstance(other, int) or isinstance(other, float):
            result = self.amount + other
        return Money(result, self.currency)
  
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, Money):
            result = self.amount - other.rates[self.currency]
        elif isinstance(other, int) or isinstance(other, float):
            result = self.amount - other
        return Money(result, self.currency)
    
    def __rsub__(self, other):
        return self.__sub__(other)
  
    def __mul__(self, other):
        if isinstance(other, Money):
            result = self.amount * other.rates[self.currency]
        elif isinstance(other, int) or isinstance(other, float):
            result = self.amount * other
        return Money(result, self.currency)
    
    def __rmul__(self, other):
        return self.__mul__(other)
  
    def __truediv__(self, other):
        if isinstance(other, Money):
            result = self.amount / other.rates[self.currency]
        elif isinstance(other, int) or isinstance(other, float):
            result = self.amount / other
        return Money(result, self.currency)
  
    def __rtruediv__(self, other):
        return self.__truediv__(other)
  
    def __eq__(self, other):
        if isinstance(other, Money):
            return self.amount == other.rates[self.currency]
        elif isinstance(other, int) or isinstance(other, float):
            return self.amount == other
  
    def __lt__(self, other):
        if isinstance(other, Money):
            return self.amount < other.rates[self.currency]
        elif isinstance(other, int) or isinstance(other, float):
            return self.amount == other


x = Money(10, "BYN")
y = Money(11) # define your own default value, e.g. “USD”
z = Money(12.34, "EUR")
print(z + 3.11 * x + y * 0.8) # result in “EUR”

lst = [Money(10,"BYN"), Money(11), Money(12.01, "JPY")]
s = sum(lst)
print(s) #result in “BYN”