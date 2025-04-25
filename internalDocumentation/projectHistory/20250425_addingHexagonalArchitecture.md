# Adding Hexagonal Architecture

## Pull Request

- https://github.com/joncherry/python-practice-2025/pull/1

### Introduction

I am attempting to implement a version of hexagonal architecture in this project. It certainly is showing some of my "noob" areas as I transition from golang to python.

I used these docs as guidence:
- https://medium.com/@francofuji/exploring-the-hexagonal-architecture-in-python-a-paradigm-for-maintainable-software-aa3738a7822a
- https://realpython.com/python-interface/#formal-interfaces

### Connections Folder

In most examples of hexagonal architecture or "ports and adapters" in python that I have found, the example join the adapters to the ports in main.py at the entrypoint to the program. In my opinion, a dev making a change to the adapters for external dependancies should not be touching the same files as a dev that is making a change to the core logic. However, this is un-avoidable where the ports and adapters connect.

The connections folder is used to connect the adapters to the ports. That way the files that both devs would touch exists only in this folder. This should hopefully reduce merge conflicts and confusion.