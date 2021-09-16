from django import forms
from django.core.validators import ValidationError
from partial_date.fields import PartialDate
from partial_date.widget import PartialDateWidget


def vali_date(a_tentative_partial_date_as_a_string):
    try:
        _ = PartialDate(a_tentative_partial_date_as_a_string)
    except:
        raise ValidationError(f"{a_tentative_partial_date_as_a_string} is not a valid (partial) date")


class PartialDateFormField(forms.MultiValueField):
    default_validators = [vali_date]

    def __init__(self, *args, **kwargs):
        if 'min_year' in kwargs:
            min_year = kwargs.pop('min_year')
        else:
            min_year = 1900

        if 'max_year' in kwargs:
            max_year = kwargs.pop('max_year')
        else:
            max_year = 2099

        my_fields = [forms.CharField(help_text="Please enter a month"),
                     forms.CharField(help_text="Please enter a day"),
                     forms.IntegerField(min_value=min_year, max_value=max_year)]
        if 'widget' not in kwargs:
            kwargs['widget'] = PartialDateWidget({'min_year': min_year, 'max_year': max_year})
        super().__init__(fields=my_fields, *args, **kwargs)

    def compress(self, data_list):
        """Expects values in a month-day-year sequence, because USA."""
        assert len(data_list) == 3
        m, d, y = data_list

        output = [y]
        if m:
            output.append(m)
        if d:
            output.append(d)

        partial_date_string = "-".join(output)
        return partial_date_string

    def clean(self, value):
        if self.required:
            if value is None:
                raise ValidationError('This field is required.')

        try:
            return PartialDate(value)
        except ValidationError:
            raise ValidationError("Please enter a complete, valid date in month, day, year "
                                  "order, or a month and year, or just a year.")
