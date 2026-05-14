from elevenlabs.conversational_ai.conversation import ClientTools
from langchain_community.tools import DuckDuckGoSearchRun

def searchweb(parameters):
    query = parameters.get("query")
    results = DuckDuckGoSearchRun(query = query)
    return results

def save_to_txt(parameters):
    filename = parameters.get("filename")
    data = parameters.get("data")
    

    formatted_data = f"{data}"

    with open(filename, "a", encoding="utf-8") as file:
        file.write(formatted_data + "\n")


client_tools = ClientTools()
client_tools.register("searchweb", searchweb)
client_tools.register("savetotxt", save_to_txt)
