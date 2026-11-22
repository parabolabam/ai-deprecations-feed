import pytest

from depfeed.dates import parse_date


@pytest.mark.parametrize("s,want", [
    ("**Dec 11, 2026**", "2026-12-11"),
    ("Not sooner than November 9, 2027", "2027-11-09"),
    ("2027-04-14^3^", "2027-04-14"),
    ("09/21/26", "2026-09-21"),
    ("Sept 7, 2026", "2026-09-07"),
    ("October 13, 2027 or later", "2027-10-13"),
    ("TBD", None),
    ("", None),
])
def test_parse_date(s, want):
    assert parse_date(s) == want
