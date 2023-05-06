from autogpt.memory.ram import RAM


def test_ram():
    memory = RAM()
    memory.create("key", "value")
    assert memory.read("key") == "value"


def test_ram_limit():
    memory = RAM(limit=2)
    memory.create("key1", "value1")
    memory.create("key2", "value2")
    assert memory.read("key1") == "value1"
    assert memory.read("key2") == "value2"

    # This should evict key1
    memory.create("key3", "value3")
    assert memory.read("key1") is None
    assert memory.read("key2") == "value2"
    assert memory.read("key3") == "value3"

    memory.update("key2", "value2-updated")
    memory.create("key4", "value4")
    # This should evict key3
    assert memory.read("key3") is None
    assert memory.read("key2") == "value2-updated"
    assert memory.read("key4") == "value4"


def test_ram_infinite_limit():
    memory = RAM(limit=-1)
    memory.create("key1", "value1")
    memory.create("key2", "value2")
    assert memory.read("key1") == "value1"
    assert memory.read("key2") == "value2"
