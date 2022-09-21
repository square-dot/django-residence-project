from django import forms
from meals.models import Meal
from meals.support_classes import Week
from datetime import date

def string_to_date(str):
    elements = str.split("-")
    return date(int(elements[0]), int(elements[1]), int(elements[2]))


class DateInput(forms.DateInput):
    input_type = "date"
    width = "400pt"


class FormForDate(forms.Form):
    date = forms.DateField(widget=DateInput())


class BulkPickerForm(forms.Form):
    date = forms.DateField(widget=forms.HiddenInput())
    meal_type = forms.ChoiceField(
        choices=(
            (Meal.LUNCH, Meal.LUNCH),
            (Meal.DINNER, Meal.DINNER),
        ),
        widget=forms.HiddenInput,
    )

    def process(self, a_user):
        selected_date = string_to_date(self["date"].value())
        days_of_week = Week.days_of_week(selected_date)
        selected_meal_type = self["meal_type"].value()
        tof = not Meal.exists(selected_date, a_user.id, selected_meal_type)
        for a_day in days_of_week:
            Meal.set_in_db(a_day, a_user, selected_meal_type, tof)


class DayForm(forms.Form):
    not_picked = ("", "No")
    picked_string = "Yes"
    date = forms.DateField(widget=forms.HiddenInput())
    BR = forms.ChoiceField(
        required=False,
        choices=(
            not_picked,
            (Meal.BREAKFAST, picked_string),
        ),
        widget=forms.RadioSelect(attrs={"onchange": "submit()"}),
    )
    LU = forms.ChoiceField(
        required=False,
        choices=(
            not_picked,
            (Meal.LUNCH, picked_string),
        ),
        widget=forms.RadioSelect(attrs={"onchange": "submit()"}),
    )
    DI = forms.ChoiceField(
        required=False,
        choices=(
            not_picked,
            (Meal.DINNER, picked_string),
        ),
        widget=forms.RadioSelect(attrs={"onchange": "submit()"}),
    )

    @staticmethod
    def populated(day, user):
        return DayForm(Meal.meals(day, user))

    def process(self, a_user):
        a_day = self["date"].value()
        for m in Meal.MEAL_TYPE:
            Meal.set_in_db(a_day, a_user, m[0], self[m[0]].value())
