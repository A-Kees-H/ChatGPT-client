import os, sys
import openai
import datetime

#openai api fine_tunes.create -t "C:/My Files/Work/Projects/machine learning/GumPTion-3/katherine_prepared.jsonl" -m "text-davinci-003" --suffix "Katherine"
reg_key = "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"
openai.api_key = reg_key
#print(openai.File.create(
#  file=open("katherine_prepared.jsonl", "rb"),
#  purpose='fine-tune'))
input(openai.FineTune.list())
print(openai.FineTune.create(training_file="file-JxPBLs5QBxXFrmf6GoBiT0y8", model="davinci", suffix="Katherine"))