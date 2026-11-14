#!/usr/bin/env python3
"""
Weekend promotions — which poster goes out on which day.

Two promotions every weekend, one on Saturday and one on Sunday, so each of the
four posters comes round once a fortnight:

    Weekend A   Saturday: Study Notes     Sunday: Mock Tests
    Weekend B   Saturday: Monthly Quest   Sunday: Virtual Labs

The day decides the promo (no saved counter), so a missed or repeated run can
never push the rotation out of step.

    python3 promo_config.py            -> today's promo mode (blank on weekdays)
    python3 promo_config.py --plan 8   -> the next 8 promo days
"""
import sys
from datetime import date, datetime, timedelta, timezone

PORTAL_URL = "https://cbsemock.org.in"
POSTERS = {
    "promo_notes": "01_study_notes.jpg",
    "promo_mock":  "02_mock_tests.jpg",
    "promo_quest": "03_monthly_quest.jpg",
    "promo_lab":   "04_virtual_labs.jpg",
}
NAMES = {"promo_notes": "Study Notes", "promo_mock": "Mock Tests",
         "promo_quest": "Monthly Quest", "promo_lab": "Virtual Labs"}
ROTATION = [["promo_notes", "promo_mock"], ["promo_quest", "promo_lab"]]   # [weekend][Sat, Sun]
ANCHOR_SATURDAY = date(2026, 11, 14)                                       # a "Weekend A" Saturday


def poster_url(mode: str) -> str:
    return f"{PORTAL_URL}/promo-posters/{POSTERS[mode]}"


def today_ist() -> date:
    return (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date()


def promo_for(day: date) -> str:
    """Promo mode for a date; '' on weekdays."""
    wd = day.weekday()
    if wd not in (5, 6):
        return ""
    saturday = day - timedelta(days=wd - 5)
    weekend = ((saturday - ANCHOR_SATURDAY).days // 7) % 2
    return ROTATION[weekend][wd - 5]


def month_name() -> str:
    return today_ist().strftime("%B")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--plan":
        d, left = today_ist(), int(sys.argv[2])
        while left:
            m = promo_for(d)
            if m:
                print(f"{d:%a %d %b %Y}  {NAMES[m]}")
                left -= 1
            d += timedelta(days=1)
    else:
        print(promo_for(today_ist()))
