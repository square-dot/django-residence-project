from django.urls import path
from . import views
from django.views.generic import RedirectView



urlpatterns = [
    path("", RedirectView.as_view(url="week_view", permanent=True)),
    path("week_view", views.WeekView.as_view(), name="week_view"),
    path("date_picker", views.CalendarView.as_view(), name="date_picker"),
    path("meal_list", views.MealsListView.as_view(), name="meals"),
    path("day_meals", views.DayMeals.as_view(), name="day_meals"),
    path("list_of_users", views.list_of_users, name="list_of_users"),
    path("user_detail/<int:pk>", views.UserDetailView.as_view(), name="user_detail"),
]