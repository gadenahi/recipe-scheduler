import calendar
from collections import deque
import datetime
from datetime import timezone
import itertools
from recipe_scheduler.models import Event, Recipe


class BaseCalendarMixin:
    """
    Base calender
    """
    first_weekday = 6  # 0 is Monday. 6 is Sunday
    week_names = ['M', 'T', 'W', 'T', 'F', 'S', 'S']

    def setup_calendar(self):
        """
        Instance the calender.Calender class
        """
        self._calendar = calendar.Calendar(self.first_weekday)

    def get_week_names(self):
        """
        Shift week_names by first_weekday
        """
        week_names = deque(self.week_names)
        week_names.rotate(-self.first_weekday)
        return week_names


class MonthCalendarMixin(BaseCalendarMixin):
    """
    Monthly Calendar
    """

    def get_previous_month(self, date):
        """
        Previous Month
        :param date:
        :return:
        """
        if date.month == 1:
            return date.replace(year=date.year-1, month=12, day=1)
        else:
            return date.replace(month=date.month-1, day=1)

    def get_next_month(self, date):
        """
        Next Month
        :param date:
        :return:
        """
        if date.month == 12:
            return date.replace(year=date.year+1, month=1, day=1)
        else:
            return date.replace(month=date.month+1, day=1)

    def get_month_days(self, date):
        """
        :param date:
        :return: all days of the month
        """
        return self._calendar.monthdatescalendar(date.year, date.month)

    def get_current_month(self, year, month):
        """
        current month
        :param year:
        :param month:
        :return:
        """
        if month and year:
            month = datetime.date(year=int(year), month=int(month), day=1)
        else:
            month = datetime.date.today().replace(day=1)
        return month

    def get_month_schedules(self, start, end, days, group):
        check_event = Event.query.filter(
            Event.event_date.between(start, end)).filter_by(
            group_id=group).all()

        day_schedules = {day: {0: None, 1: None, 2: None} for week in days
                         for day in week}

        for e in check_event:
            r = Recipe.query.filter_by(id=e.recipe_id).first()
            if e.event_type == 0:
                day_schedules[e.event_date][0] = [r, e]
            elif e.event_type == 1:
                day_schedules[e.event_date][1] = [r, e]
            else:
                day_schedules[e.event_date][2] = [r, e]
        size = len(day_schedules)
        return [{key: day_schedules[key] for key in
                 itertools.islice(day_schedules, i, i + 7)} for i in
                range(0, size, 7)]

    def get_month_calendar(self, year, month, group):
        """
        :param year:
        :param month:
        :return: calendar information at dict
        """
        self.setup_calendar()
        current_month = self.get_current_month(year, month)
        calendar_data = {
            # 'now': datetime.datetime.now().date(),
            'now': datetime.datetime.now(datetime.timezone(
            datetime.timedelta(hours=-8))).date(),
            'month_days': self.get_month_days(current_month),
            'month_current': current_month,
            'month_previous': self.get_previous_month(current_month),
            'month_next': self.get_next_month(current_month),
            'week_names': self.get_week_names(),
        }
        month_days = calendar_data['month_days']
        month_first = month_days[0][0]
        month_last = month_days[-1][-1]
        calendar_data['month_day_schedulers'] = self.get_month_schedules(
            month_first,
            month_last,
            month_days,
            group
        )

        return calendar_data


class MonthCalendar(MonthCalendarMixin):
    def get_context_data(self, year, month, group):
        calendar_context = self.get_month_calendar(year, month, group)
        return calendar_context
