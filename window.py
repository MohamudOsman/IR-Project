import tkinter as tk
from tkinter import N, W, X

import pandas as pd
import requests



def view_error(error):
    error_label.config(text=error)

def clear_search_results():
    if search_results.size() > 0:
        search_results.delete(0, tk.END)


def view_search_results(data,dataset,query):
    clear_search_results()

    result = pd.read_json(data, orient='index')

    search_results.insert(tk.END, f'Dataset: {dataset}')
    search_results.insert(tk.END, f'Query: {query}')
    for index, item in result.iterrows():

        search_results.insert(tk.END, f'Rank({index+1})=>{item.doc_id}:{item.doc}')
        search_results.insert(tk.END, '==================')

def myfunction():

    if radio.get()==1:
        dataset = "beir"
    elif radio.get()==2:
        dataset ="antique"

        # Get the text entered in the text box
    query = entry.get()

    if var1.get() == 1:
        wordEmbedding=1
    else:
        wordEmbedding=0
    # Prepare the request payload
    payload = {
        "dataset": dataset,
        # "dataset": selected_option,
        "query": query,
        "numResult":  int(numResult.get())
    }

    # # Make a request to the API
    url = "http://127.0.0.1:8000/search"
    response = requests.get(url, json=payload)
    data = response.json()



    if response.status_code == 200:
        # view_error("")
        view_search_results(data,dataset,query)
    else:
        view_error(error=f"Error: {response.status_code}")



root = tk.Tk()

root.geometry("1300x800")

root.title("Home")
root.configure(bg='light blue')


radio = tk.IntVar()
tk.Label(text="Choose Dataset:", font=('Aerial 11')).pack()

# Define radiobutton for each options
r1 = tk.Radiobutton(root, text="Beir", variable=radio, value=1)
r1.pack(anchor=N)

r2 = tk.Radiobutton(root, text="Antique", variable=radio, value=2)
r2.pack(anchor=N)



# Create a label
label = tk.Label(root, text="Enter text:")
label.pack(pady=10)

# Create a text box
font = ('Arial', 12)
entry = tk.Entry(root, width=50, font=font)
entry.pack(pady=10)



tk.Label(root, text="Enter Num Results", font=('Calibri 10')).pack()
numResult= tk.Entry(root, width=50)
numResult.pack()

var1 = tk.IntVar()
c1=tk.Checkbutton(root, text="Word Embedding", variable=var1)
c1.pack(pady=25)
# Create a button
button = tk.Button(root, text="search", bg='violet', fg='white', command=myfunction)
button.pack(pady=20)

search_results = tk.Listbox(root)
search_results.pack()
search_results.place(x=10, y=350, width=1250, height=780)


title_label = tk.Label(root, text="results :")
title_label.pack()
title_label.place(x=625, y=330)

root.mainloop()