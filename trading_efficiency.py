import json
from tkinter import *
from pymongo import MongoClient
import pymongo

class trading_efficiency:

    def __init__(self):
        self.data=[]
        self.percentual_balance=0

        window =Tk()

        random_trade_title=Label(window,text='Random trade:')
        random_trade_title.grid(row=0,columnspan=2)

        gain_label=Label(window,text='Percentage gain:')
        gain_label.grid(row=1,column=0)

        self.gain_input=Entry(window)
        self.gain_input.delete(0, END)
        self.gain_input.insert(0, "0.04")
        self.gain_input.grid(row=1,column=1)

        loss_label=Label(window,text='Percentage loss:')
        loss_label.grid(row=2,column=0)

        self.loss_input=Entry(window)
        self.loss_input.grid(row=2,column=1)
        self.loss_input.delete(0, END)
        self.loss_input.insert(0, "0.04")

        random_trade_button=Button(window,text='random trade',command=self.test_trade)
        random_trade_button.grid(row=3,columnspan=2)
        self.result_text=Label(window,text='result:')
        self.result_text.grid(row=4,columnspan=2)

        window.mainloop()

    def get_data_from_database(self):
        client=MongoClient()
        database=client.get_database('database')
        collection=database.get_collection('collection')
        ordered_data=[]
        for data in collection.find().sort('_id',pymongo.ASCENDING):
            self.data.append(data)

    #test trading and returns balance
    def test_trade(self):
        self.data=[]
        self.get_data_from_database()
        self.convert_data()
        for index in range(len(self.data)):
            self.trade(index)
        self.result_text['text']='result: '+str(self.percentual_balance)

    #imports configurations from json file
    # file=open('configuration.json','r')
    # json_file=json.load(file)
    # return_percentage=json_file['trading_efficiency']
    # return_percentage=return_percentage['return_percentage']

    #convert dict in close value
    def convert_data(self):
        cleaned_data=[]
        for data in self.data:
            value=data['value']
            value=value['close']
            cleaned_data.append(float(value))
        self.data=cleaned_data

    #trade the a determined value in a determined time(index)
    def trade(self,index):
                  
        gain_percentage=float(self.gain_input.get())/100
        loss_percentage=float(self.loss_input.get())/100


        gain_price=self.data[index]+self.data[index]*gain_percentage
        loss_price=self.data[index]-self.data[index]*loss_percentage


        #check future prices
        for points in range(index,len(self.data)):
            #checks if current price is bigger or equal selling price
            if self.data[points]>gain_price:
                self.percentual_balance+=gain_percentage

            #checks if current price is bigger or equal buying price
            elif self.data[points]<loss_price:
                self.percentual_balance-=loss_percentage

            #nor loss nor gain
            else:
                pass