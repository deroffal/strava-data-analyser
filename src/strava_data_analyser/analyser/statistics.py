from enum import Enum

BetterWhen = Enum("BetterWhen", [('HIGH', 'high'), ('LOW', 'low')])



def _get_percentile_for(_df, _col, _value, _order=BetterWhen.HIGH) -> dict:
    _better_performance_filter = _col > _value if _order == BetterWhen.HIGH else _col < _value
    _better_count = _df.filter(_better_performance_filter).height
    return {
        'percentile': int(round(1 - _better_count / _df.height, 2) * 100),
        'rank': _better_count + 1,
        'total': _df.height
    }
