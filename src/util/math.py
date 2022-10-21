def round_all(values, decimals=None):
    return [round_(v, decimals)for v in values]


def round_(value, decimals=None):
    return round(value, decimals) if decimals is not None and decimals >= 0 else value