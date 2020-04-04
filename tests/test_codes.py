import pytest

from owenscrape.codes import (
    NewCode,
    find_collection,
    COLLECTIONS,
    LINES,
    ParseCodeFailedException,
)


@pytest.fixture()
def new_code():
    return "RP20S1704LLP54"


def test_find_collection():
    larry = find_collection("19", "F")
    assert larry != None
    assert larry.year == "19"
    assert larry.season == "FW"
    assert larry.name == "LARRY"

    with pytest.raises(ValueError):
        find_collection("00", "S")

    with pytest.raises(ParseCodeFailedException):
        find_collection("19", "AS")


def test_parse_new_code(new_code):
    code = NewCode(new_code)
    assert code.collection == find_collection("20", "S")
    assert code.fabric_code == "LLP"
    assert code.colour_code == "54"
    assert code.line == "Precollection"
    assert code.gender == "Women"

    # Test a bunch of random Tec codes
    for c in [
        "RP20S1704LLP 54",
        "RP20S1704LSN 09",
        "RR20S7424LTY 2208",
        "RA19F0493GDSTB-3409",
    ]:
        NewCode(c)


def test_parse_champ_code():
    champ_codes = {
        "cw20s0004113688-09": ("0004", "113688", "09"),
        "cw20s0009113654-08": ("0009", "113654", "08"),
        "cm20s0001215084-09": ("0001", "215084", "09"),
    }
    for code, components in champ_codes.items():
        parsed = NewCode(code)
        parsed_components = (parsed.item_code, parsed.fabric_code, parsed.colour_code)
        assert parsed_components == components
