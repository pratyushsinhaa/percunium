import datetime

# NSE Holidays 2024 (add/update as needed)
NSE_HOLIDAYS_2024 = [
    datetime.date(2024, 1, 26),  # Republic Day
    datetime.date(2024, 3, 8),   # Maha Shivaratri
    datetime.date(2024, 3, 25),  # Holi
    datetime.date(2024, 3, 29),  # Good Friday
    datetime.date(2024, 4, 11),  # Eid-Ul-Fitr
    datetime.date(2024, 4, 17),  # Ram Navami
    datetime.date(2024, 5, 1),   # Maharashtra Day
    datetime.date(2024, 6, 17),  # Bakri Eid
    datetime.date(2024, 7, 17),  # Muharram
    datetime.date(2024, 8, 15),  # Independence Day
    datetime.date(2024, 9, 2),   # Ganesh Chaturthi
    datetime.date(2024, 10, 2),  # Gandhi Jayanti
    datetime.date(2024, 11, 1),  # Diwali-Laxmi Pujan*
    datetime.date(2024, 11, 15), # Gurunanak Jayanti
    datetime.date(2024, 12, 25), # Christmas
]

def is_holiday(date):
    """Check if a given date is a NSE holiday"""
    current_year_holidays = [d for d in NSE_HOLIDAYS_2024 if d.year == date.year]
    return date.date() in current_year_holidays

def nifty_market_is_open():
    """Check if the NSE market is open
    Returns:
        int: 1 if market is open, 0 if closed
    """
    try:
        now = datetime.datetime.now()
        
        if now.weekday() >= 5:  # Weekend check
            return 0
        
        if is_holiday(now):  # Holiday check
            return 0

        market_open_time = now.replace(hour=9, minute=15, second=0, microsecond=0)
        market_close_time = now.replace(hour=15, minute=30, second=0, microsecond=0)

        return 1 if market_open_time <= now <= market_close_time else 0
        
    except Exception as err:
        print(f"Error checking NSE market status: {err}")
        return 0





# CHECK IF THE FUNCTION IS WORKING OUTSIDE OF IT'S APPLICATION IN THE MAIN FOLDER
# if __name__ == "__main__":              
#     now = datetime.datetime.now()
#     if nifty_market_is_open():
#         print("The Indian stock market is open.")
#     else:
#         if now.weekday() >= 5:
#             print("The Indian stock market is closed (Weekend).")
#         elif is_holiday(now):
#             print("The Indian stock market is closed (Holiday).")
#         else:
#             print("The Indian stock market is closed (Outside trading hours).")