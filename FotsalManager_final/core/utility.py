from django.utils import timezone

def time_ago(timestamp):
    now = timezone.now()
    diff = now - timestamp
    if diff.days > 365:
        return f'{diff.days // 365} years ago'
    if diff.days > 30:
        return f'{diff.days // 30} months ago'
    if diff.days > 7:
        return f'{diff.days // 7} weeks ago'
    if diff.days > 0:
        return f'{diff.days} days ago'
    if diff.seconds > 3600:
        return f'{diff.seconds // 3600} hours ago'
    if diff.seconds > 60:
        return f'{diff.seconds // 60} minutes ago'
    return f'{diff.seconds} seconds ago'

