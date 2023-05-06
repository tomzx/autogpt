from autogpt.tasks.base import Task


class Start(Task):
    def generate_prompt(self, query: str) -> str:
        return f"""
        {query}
        List of callable functions and their signature:
        container_execute(container: str, command: List[str])
        container_start(image: str, command: List[str], volumes: List[str])
        read_file(path: str)
        write_file(path: str, content: str)
        git_add(path: str)
        git_commit(message: str)
        git_push()
        execute_python(code: str)
        """

    def process_response(self, response: str) -> None:
        pass
