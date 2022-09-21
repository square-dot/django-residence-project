from django.shortcuts import render
from meals.models import Meal, Resident
from meals.support_classes import Week
from datetime import date
from meals.forms import FormForDate, FormForDate, DayForm, BulkPickerForm
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.core.exceptions import ValidationError
from meals.forms import string_to_date


class WeekView(View, LoginRequiredMixin, PermissionRequiredMixin):
    template_name = "week_view.html"
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    permission_required = 'can_reserve_meal'

    def get(self, request):
        days_of_week = Week.days_of_week(date.today())
        return self.__render(request, days_of_week)

    def __render(self, request, days_of_week):
        return render(
            request,
            self.template_name,
            {
                "bulk_lunches": BulkPickerForm(
                    {"date": days_of_week[0], "meal_type": Meal.LUNCH}
                ),
                "bulk_dinners": BulkPickerForm(
                    {"date": days_of_week[0], "meal_type": Meal.DINNER}
                ),
                "monday_form": DayForm.populated(days_of_week[0], request.user.id),
                "tuesday_form": DayForm.populated(days_of_week[1], request.user.id),
                "wednesday_form": DayForm.populated(days_of_week[2], request.user.id),
                "thursday_form": DayForm.populated(days_of_week[3], request.user.id),
                "friday_form": DayForm.populated(days_of_week[4], request.user.id),
                "saturday_form": DayForm.populated(days_of_week[5], request.user.id),
                "sunday_form": DayForm.populated(days_of_week[6], request.user.id),
            },
        )

    def post(self, request):
        a_date = date.today()
        if "date_change" in request.POST:
            date_form = FormForDate(request.POST)
            if not date_form.is_valid():
                return ValidationError("Expected date change but form not valid")
            a_date = string_to_date(date_form["date"].value())

        if "bulk_pick" in request.POST:
            bulk_form = BulkPickerForm(request.POST)
            if not bulk_form.is_valid():
                return ValidationError("Expected bulk picker form but form not valid")
            bulk_form.process(request.user)
            a_date = string_to_date(bulk_form["date"].value())

        else:
            day_form = DayForm(request.POST)
            if not day_form.is_valid():
                return ValidationError("Expected day form but form not valid")
            day_form.process(request.user)
            a_date = string_to_date(day_form["date"].value())

        return self.__render(
                request, Week.days_of_week(a_date)
            )


class CalendarView(View, LoginRequiredMixin, PermissionRequiredMixin):
    template_name = "date_picker.html"

    def get(self, request):
        date_input = FormForDate(initial={"date": date.today()})
        return render(request, self.template_name, {"date_input": date_input})


class KitchenCalendarView(View, LoginRequiredMixin, PermissionRequiredMixin):
    template_name = "date_picker.html"

    def get(self, request):
        date_input = FormForDate(initial={"date": date.today()})
        return render(request, self.template_name, {"date_input": date_input})


def list_of_users(request):
    all_users = {"all_users_list": Resident.objects.all()}
    template_name = "meals/list_of_users.html"
    return render(request, template_name, all_users)


class Login(LoginView):
    template_name = "login.html"
    next = "week_view"


def logout_view(request):
    logout(request)
    return render(request, 'logged_out.html')

class MealsListView(ListView, LoginRequiredMixin):
    model = Meal


class DayMeals(View, LoginRequiredMixin):
    template_name = "day_meals.html"

    def get(self, request):
        day = date.today()
        all_meals = Meal.objects.filter(day=day)
        lunches = [x.user for x in all_meals.filter(meal_type=Meal.LUNCH)]
        dinners = [x.user for x in all_meals.filter(meal_type=Meal.DINNER)]

        return render(
            request,
            self.template_name,
            {
                Meal.LUNCH: lunches,
                Meal.DINNER: dinners,
            },
        )


class UserDetailView(DetailView):
    model = Resident
