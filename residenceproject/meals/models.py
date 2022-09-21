from django.db import models
from django.contrib.auth.models import AbstractUser

class Resident(AbstractUser):
    pass


class Meal(models.Model):
    BREAKFAST = "BR"
    LUNCH = "LU"
    DINNER = "DI"
    MEAL_TYPE = [
        (BREAKFAST, "Breakfast"),
        (LUNCH, "Lunch"),
        (DINNER, "Dinner"),
    ]

    day = models.DateField()
    user = models.ForeignKey(Resident, on_delete=models.CASCADE)
    meal_type = models.CharField(
        max_length=2,
        choices=MEAL_TYPE,
        default=LUNCH,
    )

    @staticmethod
    def exists(a_day, a_user_id, a_meal):
        if a_user_id is None:
            return False
        a_user = Resident.objects.get(id=a_user_id)
        day_meals = Meal.objects.filter(day=a_day).filter(meal_type=a_meal).filter(user=a_user)
        return day_meals.exists()

    @staticmethod
    def set_in_db(a_day, a_user, a_meal_type, tof):
        in_db = (
                Meal.objects.filter(day=a_day)
                .filter(user=a_user)
                .filter(meal_type=a_meal_type)
            )
        if in_db.exists() and not tof:
            in_db.delete()
        elif not in_db.exists() and tof:
            Meal.objects.create(day=a_day, user=a_user, meal_type=a_meal_type)


    @staticmethod
    def meals(a_day, user):
        return {
                "date": a_day,
                Meal.LUNCH: Meal.LUNCH
                if Meal.exists(a_day, user, Meal.LUNCH)
                else "",
                Meal.DINNER: Meal.DINNER
                if Meal.exists(a_day, user, Meal.DINNER)
                else "",
            }

    class Meta:
        constraints = [models.constraints.UniqueConstraint(
            fields=["day", "user", "meal_type"], name="one_meal_per_person"
        )]
        # permissions = ("can_reserve_meal", )

    def meal_description(self):
        return next((x[1] for x in self.MEAL_TYPE if self.meal_type == x[0]))

    def __str__(self):
        return (
            self.day.strftime("%Y-%m-%d")
            + " - "
            + self.user.first_name
            + " "
            + self.user.last_name
            + " - "
            + self.meal_description()
        )

