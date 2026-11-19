from datetime import datetime

try:
    start_date = datetime.strptime("2027-04-19", "%Y-%m-%d").date()
    end_date = datetime.strptime("2027-07-21", "%Y-%m-%d").date()

    if end_date <= start_date:
        print("End date must be after start date.")
    else:
        print("Dates are valid")
except ValueError:
    print("Please enter valid dates.")