# Import necessary libraries
from chat import Chat
import importlib.util
import codecs
import re
from wallet_check import check_bal


# Function to extract python code from response
def get_python_code(response):
    pattern = r"```python\n(.*?)\n```"
    match = re.search(pattern, response, re.DOTALL)
    if match:
        python_code = match.group(1)
        print(python_code)
        return python_code
    else:
        return response


# Function to extract HTML code from response
def get_html_code(response):
    pattern = r"```html\n(.*?)\n```"
    match = re.search(pattern, response, re.DOTALL)
    if match:
        html_code = match.group(1)
        print(html_code)
        return html_code
    else:
        return response


# Function to write python code to a file
def write_python_code(python_code):
    with codecs.open("runfile.py", 'w', encoding='utf-8', errors='ignore') as runfile:
        print("\nwriting python\n")
        runfile.write(python_code)


# Function to write HTML code to a file
def write_html_code(html_code):
    with codecs.open("index.html", 'w', encoding='utf-8', errors='ignore') as runfile:
        print("\nwriting html\n")
        runfile.write(html_code)


# Function to run python code from a file
def run_python_code():
    print("\nrunning code\n")
    spec = importlib.util.spec_from_file_location("runfile", "runfile.py")
    my_code = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(my_code)


# Main loop to interact with the chat API
code_gen = Chat("gpt-4", "you are a code-writing bot that writes inline-commented code. you write the full code for the task given to you. you do not break up the code into separate sections. you write the code for python 3.9", chat_type="ladder")

command = "write a program that prints the balance in this bitcoin wallet to 5 decimal places: bc1qr6mvdu7wwlnftk98h5t3flgu9mlwu370q967x0"

while True:
    command = "rewrite this program using best coding practices and inline comments: " + open("use_chat.py").read()
    print("sending command")
    response = code_gen.respond(command).content
    print(response)

    python_code = get_python_code(response)
    if "```html" in response:
        html_code = get_html_code(response)
        write_html_code(html_code)

    write_python_code(python_code)
    try:
        run_python_code()
    except Exception as e:
        print(e)
    command = input(": ")
    if "{e}" in command:
        command.replace("{e}", str(e))