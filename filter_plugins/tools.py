from collections.abc import Iterable

class FilterModule(object):
    def filters(self):
        return {
            'enforce_list': self.enforce_list,
            'dict2records': self.dict2records,
        }

    def enforce_list(self, obj) -> list:
        """Normalize any value into a list."""
        if obj is None:
            return []
        if isinstance(obj, (str, bytes)):
            return [obj]
        if isinstance(obj, Iterable):
            return list(obj)
        return [obj]

    def dict2records(self, d: dict[str, dict], key: str = 'key') -> list[dict]:
        return [{
            key: k,
            **v
        } for k, v in d.items()]
