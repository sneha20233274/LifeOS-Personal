from datetime import date

def assert_deadline_type(deadline, context: str):
    if deadline is None:
        return
    if not isinstance(deadline, date):
        raise TypeError(
            f"[DEADLINE TYPE ERROR] {context}: "
            f"expected datetime.date | None, got {type(deadline)} -> {deadline!r}"
        )
