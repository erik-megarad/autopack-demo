# AutoPack demo

This is a small demo of [AutoPack](https://autopack.ai). This example is an Autonomous AI Agent capable of accomplishing
tasks with three tools:

- Get OS info
- Get disk usage
- Write to a file

Here is how to use it, including an example run.

### Install the requirements

`poetry install`

### Install the tools used in the example

```
autopack install erik-megarad/my_tools/os_info
autopack install erik-megarad/my_tools/disk_usage
```

### Execute the main.py script

```bash
$ python main.py
```

### It will prompt you for what you want to do

In this case we want it to write OS and disk info to a file.

```
What would you like me to do?
> Write the current OS name, OS version, and used disk percentage into a file called my_computer.txt
```

### The agent will then go and complete the task.

The verbose output has been edited for clarity.

```
> Entering new  chain...
To write the current OS name, OS version, and free disk percentage into a file called my_computer.txt,
I can use the `os_info` and `disk_usage` tools. First, I will use the `os_info` tool to get the current OS name and
version. Then, I will use the `disk_usage` tool to get the free disk percentage. Finally, I will write all this
information into the file using the `write_file` tool.

Observation: {"os_name": "Darwin", "os_version": "22.5.0"}
Thought:The current OS name is Darwin and the OS version is 22.5.0. Now I need to get the free disk percentage.

Observation: {"total": 1720000159744, "used": 9597345792, "free": 1427958325248, "percent": 70.0}
Thought:The free disk percentage is 70.0%. Now I can write the OS name, OS version, and free disk percentage into the file my_computer.txt.

Observation: File written successfully to my_computer.txt.
Thought:The current OS name is Darwin, the OS version is 22.5.0, and the free disk percentage is 70.0%. I have successfully written this information into the file my_computer.txt.

> Finished chain.
```

### Now that the task has finished, we can check the file.

```bash
$ cat my_computer.txt
OS Name: Darwin
OS Version: 22.5.0
Used Disk Percentage: 70.0%
```