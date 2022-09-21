from datetime import timedelta
from meals.models import Meal

class Week:
    
    @staticmethod
    def days_of_week(a_day):
        weekday = a_day.isoweekday()
        start_of_week = a_day - timedelta(days=weekday - 1) #starts on monday
        return [start_of_week + timedelta(days=d) for d in range(7)]

    def __init__(self, a_day, a_user):
        days = self.days_of_week(a_day)
        self.dict = {every_day : Meal.meals(a_day, a_user) for every_day in days}

