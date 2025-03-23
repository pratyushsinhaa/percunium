from datetime import datetime, time
import holidays #type: ignore
import pytz

def nyse_market_is_open():
    """
    Checks whether the U.S. stock market (NYSE) is currently open.
    Returns:
        int: 1 if market is open, 0 if closed
    """
    try:
        eastern_tz = pytz.timezone('US/Eastern')
        current_time_eastern = datetime.now(eastern_tz)

        nyse_holidays = holidays.NYSE()
        today_date_str = current_time_eastern.strftime('%Y-%m-%d')
        is_holiday = nyse_holidays.get(today_date_str)
        if is_holiday:
            return 0

        day_of_week = current_time_eastern.weekday()
        if day_of_week == 5 or day_of_week == 6:
            return 0

        market_open_time = time(9, 0)
        market_close_time = time(16, 0)

        if market_open_time <= current_time_eastern.time() <= market_close_time:
            return 1
        else:
            return 0

    except Exception as err:
        print(err)
        return 0

# # Test the function
# if nyse_market_is_open() == 1:
#     print("The market is currently open.")
# else:
#     print("The market is currently closed.")