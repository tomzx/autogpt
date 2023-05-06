from autogpt.commands.container.execute import ExecuteContainer


def test_command():
    assert ExecuteContainer("container", ["command"]).command() == [
        "docker",
        "exec",
        "-it",
        "container",
        "command",
    ]
    assert ExecuteContainer("container", ["command", "with", "args"]).command() == [
        "docker",
        "exec",
        "-it",
        "container",
        "command",
        "with",
        "args",
    ]
