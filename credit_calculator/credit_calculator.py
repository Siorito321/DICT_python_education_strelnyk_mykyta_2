import math
import argparse

parser = argparse.ArgumentParser(description="Calculates loan")


parser.add_argument("--type", default=None, help="The type of payment: 'annuity' or 'diff'")
parser.add_argument("--payment", default=None, help="The monthly payment amount")
parser.add_argument("--principal", default=None, help="The loan principal amount")
parser.add_argument("--periods", default=None, help="The number of payments required to pay off the loan")
parser.add_argument("--interest", default=None, help="The annual interest rate")

args = parser.parse_args()


class LoanCalc:
    """Provides methods to calculate the monthly payments,
     loan principal, and number of months needed to repay a loan based on user input."""

    def __init__(self):
        self.principal = 0
        self.monthly_payment = 0
        self.n_payments = 0
        self.loan_interest = 0
        self.attrib = {"princ": self.principal, "m_pay": self.monthly_payment, "pays": self.n_payments,
                       "inter": self.loan_interest}
        self.attrib_names = {"princ": "principal", "m_pay": "monthly payment", "pays": "number of months",
                       "inter": "loan interest"}

    def n_months_get(self) -> str:
        """
        Calculates the number of monthly payments needed to pay off the loan.

        Parameters:
        None

        Returns:
        str: a string indicating the number of years and months required to pay off the loan
        """
        i = float(self.attrib["inter"]) / 1200
        p = float(self.attrib["princ"])
        try:
            n = math.ceil(math.log((float(self.attrib["m_pay"]) / (float(self.attrib["m_pay"]) - i * p)), 1 + i))
        except ValueError:
            print("Your data is incorrect! Formula can not calculate the result")
            return "Please, check your data"
        else:
            years = n // 12
            months = math.ceil(n % 12)
            total = float(self.attrib["m_pay"]) * n
            overpayment = int(total - p)
            if years == 0:
                return f"It will take {months} months to repay this loan!\nTotal overpayment is: {total}"
            if months == 0:
                return f"It will take {years} years to repay this loan!\nTotal overpayment is: {total}"
            else:
                return f"It will take {years} years and {months} months to repay this loan!" \
                       f"\nTotal overpayment is: {total}"

    def principal_get(self) -> str:
        """
        Calculates the loan principal based on the given monthly payment, interest rate, and number of payments.

        Parameters:
        None

        Returns:
        str: a string indicating the loan principal amount
        """
        A = float(self.attrib["m_pay"])
        i = float(self.attrib["inter"]) / 1200
        n = int(self.attrib["pays"])
        try:
            p = A * 1 / (i * (1 + i) ** n / ((1 + i) ** n - 1))
        except ValueError:
            return "Your data is incorrect!"
        else:
            return f"Your principal is {round(p, 2)}!\nTotal overpayment is: {int((A * n) - p)}"

    def annuity_get(self) -> str:
        """
        Calculates the annuity monthly payment amount based on the given loan principal,
         interest rate, and number of payments.

        Parameters:
        None

        Returns:
        str: a string indicating the annuity monthly payment amount
        """
        i = float(int(self.attrib["inter"]) / 1200)
        n = int(self.attrib["pays"])
        p = int(self.attrib['princ'])
        try:
            a = p * (i * (1 + i) ** n) / ((1 + i) ** n - 1)
        except ValueError:
            return "Your data is incorrect!"
        else:
            return f"Your annuity monthly payment amount is {round(a, 2)}!\nTotal overpayment is: {int((a * n) - p)}"

    def diff(self) -> None:
        """
        Calculates differential monthly payments for a loan with varying interest rates, based on
        the given loan principal, interest rate, and number of payments.

        Parameters: None

        Returns: None
        """
        i = float(int(self.attrib["inter"]) / 1200)
        n = int(self.attrib["pays"])
        p = int(self.attrib['princ'])
        total = 0
        for k in range(n):
            D = p / n + 1 * (p - p * (k - 1) / n)
            total += D
            print(f"Month {k + 1}: payment is {round(D)}")
        print(f"Total overpayment is: {int(total - p)}")


try:
    a = LoanCalc()
    if args.type == "annuity":
        if args.principal is not None and args.payment is not None and args.interest is not None:
            a.attrib["princ"] = float(args.principal)
            a.attrib["m_pay"] = float(args.payment)
            a.attrib["inter"] = float(args.interest)
            print(a.n_months_get())
        elif args.principal is not None and args.periods is not None and args.interest is not None:
            a.attrib["princ"] = float(args.principal)
            a.attrib["inter"] = float(args.interest)
            a.attrib["pays"] = float(args.periods)
            print(a.annuity_get())

        elif args.payment is not None and args.periods is not None and args.interest is not None:
            a.attrib["m_pay"] = float(args.payment)
            a.attrib["inter"] = float(args.interest)
            a.attrib["pays"] = float(args.periods)
            print(a.principal_get())

        else:
            raise ValueError
    elif args.type == "diff":
        if args.principal is not None and args.periods is not None and args.interest is not None:
            a.attrib["princ"] = float(args.principal)
            a.attrib["pays"] = float(args.periods)
            a.attrib["inter"] = float(args.interest)
            a.diff()

    else:
        raise ValueError
except (ValueError, TypeError):
    print("Incorrect parameters")

