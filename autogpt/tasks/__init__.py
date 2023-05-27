from autogpt.tasks.code.generate_poetry_command import GeneratePoetryCommand
from autogpt.tasks.code.generate_python import GeneratePython
from autogpt.tasks.code.generate_tests import GenerateTests
from autogpt.tasks.code.programmer import Programmer
from autogpt.tasks.code.review_codebase import ReviewCodebase
from autogpt.tasks.code.summarize_code_changes import SummarizeCodeChanges
from autogpt.tasks.recall import Recall
from autogpt.tasks.remember import Remember
from autogpt.tasks.simple import Simple
from autogpt.tasks.task.identify_similar_tasks import IdentifySimilarTasks
from autogpt.tasks.task.review_tasks import ReviewTasks
from autogpt.tasks.text.query_multiple_personas import QueryMultiplePersonas
from autogpt.tasks.text.summarize import Summarize
from autogpt.tasks.text.summarize_multiple_personas import SummarizeMultiplePersonas
from autogpt.tasks.text.summarize_responses import SummarizeResponses

all_tasks = [
    # Code
    GeneratePoetryCommand,
    GeneratePython,
    GenerateTests,
    Programmer,
    ReviewCodebase,
    SummarizeCodeChanges,
    # Task
    IdentifySimilarTasks,
    ReviewTasks,
    # Text
    QueryMultiplePersonas,
    Summarize,
    SummarizeMultiplePersonas,
    SummarizeResponses,
    # Base
    Recall,
    Remember,
    Simple,
]
all_tasks = {task.name: task for task in all_tasks}

all_tasks_names = [task for task in all_tasks.keys()]
