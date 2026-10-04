import math

from src.cleaning import (
    clean_product_link,
    is_smartphone_candidate,
    normalize_brand,
    parse_naira,
    parse_rating,
    parse_review_count,
)


def test_parse_naira():
    assert parse_naira("₦ 124,143") == 124143.0


def test_parse_rating():
    assert parse_rating("4.2 out of 5") == 4.2
    assert math.isnan(parse_rating(None))


def test_parse_review_count_legacy_snapshot():
    assert parse_review_count("4.1 out of 5861") == 861.0
    assert parse_review_count("5 out of 51") == 1.0
    assert parse_review_count("4.5 out of 52") == 2.0
    assert parse_review_count("0") == 0.0


def test_normalize_brand():
    assert normalize_brand("XIAOMI Redmi 15C", "XIAOMI") == "Xiaomi"
    assert normalize_brand("itel A100", "itel") == "Itel"
    assert normalize_brand("SPARK Tecnospark 40", "SPARK") == "Tecno"


def test_invalid_login_url_removed():
    assert clean_product_link(
        "https://www.jumia.com.ng/customer/account/login/?x=1"
    ) is None


def test_scope_flag():
    assert is_smartphone_candidate("Samsung Galaxy A15 5G 128GB") is True
    assert is_smartphone_candidate("Samsung Galaxy Tab A9 8.7 Android 13") is False
    assert is_smartphone_candidate("Nothing Headphone (1) Wireless") is False
