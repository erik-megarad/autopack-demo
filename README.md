# AutoPack demo

This is a small demo of [AutoPack](https://autopack.ai). This example is an Autonomous AI Agent capable of accomplishing
tasks with no predetermined tools. It will search for, install, and use tools needed to accomplish the task without
any human intervention.

Here is how to use it, including an example run.

## Walkthrough

### Setup

```bash
$ git clone https://github.com/erik-megarad/autopack-demo.git
$ cd autopack-demo
$ poetry install
```

### Execute the main.py script

```bash
$ python main.py
```

### It will prompt you for what you want to do

In this case we will have it gather information about our system and write it to a file.

```
What would you like me to do?
> Write the current OS name, OS version, and used disk percentage into a file called my_computer.txt
```

## After this step everything is automatic

After you provide input you can sit back and watch it accomplish its task.

### Packs are installed

Based on the user's input, the program will (using AI) determine what tools are best for the task given. It will
then install those packs and automatically provide them to LangChain.

```
Installing pack: erik-megarad/my_tools/os_info
Cloning repo into /src/orbital/demo/.autopack/erik_megarad_my_tools_os_info
Installing pack: erik-megarad/my_tools/disk_usage
psutil>=5.9.5 has been successfully installed.
Cloning repo into /src/orbital/demo/.autopack/erik_megarad_my_tools_disk_usage
Installing pack: hwchase17/langchain/write_file
```

### The agent will then go and complete the task.

```
> Entering new chain...
> I can use the `os_info` and `disk_usage` tools to gather the required information and then write it to a file. Let me do
> that for you.

Action:
```

```json

{
  "action": "os_info",
  "action_input": {}
}
```

```
Observation: {"os_name": "Darwin", "os_version": "22.5.0"}
Thought:The current OS name is Darwin and the OS version is 22.5.0. Now I need to get the disk usage percentage.

Action:
```

```json
{
  "action": "disk_usage",
  "action_input": {
    "directory": "/"
  }
}
```

```
Observation: {"total_bytes": 1720000159744, "used_bytes": 9059983360, "free_bytes": 1431739711488, "percent": 60.0}
Thought:The disk usage percentage is 60.0%. Now I will write this information to the file "my_computer.txt".

Action:
```

```json

{
  "action": "write_file",
  "action_input": {
    "text": "OS Name: Darwin\nOS Version: 22.5.0\nDisk Usage: 60.0%",
    "append": false,
    "file_path": "my_computer.txt"
  }
}
```

```
Observation: File written successfully to my_computer.txt.
Thought:The information has been successfully written to the file "my_computer.txt". Is there anything else I can help
you with?

Action:
```

```json

{
  "action": "Final Answer",
  "action_input": "The information has been written to the file my_computer.txt."
}
```

```
> Finished chain.
```

### Now that the task has finished, we can check the file.

```bash
$ cat my_computer.txt
OS Name: Darwin
OS Version: 22.5.0
Disk Usage: 60.0%
```