**Safe-Code-Executor**

This project is an API that runs Python code safely inside Docker containers. It allows users to send Python code, executes it in isolation, and returns the output. The goal is to run untrusted code without risking your system.

The goal of this project is to learn:

- How to run code inside Docker  
- How to safely execute untrusted code  
- How to apply security limits (timeout, memory, no network)  
- What Docker can and cannot protect  
- How to document and test a real API

- **What You Built**

A single-endpoint API that:

- Accepts Python code from the user  
- Writes it to a temporary file  
- Executes it inside a **Docker python:3.11-slim container**  
- Returns the output safely

- Example:

**User sends:**

```json
{ "code": "print('Hello World')" }
```

**API returns:**

```json
{ "output": "Hello World\n" }
```

<img width="415" height="96" alt="image" src="https://github.com/user-attachments/assets/b053cf1d-c37b-4ead-8cbb-9052a68a67ac" />

**Implementation Steps**
- Create a Flask API
- 
- Write incoming code to a temporary file
- 
- Run it using Docker:
- 
  ```
  docker run python:3.11-slim python script.py
  ```
- Capture output and return it

**Basic Functionality Goal**
Create an API with one endpoint:
Request:
POST /run { "code": "print(4 + 4)" }
Response:
{ "output": "8\n" }
- **
- 
- <img width="415" height="116" alt="image" src="https://github.com/user-attachments/assets/f90df7d5-691e-49ac-8c11-9deeba234511" />


**How it works**
The API receives Python code from the user.
The code is saved to a temporary file.
A Docker container runs the code using Python.
The API returns whatever the program prints.
Basic Docker command docker run --rm -v /path/to/tmp:/app python:3.11-slim python /app/script.py

**Test examples:**
print("Hello")
x = 5 + 3; print(x)
for i in range(5): print(i)

<img width="415" height="111" alt="image" src="https://github.com/user-attachments/assets/e910a7dd-e327-4fb5-a8cc-bc1554c36edf" />

**Add Basic Safety Goal**
Running user code can be dangerous. So we added protections against:
Example of bad code:

Infinite loops
while True: pass
This should stop after 10 seconds. Use timeout=10 in the Python subprocess

<img width="416" height="112" alt="image" src="https://github.com/user-attachments/assets/8259369a-9fda-4543-af55-7bf6b919658c" />

Memory bombs:
Example:

```python
x = "a" * 1000000000
```

✔ Stopped safely due to Docker’s memory limit (`--memory=128m`)

---
<img width="416" height="114" alt="image" src="https://github.com/user-attachments/assets/6396a902-51a1-4e0a-af64-20ed4a8b2a47" />
 but the statues is 
 <img width="415" height="119" alt="image" src="https://github.com/user-attachments/assets/1b9b3daf-35a2-4627-ab89-fe34793d80cc" />

 Docker security flags used:

--timeout 10

--memory="128m"

--network none

These prevent system crashes and malicious behavior.

-network none --memory="128m" --cpus="0.5" --pids-limit=100 --read-only --tmpfs /tmp --security-opt no-new-privileges

What each flag protects:

Problem Solution Infinite loops Subprocess timeout High memory usage --memory="128m" High CPU usage --cpus="0.5" Fork bombs --pids-limit=100 Network attacks --network none Writing files --read-only Privilege escalation --security-opt no-new-privileges 4. Docker Security Experiments

These experiments help you understand what Docker protects and what it does not.

Experiment 1 — ** Reading system files**
Code:
```python
with open("/etc/passwd") as f:
    print(f.read())
```

 Works  
But it shows container’s `/etc/passwd`  
NOT the host → Safe.

Experiment 2: Writing files with open("/tmp/test.txt", "w") as f: f.write("hacked!")

This will work because containers have a writable filesystem. It does not write to your host machine.

Experiment 3: Read-only mode

If you run Docker with:
--read-only --tmpfs /tmp
Writing files will fail with an error:
Read-only file system

This confirms the protection works.

**A basic HTML page with:**

Text area for code

Submit button

Display for output

example

<img width="947" height="492" alt="image" src="https://github.com/user-attachments/assets/6402c204-e413-44a7-8f72-532c45367fc4" />


**Final Secure Docker Command**

This is the final recommended command to run the code safely:

docker run --rm
--network none
--memory="128m"
--cpus="0.5"
--pids-limit=100
--read-only
--tmpfs /tmp
-v /your/tmpdir:/app
python:3.11-slim python /app/script.py

**What You Learn**

This project is a Secure Python Code Executor that allows users to safely run Python code inside a Docker container through a Flask API. The system isolates untrusted code by applying strict security measures such as execution timeouts, memory limits, CPU limits, no network access, and a read-only filesystem. I built a simple web interface to send code to the API and display the output. Through this project, I learned how to run code securely using Docker, how to design and test APIs, how to prevent common security risks like infinite loops, memory attacks, and file modifications, and how to create clear documentation and a functional user interface. Overall, the project helped me understand both backend and container-based security concepts while building a practical real-world application.

**Summary**
You built an API that runs Python code safely by executing it inside a Docker container. You added protection such as timeouts, memory limits, no network access, and a read-only filesystem so the code cannot harm your system. The result is a secure sandbox where untrusted Python code can run safely.

