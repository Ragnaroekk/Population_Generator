from tkinter import*
import requests
from bs4 import BeautifulSoup
import pandas as pd
import socket
import os
from multiprocessing import Process


def keywords_transform(string):
    # transform the string to the format 'Mathematics'
    string = string.lower()
    return string[0].upper() + string[1:]

def generate_content(primary_key,secondary_key):
    url = 'https://en.wikipedia.org/wiki/'+keywords_transform(primary_key)
    resp = requests.get(url=url, headers={'User-Agent': 'Custom'})
    if '404' in str(resp):
        return 'Page not found'
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    text=soup.get_text()
    text=text.split('\n')
    text=[i for i in text if i!='' and len(i.split(' '))>15 and '\\' not in i and '[' not in i]

    text=[i for i in text if (keywords_transform(primary_key) in i or primary_key.lower() in i) and (keywords_transform(secondary_key) in i or secondary_key.lower() in i)]

    if len(text)>0:
        return text[0]
    else:
        return 'Content not found.'

def GUI():



    def content_by_keywords():
        try:
            t.delete(1.0, END)
        except Exception as e:
            print(e)
        primary_keyword=entry1.get()
        secondary_keyword=entry2.get()

        if len(primary_keyword)>0 and len(secondary_keyword)>0:
            content=generate_content(primary_keyword,secondary_keyword)
            t.insert('end',content)
            t.grid(row=4,column=1)
            entry1.delete(0,END)
            entry2.delete(0,END)
        else:
            t.insert('end','Either primary_keyword or secondary_keyword is not entered.')
            t.grid(row=4,column=1)

    def content_by_csvfile():
        try:
            t.delete(1.0, END)
        except Exception as e:
            print(e)

        file_name=entry3.get()
        if file_name is None or len(file_name)==0:
            file_name='input.csv'

        try:
            df=pd.read_csv(file_name)
            #assume that the format of keywords is right.
            keywords=df['input_keywords'].iloc[0]
            primary_keywords=keywords.split(';')[0]
            secondary_keywords = keywords.split(';')[1]
            content=generate_content(primary_keywords,secondary_keywords)
            t.insert('end', content)
            t.grid(row=4,column=1)

            df_temp=pd.DataFrame(index=[0],columns=['input_keywords','output_content'])
            df_temp.iloc[0,0]=keywords
            df_temp.iloc[0,1]=content
            df_temp.to_csv('output.csv')
        except:
            t.insert('end', file_name+' is not in the current directory.')
            t.grid(row=4,column=1)

    def data_socket_client():
        '''

        :param message: message is a string
        :return:
        '''
        state=entry4.get()
        year=entry5.get()
        t1.grid(row=5, column=1)
        if len(state)>0 and len(year)>0:
            try:
                t1.delete(1.0, END)
                client = socket.socket()
                client.connect(("localhost", 9999))
                message=state+','+year
                t1.insert('end', 'Content Generator is requesting data...\n\n')
                client.send(message.encode())
                data = client.recv(1024)  # data is a binary string
                data=data.decode()
                t1.insert('end','The population size of ' +state+ ' in '+year+' is '+data+'.\n')
            except Exception as e:
                t1.insert('end',str(e)+'\n')
        else:
            t1.insert('end','Either state or year is not entered.')





    #initialize Tk()
    myWindow = Tk()
    #title
    myWindow.title('Content Generator Microservice')
    #labels
    Label(myWindow, text="The primary keyword:").grid(row=0,column=0)
    Label(myWindow, text="The secondary keyword:").grid(row=1,column=0)
    Label(myWindow, text="CSV file name:").grid(row=2,column=0)

    #Entry
    entry1=Entry(myWindow)
    entry2=Entry(myWindow)
    entry3=Entry(myWindow)

    entry1.grid(row=0, column=1)
    entry2.grid(row=1, column=1)
    entry3.grid(row=2,column=1)

    Label(myWindow, text="State:").grid(row=0,column=2)
    Label(myWindow, text="Year:").grid(row=1,column=2)
    entry4=Entry(myWindow)
    entry5=Entry(myWindow)
    entry4.grid(row=0, column=3)
    entry5.grid(row=1,column=3)

    #buttons
    Button(myWindow, text='Generate content by the primary and secondary keyword', command=content_by_keywords).grid(row=3, column=0, sticky=W, padx=5, pady=5)
    Button(myWindow, text='Generate content by a csv file', command=content_by_csvfile).grid(row=3, column=1, sticky=W, padx=5, pady=5)
    Button(myWindow, text='Request data from Population Generator',command=data_socket_client).grid(row=3,column=2,sticky=W, padx=5, pady=5)
    Button(myWindow, text='Quit', command=myWindow.quit).grid(row=3, column=3,sticky=W, padx=5, pady=5)

    #output textbox
    Label(myWindow, text="Generated content:").grid(row=4)

    t=Text(myWindow, height=5)

    Label(myWindow, text="Socket information:").grid(row=5)

    t1=Text(myWindow, height=5)
    #loop
    myWindow.mainloop()




def data_socket_server():
    '''
    :return:
    '''

    server = socket.socket()
    server.bind(("localhost", 8000))  # bind ip port
    server.listen()
    while True:
        conn, addr = server.accept()
        print("New Connection:", addr)

        data = conn.recv(1024)
        data = data.decode()
        print("Message received:", data)
        content=generate_content(data.split(',')[0],data.split(',')[1])
        conn.send(content.encode())

if __name__=="__main__":

    print('The program is starting...')
    p1=Process(target=GUI)
    p2=Process(target=data_socket_server)
    p1.start()
    p2.start()
    p1.join()
