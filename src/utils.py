from datetime import datetime

def get_day_suffix(day: int) -> str:
    if 11 <= day <= 13:
        return 'th'
    match day % 10:
        case 1: return 'st'
        case 2: return 'nd'
        case 3: return 'rd'
        case _: return 'th'

def format_time(time: datetime) -> str:
    day = time.day
    suffix = get_day_suffix(day)
    return time.strftime(f"%A %B {day}{suffix} %I:%M %p").lower()