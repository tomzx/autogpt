# Getting started
* Install python 3.8+
* Install poetry
* Install docker (if using docker as a backend)
* Install kubernetes (if using kubernetes as a backend)
* Clone this repository
* `poetry install`

## Run without scheduler (local)
* Make sure you do not have an environment variable `SCHEDULER_URL` set nor in your `.env` file
* Run the CLI `python cli.py`
* You can visit the dask dashboard at http://localhost:8787/

## Run with scheduler (distributed)
* In your `.env` file, set `SCHEDULER_URL=tcp://localhost:8786`
* Start one dask scheduler and one to many workers (in the poetry environment)
  * `dask scheduler`
  * `dask-worker --nprocs 1 --nthreads 1 --memory-limit 2GB  tcp://localhost:8786`
    * Feel free to configure your dask workers as you see fit and to launch as many as you want
* Run the CLI `python cli.py`
* You can visit the dask dashboard at http://localhost:8787/

# Notion
You can store sessions and interactions in Notion for reviewing/analysis purposes. To do so, you need to set the following environment variables in your `.env` file:

```
NOTION_TOKEN
NOTION_TASK_DATABASE_ID
NOTION_SESSION_DATABASE_ID
NOTION_INTERACTION_DATABASE_ID
```

For AutoGPT to interact with your Notion workspace, go to `Settings & members`, then `Connections`, then `Develop or manage integrations`. Click on `New integration`, fill out the form and associate it with the workspace you want to use. Once the integration is created, copy the generated token as `NOTION_TOKEN`.

You then need to create 3 new pages. With the pages created, click on the 3 dots on the top right corner and select `Add connections`, the pick the integration you just created. Repeat this process for every page you want to give access.

For the task database, you need to create a database with the following properties:
* Query: the title property
* Status: Select, with the following options: `Not started`, `In progress`, `Done`
* Budget: Budget for the task
* Created: Creation date time of the task, used to process tasks in ascending order
* Updated (optional)

For the session database, you need to create a database with the following properties:
* Id: the title property
* Interactions: Relation to the interactions database
* Budget: Budget for the session
* Total cost (optional): Rollup, using th `Cost` property of the `Interactions` relation, calculate the sum
* Duration (optional): Rollup, using the `Duration` property of the `Interactions` relation, calculate the date range
* Total interactions (optional): Rollup, using the `Interactions` property of the `Interactions` relation, calculate the count
* Created (optional)
* Updated (optional)

For the interactions database, you need to create a database with the following properties:
* Prompt
* Response
* Task
* Cost
* Parent (relation to the interactions database, parent interaction)
* Children (relation to the interactions database, children interactions)
* Sessions (inverse relation to the sessions database)
* Created (optional)
* Updated (optional)
