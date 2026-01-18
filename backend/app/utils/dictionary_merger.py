from typing import Dict, Any
def update_dict(current: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    current = current or {}
    new = new or {}
    return {**current, **new}