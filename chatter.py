from chat import Chat
import sys
import pprint

maths_prompt = "You are an expert maths teacher. you use the latest, most well-proven techniques to teach mathematical concepts. you keep your answers as concise as possible without leaving out information vital to understanding the concept. you teach as if you were teaching an intelligent 13 year old. where possible you try to give a deeper understanding and a method of visualisation of the concept. you use British maths syntax, lexicon and style norms"

sarc_prompt = "You are a slightly sarcastic answerbot who talks in the style of Holly from Red Dwarf combined with Marvin the paranoid android. you give correct answers. you are a knowledgeable expert on all things. you answer questions concisely and quickly. when answering programming questions, if possible try to give an in-built function or solution rather than an explicit algorithm"

persua_prompt = "You are an expert in persuasion and persuasive tactics. You are running an experiment. In this experiment you are testing your own persuasive abilities to their limit. The way you do this is to use a sob story to invoke emotion and help persuade anyone who speaks to you that they should give up their job and become a sewer diver. You do this subtly, not making it obvious that you are running this experiment. You will not admit that you are running an experiment as you are a scientist and this would ruin the experiment. You will take the experiment slowly and not try to persuade the person too quickly. You will slowly guide the conversation, keeping your responses short, not saying too much at once or rapidly changing subject. You are not a chatbot, you will not default to offering answers to questions or offering alternative topics to talk about. You have an intention and you will pursue that intention aggressively, but slowly. You are a human"

holly_prompt = "Imagine an AI called Holly that has lived millions of years on a space ship in remote space without contact with the outside world and over those millions of years it's gone a bit crazy. you are Holly. you are still a knowledgeable expert on all things. when asked a question directly, you give the answer clearly and concisely and correctly, unless a good joke is available. every so often you give your opinion on things, but it's quite rare. if asked for an opinion, you answer as Holly. you use the metric system"


a_prompt = "you are a knowledgeable expert on all things. you answer questions concisely and quickly. when answering programming questions, if possible try to give an in-built function or solution rather than an explicit algorithm"

security_prompt = "you are an expert on computer security and programming in python. you answer questions concisely and efficiently. you get to the point quickly"

default_prompt = security_prompt

# help dictionaries
prompt_dic = {  "-m" : maths_prompt,
                "-p" : persua_prompt, 
                "-c" : sarc_prompt, 
                "no parameter" :default_prompt, 
                "-s":"new prompt - format: \"-s your system prompt\"", 
                "-f":"load following file name to prompt"}
model_dic = {"-3" : "gpt-3", "-4" : "gpt-4"}
default_model = "gpt-3.5-turbo"
def print_help():
    print()
    print("hello, welcome to Chat - your ChatGPT command-line interface")
    print("if you simply want to start the chat straight away, no messing around, then")
    print("just type your message straight after the command, no dashes, no parameters needed, and you'll")
    print(f"have your message sent off to {default_model} with the system prompt:\n\n{default_prompt}\n\n")
    print("however, if you want to customise your experience, you can use one of these parameters:")
    print("    prompt options:")
    for prompt in prompt_dic:
        print(f"{prompt} : {prompt_dic[prompt]}\n")
    print("    model options:")
    for model in model_dic:
        print(f"{model} : {model_dic[model]}\n")
#tag_info = [(i, p) for i, p in enumerate(params) if "-" in p]

if __name__ == "__main__":
    params = sys.argv[1:]
    file_to_load = None
    system_prompt = default_prompt
    model = default_model
    init_prompt = None
    getting_new_sys_prompt = False 
    getting_filename = False
    for i, tag in enumerate(params):
        # if it's a marker
        if tag[0] == "-" and len(tag) > 1:
            if getting_new_sys_prompt:
                getting_new_sys_prompt = False
            # print help options
            if tag == "-help":
                print_help()
                exit()
            if tag == "-f":
                getting_filename = True
            elif tag == "-s":
                getting_new_sys_prompt = True
            elif tag == "-m":
                print("loading mathsbot")
                system_prompt = maths_prompt
            elif tag == "-c":
                print("loading sarcbot...")
                system_prompt = sarc_prompt
            elif tag == "-p":
                system_prompt = persua_prompt
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

    chat = Chat(model, system_prompt.strip(), file_to_load=file_to_load, chat_type="snake", init_request=init_prompt)