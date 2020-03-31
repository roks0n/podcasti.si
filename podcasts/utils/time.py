from django.utils import timezone


def pretty_date(datetime):
    if not datetime:
        return "neznano"

    output = None
    now = timezone.now()
    diff = now - datetime

    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        output = ""

    elif day_diff == 0:
        if second_diff < 10:
            output = "ravnokar"
        elif second_diff < 60:
            output = "{} sekundami".format(second_diff)
        elif second_diff < 120:
            return "pred minuto"
        elif second_diff < 3600:
            output = "pred manj kot uro"
        elif second_diff < 7200:
            output = "pred 1 uro"
        elif second_diff < 10800:
            output = "pred 2 urama"
        elif second_diff < 86400:
            output = "pred {} urami".format(round(second_diff / 3600))

    elif day_diff == 1:
        output = "včeraj"

    elif day_diff < 3:
        output = "pred 2 dnevoma"

    elif day_diff < 30:
        output = "pred {} dnevi".format(day_diff)

    if not output:
        output = datetime.strftime("%d.%m.%Y")

    return output
