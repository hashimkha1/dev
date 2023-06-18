
def compute_pay(amount):
    if amount <= 2000:
        return 15
    elif amount <= 4000:
        return 15 + (amount - 2000) * (12.5 - 15) / 2000
    elif amount <= 6000:
        return 15 + 12.5 + (amount - 4000) * (10 - 12.5) / 2000
    else:
        return 15 + 12.5 + 10 + (amount - 6000) * (5 - 10) / 2000

