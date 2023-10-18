import pycountry
from typing import Optional


def country_code_to_name(code: str) -> Optional[str]:
    country = pycountry.countries.get(alpha_2=str.upper(code))
    if country is not None:
        return country.name
    else:
        print("Country code is invalid")
        return None


def country_name_to_code(name: str) -> Optional[str]:
    country = pycountry.countries.get(name=name)
    if country is not None:
        return country.alpha_2
    else:
        print("Country name is invalid")
        return None
