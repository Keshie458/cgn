from datetime import date

def calculate_depreciation(asset):
    if not asset.purchase_date or not asset.purchase_cost or not asset.useful_life:
        return None, None

    years_used = (date.today() - asset.purchase_date).days / 365.25
    depreciation_per_year = (asset.purchase_cost - (asset.salvage_value or 0)) / asset.useful_life
    accumulated = min(depreciation_per_year * years_used, asset.purchase_cost)
    book_value = max(asset.purchase_cost - accumulated, 0)

    return round(accumulated, 2), round(book_value, 2)