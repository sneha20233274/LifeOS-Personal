from datetime import date

def coerce_date(value):
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value)
    raise TypeError(f"Invalid deadline type: {type(value)}")

#rehydration helper after convertin into json by normalize payload date becomes string so it is used to rehydate it
