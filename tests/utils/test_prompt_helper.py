from autogpt.utils.prompt_helper import return_json, return_yaml


def test_return_json():
    assert (
        return_json({"item": 3, "subitem": {"item": 3}})
        == 'Return your response in JSON format. Use the following format for your output:\n{"item": 3, "subitem": {"item": 3}}'
    )
    assert return_json() == "Return your response in JSON format."


def test_return_yaml():
    assert (
        return_yaml({"item": 3, "subitem": {"item": 3}})
        == "Return your response in YAML format. Use the following format for your output:\nitem: 3\nsubitem:\n  item: 3"
    )
    assert (
        return_yaml({"item": 3, "subitem": {"item": 3}}, True)
        == "Return your response in YAML format. Use the following format for your output:\n{item: 3, subitem: {item: 3}}"
    )
    assert return_yaml() == "Return your response in YAML format."
