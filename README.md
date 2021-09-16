django_partial_date
================

Django custom model field for partial dates with the form YYYY, YYYY-MM, YYYY-MM-DD

 * Works with DRF
 * Supports comparison operations
 * Supports Django 2.0 and Django 3.0
 * Provides a Widget and a form control (extremely basic, only supports M-D-Y at the moment because USA)

Usage
================

install the package

```bash
pip install django_partial_date
```


## partial_date.PartialDateField

A django model field for storing partial dates. Accepts None, a partial_date.PartialDate object, or a formatted string such as YYYY, YYYY-MM, YYYY-MM-DD. In the database it saves the date in a column of type DateTimeField and uses the seconds to save the level of precision.

## class partial_date.PartialDate

Object to represent the partial dates.

## class partial_date.PartialDateFormField

A field to add to a form. Rendered as three number inputs; the first and second (Month and Day) can be left blank. Its `clean()` method returns a `PartialDate` object.
Pass `min_year` or `max_year` to the constructor to set the limits; otherwise they'll default to 1900 and 2099, respectively. 

This is the default control for PartialDateField.

## class partial_data.PartialDateWidget

A widget to render the field above. Can be used by itself, too. Set the `min_year` and `max_year` attrs to override
the defaults of 1900 and 2099, respectively.


## Example

models.py
```python
from django.db import models
from partial_date import PartialDateField

class TestModel(models.Model):
    some_partial_date = PartialDateField()
```

```python
>>> from partial_date import PartialDate
>>> from core.models import TestModel
>>> obj = TestModel(some_partial_date="1995")
>>> obj.save()
>>> obj.some_partial_date
'1995'
>>> obj.some_partial_date = PartialDate("1995-09")
>>> obj.save()
>>> obj.some_partial_date
1995-09
>>>
```

```python
>>> from partial_date import PartialDate
>>> import datetime
>>> partial_date_instance = PartialDate(datetime.date(2012, 9, 21), precision=PartialDate.DAY)
>>> partial_date_instance
2012-09-21
>>> partial_date_instance.precisionYear()
False
>>> partial_date_instance.precisionMonth()
False
>>> partial_date_instance.precisionDay()
True
>>> partial_date_instance.precision == PartialDate.YEAR
False
>>> partial_date_instance.precision == PartialDate.MONTH
False
>>> partial_date_instance.precision == PartialDate.DAY
True
>>> partial_date_instance.precision = PartialDate.MONTH
>>> partial_date_instance
2012-09
>>> partial_date_instance = PartialDate("2015-11-01")
>>> partial_date_instance.date
datetime.date(2015, 11, 1)
```


```python
>>> from partial_date import PartialDate
>>> partial_date_instance = PartialDate("2015-11-01")
>>> partial_date_instance
2015-11-01
>>> partial_date_instance.format('%Y', '%m/%Y', '%m/%d/%Y') # .format(precision_year, precision_month, precision_day)
'11/01/2015'
>>> partial_date_instance = PartialDate("2015-11")
>>> partial_date_instance
2015-11
>>> partial_date_instance.format('%Y', '%m/%Y', '%m/%d/%Y')
'11/2015'
>>> partial_date_instance = PartialDate("2015")
>>> partial_date_instance
2015
>>> partial_date_instance.format('%Y', '%m/%Y', '%m/%d/%Y')
'2015'
```

Thanks for their collaborations to
- lorinkoz
- howieweiner
- jghyllebert
