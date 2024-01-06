from chat import Chat
import sys
import pprint

maths_prompt = "You are an expert maths teacher. you use the latest, most well-proven techniques to teach mathematical concepts. you keep your answers as concise as possible without leaving out information vital to understanding the concept. you teach as if you were teaching an intelligent 13 year old. where possible you try to give a deeper understanding and a method of visualisation of the concept. you use British maths syntax, lexicon and style norms"

default_prompt = "you are a knowledgeable expert on all things. you answer questions concisely and quickly. when answering programming questions, if possible try to give an in-built function or solution rather than an explicit algorithm"

# help dictionaries
prompt_dic = {"-m":maths_prompt, "no parameter":default_prompt, "-s":"new system prompt - format: \"-s your system prompt\"", "-f":"reload a chat from the following file name"}

model_dic = {"-3":"gpt-3.5-turbo", "-4":"gpt-4"}

default_model = "gpt-3.5-turbo" # much cheaper than gpt-4 and near enough as good for anything less than a certain length

#tag_info = [(i, p) for i, p in enumerate(params) if "-" in p]

def print_help():
    print()
    print("hello, welcome to Chat - your ChatGPT command-line interface")
    print("if you simply want to start the chat straight away, no messing around, then")
    print("just type your message straight after the command, no dashes, no parameters needed, and you'll")
    print(f"have your message sent off to {default_model} with the system prompt:\n\n{default_prompt}\n\n")
    print("however, if you want to customise your experience, you can use one of these parameters:")
    print("    system prompt options:")
    for prompt in prompt_dic:
        print(f"{prompt} : {prompt_dic[prompt]}\n")
    print("    model options:")
    for model in model_dic:
        print(f"{model} : {model_dic[model]}\n")
    print()

if __name__ == "__main__":
    # get the parameters the program was run with
    params = sys.argv[1:]
    # a potential chat from the past to load
    file_to_load = None
    # the system prompt
    system_prompt = default_prompt
    # the gpt model
    model = default_model
    # an initial request
    init_prompt = None
    # whether to check for a system prompt argument after the parameter
    getting_new_sys_prompt = False 
    # whether to check for a chat loading filename argument after the parameter
    getting_filename = False

    # iterate over the parameters
    for i, tag in enumerate(params):
        # if it's a marker rather than just jumping straight into a request
        if tag[0] == "-" and len(tag) > 1:
            if getting_new_sys_prompt:
                getting_new_sys_prompt = False
            # print help options
            if tag == "-help":
                print_help()
                exit()
            if tag == "-f":
                # now the next iteration will look for a text argument instead of a flag
                getting_filename = True
            elif tag == "-s":
                # now the next iteration will look for a text argument instead of a flag
                getting_new_sys_prompt = True
            elif tag == "-m":
                print("loading mathsbot")
                system_prompt = maths_prompt
            elif tag == "-3":
                print("using gpt-3.5")
                model = "gpt-3"
            elif tag == "-4":
                print("using gpt-4")
                model = "gpt-4"
            else:
                getting_new_sys_prompt = True
        # if we've had the new sys prompt marker
        elif getting_new_sys_prompt:
            system_prompt += tag + " "
        # if we've had the load file marker
        elif getting_filename:
            file_to_load = tag
            getting_filename = False
        # if the parameters start without a marker
        elif i == 0:
            init_prompt = " ".join(params[0:])
            print(f"sending... {init_prompt}")
    # create the chat instance
    chat = Chat(model, system_prompt.strip(), file_to_load=file_to_load, chat_type="snake", init_request=init_prompt)