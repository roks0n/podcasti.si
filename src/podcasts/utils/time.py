from django.utils import timezone


def pretty_date(datetime):
    output = None
    now = timezone.now()
    diff = now - datetime

    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        output = ''

    elif day_diff == 0:
        if second_diff < 10:
            output = 'ravnokar'
        elif second_diff < 60:
            output = '{} sekund nazaj'.format(second_diff)
        elif second_diff < 120:
            return 'pred minuto'
        elif second_diff < 3600:
            output = '{} minut nazaj'.format(round(second_diff / 60))
        elif second_diff < 7200:
            output = 'pred eno uro'
        elif second_diff < 86400:
            output = '{} ur nazaj'.format(round(second_diff / 3600))

    elif day_diff == 1:
        output = 'Včeraj'

    elif day_diff < 30:
        output = '{} dni nazaj'.format(day_diff)

    if not output:
        output = datetime.strftime('%d.%m.%Y')

    return output
