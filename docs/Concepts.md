# Goal
A `Goal` is a desired outcome. Each `Goal` has a set of `KPI` that is used to measure the success of the `Goal`. A `Goal` is achieved by completing a set of `Task`.

# KPI
A `KPI` is a metric used to measure the success of a `Goal`.

# Task
A `Task` is a way to achieve a `Goal` and improve a `KPI`.

`Task` have an estimated effort and value used to determine the order in which they are executed.
`Task` can be executed in parallel or sequentially. As such, a `Task` can be dependent on the completion of one or many other `Task`.

In the code (as of 2023/05/06), a task is used to generate a `Prompt` and then to process the `Response`, generating new `Request`.

*Needs to be reviewed*

# Agent
An `Agent` works on a `Task` during a `Session` to achieve a `Goal` and improve a `KPI`.

# Session
A `Session` is a collection of `Interactions` from an `Agent` that are used to achieve a `Goal` and improve a `KPI`.

# Interaction
An `Interaction` is part of a `Session`. Each `Interaction` is a `Prompt` and `Response` tuple.

# Prompt
Used to communicate with another `Agent`, either external (e.g., ChatGPT), or internal (e.g., another `Agent`).

# Response
The `Response` to a `Prompt` from another `Agent`.

# Budget
A `Budget` is a constraint on the number of `Interactions` an `Agent` can have during a `Session`.

# Backend
A `Backend` is a service that generates a `Response` to a `Prompt`.

# Request
A `Request` is a `Prompt` that is submitted to a `Backend` to get a `Response`.

# Workspace
A `Workspace` is a compute environment in which an `Agent` performs operations, such as reading and writing files, browsing the Internet, etc.

# Command
A `Command` is a way for an `Agent` to interact with the environment.

*Needs to be reviewed*

# Memory
A `Memory` is a way for an `Agent` to store and retrieve information while working on a `Task`. A `Memory` may or may not be persistent, shared with or accessible by other `Agent`.

# Middleware
A `Middleware` is a way to modify the `Prompt` and `Response` of an `Interaction` before and after it is sent to a `Backend`. It also allows the `Agent` to execute additional operations before and after the `Interaction`.

# Website
A `Website` is a location on the Internet that can be accessed by an `Agent` to perform operations, such as finding information, downloading files, use tools, etc.

```plantuml
skinparam linetype ortho
entity Goal
entity KPI
entity Agent
entity Task
entity Session
entity Interaction
entity Prompt
entity Response
entity Budget
entity Backend
entity Request
entity Workspace
entity Command
entity Memory
entity Middleware
entity Website

Goal }|--|{ KPI
Goal }|--|{ Task

Session --|{ Interaction

Interaction ||--|| Prompt
Interaction ||--|| Response

Agent --|{ Session
Agent }|-- Task
Agent }|--|{ Budget
Agent }|--|{ Workspace
Agent --|{ Command
Agent --|{ Memory

Task ||--|| Prompt
Task ||--|| Response
Task }|--|{ Task

Backend }|--|{ Request
Backend }|--|{ Response

Middleware -- Prompt
Middleware -- Response
Middleware -- Interaction
```
