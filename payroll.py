"""
Employee Payroll System (PS No. 27)
Concepts: Functions, Calculations, OOP (Classes + Inheritance), File Handling
"""

OVERTIME_RATE = 200      # Rs. per overtime hour
PF_RATE = 0.12           # 12% of basic
TAX_RATE = 0.10          # 10% of gross
TAX_LIMIT = 50000        # tax applies only if gross is above this
BONUS_RATE = 0.10        # manager bonus: 10% of basic
FILE_NAME = "payroll.txt"


class Employee:
    """A normal employee."""

    def __init__(self, emp_id, name, basic, overtime_hours):
        self.emp_id = emp_id
        self.name = name
        self.basic = basic
        self.overtime_hours = overtime_hours

    def calculate_overtime(self):
        return self.overtime_hours * OVERTIME_RATE

    def calculate_bonus(self):
        return 0                      # normal employees get no bonus

    def calculate_gross(self):
        return self.basic + self.calculate_overtime() + self.calculate_bonus()

    def calculate_pf(self):
        return self.basic * PF_RATE   # PF is on basic only

    def calculate_tax(self):
        gross = self.calculate_gross()
        return gross * TAX_RATE if gross > TAX_LIMIT else 0

    def calculate_net(self):
        return self.calculate_gross() - self.calculate_pf() - self.calculate_tax()


class Manager(Employee):
    """A manager is an Employee who also gets a 10% bonus on basic."""

    def calculate_bonus(self):        # overrides the Employee method
        return self.basic * BONUS_RATE


# ---------------- Functions ----------------

def build_payslip(emp):
    """Return the payslip as text (used for both screen and file)."""
    lines = [
        "=" * 36,
        f"Employee : {emp.emp_id}, {emp.name}",
        f"Basic    : {emp.basic:.0f}",
        f"Overtime : {emp.calculate_overtime():.0f}  ({emp.overtime_hours:g} hrs)",
    ]
    if isinstance(emp, Manager):      # show bonus only for managers
        lines.append(f"Bonus    : {emp.calculate_bonus():.0f}")
    lines += [
        f"Gross    : {emp.calculate_gross():.0f}",
        f"PF       : {emp.calculate_pf():.0f}",
        f"Tax      : {emp.calculate_tax():.0f}",
        f"NetSalary: {emp.calculate_net():.0f}",
        "=" * 36,
    ]
    return "\n".join(lines)


def print_payslip(emp):
    print("\n" + build_payslip(emp) + "\n")


def save_payslip(emp):
    """Append the payslip to payroll.txt (append mode keeps old payslips)."""
    with open(FILE_NAME, "a") as f:
        f.write(build_payslip(emp) + "\n\n")


def get_basic():
    while True:
        try:
            value = float(input("Basic salary: "))
            if value > 0:
                return value
        except ValueError:
            pass
        print("Invalid basic salary. Enter a positive number.")


def get_overtime():
    while True:
        try:
            value = float(input("Overtime hours: "))
            if value >= 0:
                return value
        except ValueError:
            pass
        print("Invalid overtime hours. Enter a non-negative number.")


def get_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def get_type():
    while True:
        choice = input("Type (1 = Employee, 2 = Manager): ").strip()
        if choice in ("1", "2"):
            return choice
        print("Please enter 1 or 2.")


def main():
    print("---- Employee Payroll System ----")
    while True:
        kind = get_type()
        emp_id = get_text("ID: ")
        name = get_text("Name: ")
        basic = get_basic()
        overtime = get_overtime()

        emp = Manager(emp_id, name, basic, overtime) if kind == "2" \
            else Employee(emp_id, name, basic, overtime)

        print_payslip(emp)
        save_payslip(emp)
        print(f"Payslip saved to {FILE_NAME}")

        if input("Add another employee? (y/n): ").strip().lower() != "y":
            break
    print("Thank you!")


if __name__ == "__main__":
    main()
