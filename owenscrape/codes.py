from typing import List, Set, Dict, Tuple, Optional
import re
from collections import namedtuple

LINES = {
    "BK": ("Books", "N/A"),
    "BM": ("Birkenstock", "Unisex"),
    "BW": ("Birkenstock", "Women"),
    "CM": ("Champion", "Men"),
    "CW": ("Champion", "Women"),
    "DL": ("DRKSHDW MiJ Capsule", "Unisex"),
    "DS": ("DRKSHDW", "Women"),
    "DU": ("DRKSHDW", "Men"),
    "HD": ("Hunrod", "Women"),
    "HU": ("Hunrod", "Unisex"),
    "LI": ("Lilies", "Women"),
    "NX": ("DRKSHDW Unknown", "Unisex"),
    "PM": ("Palais Royale", "Men"),
    "PR": ("Palais Royale", "Women"),
    "RA": ("Accessories", "Unisex"),
    "RB": ("Accessories", "Unisex"),
    "RF": ("Forever", "Unisex"),
    "RM": ("Precollection Adidas", "Unisex"),
    "RO": ("Runway", "Women"),
    "RP": ("Precollection", "Women"),
    "RR": ("Runway", "Men"),
    "RU": ("Precollection", "Men"),
    "RV": ("Collectables", "Unisex"),
    "RW": ("Runway Adidas", "Unisex"),
    "RW": ("Runway Adidas", "Unisex"),
    "VM": ("Veja", "Men"),
    "VW": ("Veja", "Women"),
}


Collection = namedtuple("Collection", ["year", "name", "season"])
COLLECTIONS = [
    Collection(*x)
    for x in (
        ("20", "PERFORMA", "FW"),
        ("20", "TECUATL", "SS"),
        ("19", "LARRY", "FW"),
        ("19", "BABEL", "SS"),
        ("18", "SISYPHUS", "FW"),
        ("18", "DIRT", "SS"),
        ("17", "GLITTER", "FW"),
        ("17", "WALRUS", "SS"),
        ("16", "MASTODON", "FW"),
        ("16", "CYCLOPS", "SS"),
        ("15", "SPHINX", "FW"),
        ("15", "FAUN", "SS"),
        ("14", "MOODY", "FW"),
        ("14", "VICIOUS", "SS"),
        ("13", "PLINTH", "FW"),
        ("13", "ISLAND", "SS"),
        ("12", "MOUNTAIN", "FW"),
        ("12", "NASKA", "SS"),
        ("11", "LIMO", "FW"),
        ("11", "ANTHEM", "SS"),
        ("10", "GLEAM", "FW"),
        ("10", "RELEASE", "SS"),
        ("09", "CRUST", "FW"),
        ("09", "STRUTTER", "SS"),
        ("08", "STAG", "FW"),
        ("08", "CREATCH", "SS"),
        ("07", "EXPLODER", "FW"),
        ("07", "WISHBONE", "SS"),
        ("06", "REVILLON", "FW"),
        ("06", "DUSTULATOR", "FW"),
        ("06", "TUNGSTEN", "SS"),
        ("05", "MOOG", "FW"),
        ("05", "SCORPIO", "SS"),
        ("04", "REVILLON", "FW"),
        ("04", "QUEEN", "FW"),
        ("04", "CITROEN", "SS"),
        ("03", "REVILLON", "FW"),
        ("03", "TRUCKER", "FW"),
        ("03", "SUKERBALL", "SS"),
        ("02", "SPARROWS", "FW"),
    )
]


class ParseCodeFailedException(Exception):
    """Exception raised for errors in the code.

    Attributes:
        raw_code -- input expression in which the error occurred
        component -- Portion of the code that parsing failed on
        message -- explanation of the error
    """

    def __init__(self, raw_code, component, message=None):
        self.raw_code = raw_code
        self.component = component
        self.message = message


def canonicalise_season(season: str):
    "Take a season in either FW/SS/AW/SS/F/S format and return 'F' or 'S'"
    season = season.upper()
    if season in {"FW", "AW", "F"}:
        return "F"
    elif season in {"SS", "S"}:
        return "S"
    else:
        raise ParseCodeFailedException(season, "Season", "Season Not Valid")


def find_collection(year: str, season: str) -> Collection:
    """Return the collection for a year and season"""
    season = canonicalise_season(season)
    for c in COLLECTIONS:
        if c.year == year and canonicalise_season(c.season) == season:
            return c
    error = ValueError()
    error.message = f"Collection {year}{season} not found"
    raise error


class ItemCode:
    def __init__(self, code: str):
        self.raw_code = code.strip()
        self.collection = None
        self.line = None
        self.gender = None
        self.item_code = None
        self.fabric_code = None
        self.colour_code = None

    def __str__(self):
        season = "Fall" if self.collection.season == "F" else "Spring"
        return f"{self.collection.name} {self.gender}'s {season} '{self.collection.year} | Item: {self.item_code} | Fabric: {self.fabric_code} | Colour: {self.colour_code}"

    def __repr__(self):
        return self.raw_code


class OldCode(ItemCode):
    pass


class NewCode(ItemCode):
    """Item code for FW13 Plinth and later"""
    def decode(self) -> ItemCode:
        """Decode an FW13 and later item code
        An example code like DU15F5152-R 09 contains six sections:
        DU | 15 | F | 5152 |-R | 09
        Line + Gender | Year | Season | Item Code | Fabric Code | Colour Code

        See for full details: https://docs.google.com/document/d/1DKGeJHMONInJ3ogZx1YHq4z6t9mXpbhcMAhFqhVYUwA/edit
        """
        code = re.sub("\\W", "", self.raw_code.upper())
        line, code = (code[:2], code[2:])
        if line in LINES:
            self.line, self.gender = LINES[line][0], LINES[line][1]
        else:
            raise ParseCodeFailedException(self.raw_code, "Line")

        valid_years = {c.year for c in COLLECTIONS}
        year, code = code[:2], code[2:]
        if not year in valid_years:
            raise ParseCodeFailedException(self.raw_code, "Year")

        self.collection, code = find_collection(year, code[:1]), code[1:]

        codes: Dict[str, str] = dict(item="", fabric="", colour="")
        component_sequence = (("item", "\\d"), ("fabric", "[A-Z]"), ("colour", "\\d"))
        for component, pattern in component_sequence:
            for i, c in enumerate(code):
                if re.match(pattern, c):
                    codes[component] = codes[component] + c
                else:
                    code = code[i:]
                    break
        for kv in codes.items():
            setattr(self, f"{kv[0]}_code", kv[1])
        return self

    def __init__(self, code):
        super().__init__(code)
        self.decode()
