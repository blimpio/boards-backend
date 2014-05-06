import datetime

from django.utils.translation import ungettext as _
from django.utils.timezone import utc, get_current_timezone, now


def timesince(d):
    """
    Takes a datetime object and returns the time between d and now
    as a nicely formatted string, e.g. "10 minutes".

    Adapted from django.utils.timesince.timesince.
    """
    current_timezone = get_current_timezone()
    _date = d.astimezone(current_timezone)
    _now = now()

    today = datetime.datetime(_now.year, _now.month, _now.day, tzinfo=utc)
    delta = _now - _date
    delta_midnight = today - _date
    days = delta.days
    hours = int(round(delta.seconds / 3600., 0))
    minutes = int(round(delta.seconds / 60., 0))
    chunks = (
        (365.0, lambda n: _('year', 'years', n)),
        (30.0, lambda n: _('month', 'months', n)),
        (7.0, lambda n: _('week', 'weeks', n)),
        (1.0, lambda n: _('day', 'days', n)),
    )

    if days == 0:
        if hours == 0:
            if minutes > 0:
                return _('1 minute ago',
                         '{} minutes ago'.format(minutes), minutes)
            else:
                return 'less than 1 minute ago'
        else:
            return _('1 hour ago', '{} hours ago', hours).format(hours)

    if delta_midnight.days == 0:
        return 'yesterday at {}'.format(_date.strftime('%I:%M%p'))

    count = 0

    for i, (chunk, name) in enumerate(chunks):
        if days >= chunk:
            count = round((delta_midnight.days + 1) / chunk, 0)
            break

    return '{} {} ago'.format(count, name(count))
