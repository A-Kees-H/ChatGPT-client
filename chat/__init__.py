import os, sys
import openai
import datetime
import json
from pprint import *


def get_datetime_formatted():
    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%y-%m-%d_%H-%M")


def get_message(speech):
    return {"role": "user", "content": speech}

class Chat:
    def __init__(s, model, system_prompt, file_to_load=None, chat_type="ladder"):
        models = {
        "davinci":"text-davinci-003",
        "gpt-3":"gpt-3.5-turbo",
        "katherine":"davinci:ft-personal:katherine-2023-03-01-20-30-05",
        "gpt-4":"gpt-4"}
        akb_key = "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"
        reg_key = "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"
        openai.api_key = akb_key

        s.file_to_load = file_to_load
        s.system_prompt = system_prompt
        s.model_name = model
        s.model = models[model]
        s.save = True
        s.title = ""

        s.messages = s.load_chat()

        # a loaded chat will already have a system prompt
        if not s.messages:
            sys_message = {"role": "system", "content": system_prompt}
            s.messages.append(sys_message)
        else:
            print(f"loaded {file_to_load}")

        s.num_prompts = len(s.messages) - 1
        if chat_type == "snake":
            s.chat()

    def chat(s):
        while 1:
            try:
                speech = input("you: ")
                if speech == "~print~": 
                    pprint(s.messages)
                    speech = input("you: ")
                response = s.respond(speech)
                s.print_tabbed(response.content)
                s.num_prompts += 1
                if s.num_prompts == 2:
                    s.save_chat()
                elif s.num_prompts > 2 and s.save:
                    s.save_chat()
                print()
            except KeyboardInterrupt:
                print("\nChat Ended\n")
                if s.num_prompts:
                    s.save_chat()
                break

    def print_tabbed(s, content):
        lines = content.split("\n")
        tabbed_lines = ["    " + line for line in lines]
        tabbed_content = "\n".join(tabbed_lines)
        print("\n" + tabbed_content)

    def generate_title(s):
        messages = s.messages[:]
        pretitle = s.eph_respond("write a 5 word title for the preceding chat")["content"].strip().replace(" ", "_")
        title = ""
        for c in pretitle:
            if c.lower() in "0987654321qwertyuiopasdfghjklzxcvbnm,-_~":
                title += c
        s.title = title + ".json"

    def respond(s, speech):
        s.messages.append(get_message(speech))
        response = openai.ChatCompletion.create(model=s.model, messages=s.messages, n=1, temperature=0.7).choices[0].message
        s.messages.append(response)
        return response
    
    def eph_respond(s, speech):
        messages = s.messages[:]
        messages.append(get_message(speech))
        #pprint(messages)
        response = openai.ChatCompletion.create(model=s.model, messages=messages, n=1, temperature=0.7).choices[0].message
        return response

    def save_chat(s):
        if not os.path.exists("saved_chats"):
            try:   
                os.mkdir("saved_chats")
                s.save = True
            except:
                print("unable to make saved_chats folder, continuing without autosave")
                s.save = False
                return
        if not s.title:
            s.generate_title()
            while s.title in os.listdir("saved_chats"):
                s.generate_title()
            #while input(f"are you happy with the title '{title}'? (*/n): ") == "n":
            #    s.title = generate_title(s.messages)
            print(f"\n...saved to {s.title}...")
        json.dump(s.messages, open(f"saved_chats/{s.title}", "w"))
        

    def load_chat(s):
        if not s.file_to_load:
            return []
        file_to_load = "saved_chats/" + s.file_to_load
        try:
            return json.load(open(file_to_load))
        except FileNotFoundError:
            try:
                return json.load(open(file_to_load + ".json"))
            except FileNotFoundError:
                print("file not found, starting a fresh chat")
                return []




    #raise(Exception("wrong number of parameters"))
        
