import requests
import json


class Exchanger:
    """A class for facilitating currency exchange operations."""

    def __init__(self) -> None:
        """Initialize the Exchanger class.

        Parameters:
        None

        Returns:
        None
        """
        self.your_currency_type = None
        self.exchange_cache = {}

    def exchange_courses_out(self) -> str:
        """Get and display exchange rates for a specific currency.

        Parameters:
        None

        Returns:
        str: Exchange rates for the specified currency.
        """
        self.your_currency_type = input("Enter your currency type>")
        r = requests.get(f"http://www.floatrates.com/daily/{self.your_currency_type}.json")
        rates = json.loads(r.text)
        return f"Rate for {self.your_currency_type} for USD is {rates['usd']['rate']}" \
               f" and for EUR is {rates['eur']['rate']}"

    def check_cache(self, currency_type, target) -> bool:
        """Check if a currency type exists in the exchange cache.

        Parameters:
        currency_type (str): The currency type to check.
        target (str): The currency that should be in self.exchange_cache[currency_type]

        Returns:
        bool: True if the currency type is found in the cache, False otherwise.
        """
        if currency_type in self.exchange_cache:
            if target in self.exchange_cache[currency_type]:
                return True
        return False

    def calculate_exchange(self, rate, amount) -> float:
        """Calculate the amount of money to be received based on a given exchange rate.

        Parameters:
        rate (float): The exchange rate between two currencies.
        amount (float): The amount of money to exchange.

        Returns:
        float: The amount of money to be received in the target currency.
        """
        exchange_amount = round(amount * rate, 2)
        return exchange_amount

    def calculate_exchange_cache(self, currency_type_1, currency_type_2, amount) -> float:
        """Calculate the amount of money to be received based on a cached exchange rate.

        Parameters:
        currency_type_1 (str): The currency type to exchange.
        currency_type_2 (str): The target currency type.
        amount (float): The amount of money to exchange.

        Returns:
        float: The amount of money to be received in the target currency.
        """
        rate = self.exchange_cache[currency_type_1][currency_type_2]
        exchange_amount = round(amount * rate, 2)
        return exchange_amount

    def exchange_currency(self) -> None:
        """Perform currency exchange.

        Parameters:
        None

        Returns:
        None
        """
        currency_type = input("Enter the currency you want to exchange (or leave empty to exit): ").lower()
        while True:
            if not currency_type:
                break

            target_currency = input("Enter the currency you want to receive (or leave empty to exit): ").lower()
            if target_currency == "":
                break
            amount = float(input("Enter the amount of money you want to exchange: "))

            print("Checking the cache...")
            if self.check_cache(currency_type, target_currency):
                print("It is in the cache!")
                exchange_amount = self.calculate_exchange_cache(currency_type, target_currency, amount)
            else:
                print("Sorry, but it is not in the cache!")
                try:
                    r = requests.get(f"http://www.floatrates.com/daily/{currency_type}.json")
                    rates = json.loads(r.text)
                    if target_currency.lower() in rates:
                        if currency_type not in self.exchange_cache:
                            self.exchange_cache[currency_type] = {}
                        exchange_amount = self.calculate_exchange(rates[target_currency]["rate"], amount)
                        self.exchange_cache[currency_type][target_currency] = rates[target_currency]["rate"]
                    else:
                        print("Invalid currency type.")
                        continue
                except json.decoder.JSONDecodeError:
                    print("Invalid currency you want to exchange")
                    currency_type = input("Enter the currency you want to exchange (or leave empty to exit): ").lower()
                    continue

            print(f"You received {exchange_amount} {target_currency}.\n")


ex = Exchanger()
ex.exchange_currency()
