from autogpt.commands.container.start import StartContainer


def test_command():
    assert StartContainer("image", ["command"], []).command() == [
        "docker",
        "run",
        "-it",
        "image",
        "command",
    ]
    assert StartContainer("image", ["command", "with", "args"], []).command() == [
        "docker",
        "run",
        "-it",
        "image",
        "command",
        "with",
        "args",
    ]
    assert StartContainer("image", ["command"], ["host:client"]).command() == [
        "docker",
        "run",
        "-it",
        "-v host:client",
        "image",
        "command",
    ]
