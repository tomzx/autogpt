from autogpt.utils.lists import contains_list, count_list_items, extract_list


def test_contains_list():
    assert contains_list("- item 1\n- item 2")
    assert contains_list("* item 1\n* item 2")
    assert contains_list("1. item 1\n2. item 2")
    assert not contains_list("item 1\nitem 2")
    assert contains_list("item 1\n- item 2")
    assert contains_list("*item 1\n item 2")
    assert contains_list("item 1\n1. item 2")


def test_count_list_items():
    assert count_list_items("- item 1\n- item 2") == 2
    assert count_list_items("* item 1\n* item 2") == 2
    assert count_list_items("1. item 1\n2. item 2") == 2
    assert count_list_items("item 1\nitem 2") == 0
    assert count_list_items("item 1\n- item 2") == 1
    assert count_list_items("*item 1\n item 2") == 1
    assert count_list_items("item 1\n1. item 2") == 1


def test_extract_list():
    assert extract_list("- item 1\n- item 2") == ["item 1", "item 2"]
    assert extract_list("* item 1\n* item 2") == ["item 1", "item 2"]
    assert extract_list("1. item 1\n2. item 2") == ["item 1", "item 2"]
    assert extract_list("item 1\nitem 2") == []
    assert extract_list("item 1\n- item 2") == ["item 2"]
    assert extract_list("*item 1\n item 2") == ["item 1"]
    assert extract_list("item 1\n1. item 2") == ["item 2"]
