import copy
from datetime import date
from django import forms
from partial_date.fields import PartialDate


class OptionalNumberInput(forms.TextInput):
    input_type = 'number'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['required'] = False
        return context


class PartialDateWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        self.is_required = False
        my_attrs = {}
        if attrs is not None:
            my_attrs.update(attrs)
        day_attrs = copy.copy(my_attrs)
        month_attrs = copy.copy(my_attrs)
        year_attrs = copy.copy(my_attrs)

        day_attrs.update({'maxlength': 2,
                     'min': 1,
                     'max': 31,
                    })
        month_attrs.update({'maxlength': 2,
                       'min': 1,
                       'max': 12,
                      })
        year_attrs.update({'maxlength': 4,
                      'min': attrs.get('min_year', 1900),
                      'max': attrs.get('max_year', 2099),
                      })
        widgets = [
            OptionalNumberInput(attrs=month_attrs),
            OptionalNumberInput(attrs=day_attrs),
            forms.NumberInput(attrs=year_attrs),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.month, value.day, value.year]
        elif isinstance(value, PartialDate):
            month, day = None, None
            year = value.date.year
            if value.precisionMonth() or value.precisionDay():
                month = value.date.month
            if value.precisionDay():
                day = value.date.day
            return [month, day, year]
        elif isinstance(value, str):
            to_unpack = list(reversed(value.split('-')))
            month, day = '', ''
            year = to_unpack.pop()
            if to_unpack:
                month = to_unpack.pop()
            if to_unpack:
                day = to_unpack.pop()
            return [month, day, year]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        month, day, year = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.
        output = [year]
        if month:
            output.append(month)
        if day:
            output.append(day)

        partial_date_string = "-".join(output)

        return partial_date_string

    def get_context(self, name, value, attrs):
        attrs['required'] = False
        ctx = super().get_context(name, value, attrs)
        return ctx