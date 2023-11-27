import tkinter as tk
from time import *
import yfinance as yf
from yahoo_fin import stock_info
import os
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib import pyplot as plt
import datetime as dt
from UliPlot.XLSX import auto_adjust_xlsx_column_width

########################      variables
name=''
budget=100000
amount=0
stocks={}# ={stock1:[shares1,net cost],stock2:[shares2,net cost]}  stocks bought
trades=0
#extra=0.0# for profit or loss incurred when i share is bought and later sold

colour1="#4f7eee"
colour2="#ffffff"
colour3="#3f414b"
colour4="#4da6ff"
col="#53ff1a"
#warning = 

"""
#ffffff:white
#b3edff:light blue
#4da6ff:semi light blue
#bdc1c1:light grey
#657be6:purple blue
#4f7eee:sea blue
#666666: dark grey
#3f414b: better grey
<name> is the username
"""
########################      functions  
def remove_grid(widget):
    widget.grid_forget()

def remove_place(widget):
    widget.destroy()

def change_on_hover(b,c1,c2):
    #c1 is original colour
    #c2 is hovering colour
    b.bind("<Enter>", func=lambda e: b.config(background=c2))
    b.bind("<Leave>", func=lambda e: b.config(background=c1))

def getname():
    global username,name,wlcm1
    name=username.get()
    if name.strip()=='':
        pass
    else:
        remove_place(frame_username)
        home()

def update():
    global col
    amountinvested=0
    curr=0
    for i in stocks.values():
        amountinvested+=i[1]
    for i in stocks.keys():
        live2=stock_info.get_live_price(i)
        live2=round(live2,ndigits=2)
        if ".NS" not in i:
            live2*=83
        curr+=live2*stocks[i][0]
    #print(amountinvested)
    #print(curr)
    amount=amountinvested-curr#+extra
    if amount>=0:
        col="#53ff1a"
    else:
        col="#ff0000"
    #print(amount)
    net_sum.config(text=str(amount))
    net_sum.after(1000,update)

def update_live(sto,ch):
    live=stock_info.get_live_price(sto)
    live=round(live,ndigits=2)
    price.config(text=ch+str(live))
    price.after(100,lambda: update_live(sto,ch))
    
#########################     function pages
        
def login():
    global username,frame_username,wlcm,username_text,sign
    login_colour="#ffffff"
    frame_username=tk.Frame(master=window,width=350,height=400,bg=login_colour,borderwidth=3, relief="raised")
    frame_username.place(x=580,y=200)
    wlcm=tk.Label(master=frame_username,text="PaperTrade",font=("Segoe Script Bold",30),bg=login_colour)
    wlcm.place(x=50,y=20)
    username_text=tk.Label(master=frame_username,text="Username",font=("Arial",12),bg=login_colour)
    username_text.place(x=40,y=125)
    username=tk.Entry(master=frame_username,width=20,bd=5,font=("Arial",15))
    username.place(x=45,y=150)
    username.insert(0,"Kunal Virwal")
    sign=tk.Button(master=frame_username,text="Sign in",bg=colour1,fg="white",font=("Arial",15),command=getname)
    sign.place(x=120,y=200)

def home():
    global name,budget,amount,stocks,net_sum,Name,budget_sum,port,stocks_button,wallet_button,hist,info,col
    window.configure(bg=colour2)
    
    Name=tk.Label(master=window,text="  "+name+"  ",font=("Arial Bold",50),bg=colour4,fg="black",borderwidth=5, relief="raised",anchor="w")
    Name.grid(row=1,column=1,padx=40,pady=20)
    budget_sum=tk.Label(master=window,text=u'\u20B9'+str(budget),font=("Arial Bold",30),relief="ridge",bg=colour2,fg="black")
    budget_sum.grid(row=1,column=2,padx=20,pady=20)
    wlcm=tk.Label(master=window,text="PaperTrade",font=("Segoe Script Bold",40),fg="black")
    wlcm.place(x=1100,y=20)   
    port=tk.Button(master=window,text="Portfolio",font=("Arial",30),relief="raised",borderwidth=3,bg=colour2,command=lambda:[home_remove(),portfolio()])
    port.place(x=220,y=150)
    change_on_hover(port,colour2,colour4)
    stocks_button=tk.Button(master=window,text=" Stocks ",font=("Arial",30),relief="raised",borderwidth=3,bg=colour2,command=lambda:[home_remove(),stock_lister()])
    stocks_button.place(x=520,y=150)
    change_on_hover(stocks_button,colour2,colour4)  
    wallet_button=tk.Button(master=window,text=" Wallet ",font=("Arial",30),relief="raised",borderwidth=3,bg=colour2,command=lambda:[home_remove(),wallet_sum()])
    wallet_button.place(x=820,y=150)
    change_on_hover(wallet_button,colour2,colour4)
    hist=tk.Button(master=window,text="History",font=("Arial",30),relief="raised",borderwidth=3,bg=colour2)
    hist.place(x=1120,y=150)
    change_on_hover(hist,colour2,colour4)  
    info=tk.Frame(master=window,width=500,height=200,bg=colour4,borderwidth=8, relief="raised")
    info.place(x=200,y=250)
    #info.grid(row=3,column=1,columnspan=4,padx=20)
    #info.grid_propagate(False)  
    net=tk.Label(master=info,text="Net",font=("Times New Roman",30),bg=colour4,fg="black")
    net.grid(row=1,column=1,padx=90,pady=10) 
    stock=tk.Label(master=info,text="Stocks",font=("Times New Roman",30),bg=colour4,fg="black")
    stock.grid(row=1,column=2,padx=90,pady=10)
    shares=tk.Label(master=info,text="Shares",font=("Times New Roman",30),bg=colour4,fg="black")
    shares.grid(row=1,column=3,padx=90,pady=10)
    trades_taken=tk.Label(master=info,text="Trades",font=("Times New Roman",30),bg=colour4,fg="black")
    trades_taken.grid(row=1,column=4,padx=90,pady=10)
    print(amount)
    
    
    net_sum=tk.Label(master=info,text=amount,font=("Arial Bold",30),bg=colour4,fg=col)
    net_sum.grid(row=2,column=1,padx=90,pady=20)
    stock_num=tk.Label(master=info,text=len(stocks),font=("Arial Bold",30),bg=colour4,fg="black")
    stock_num.grid(row=2,column=2,padx=90,pady=20)
    shar=0
    for i in stocks.values():
        shar+=i[0]
    shares_num=tk.Label(master=info,text=shar,font=("Arial Bold",30),bg=colour4,fg="black")
    shares_num.grid(row=2,column=3,padx=90,pady=20)
    trades_num=tk.Label(master=info,text=trades,font=("Arial Bold",30),bg=colour4,fg="black")
    trades_num.grid(row=2,column=4,padx=90,pady=20)
    update()

def home_remove():
    remove_grid(Name)
    remove_grid(budget_sum)
    remove_place(port)
    remove_place(stocks_button)
    remove_place(wallet_button)
    remove_place(hist)
    remove_place(info)
    
def portfolio():
    global back,net_sum
    
    sidebar=tk.Frame(master=window,width=120,height=800,bg=colour4,borderwidth=8, relief="raised")
    sidebar.place(x=0,y=0)
    back=tk.Button(master=sidebar,text="<=",font=("Arial",20),width=3,height=1,borderwidth=3,bg=colour2,command=lambda:[remove_place(info),remove_place(sidebar),home()])
    back.place(x=15,y=20)
    stocks_button=tk.Button(master=sidebar,text="Stocks",font=("Arial",18),relief="raised",borderwidth=3,bg=colour4,command=lambda:[remove_place(info),remove_place(sidebar),stock_lister()])
    stocks_button.place(x=6,y=100)
    change_on_hover(stocks_button,colour4,colour2)

    wallet_button=tk.Button(master=sidebar,text="Wallet ",font=("Arial",18),relief="raised",borderwidth=3,bg=colour4)
    wallet_button.place(x=6,y=180)
    change_on_hover(wallet_button,colour4,colour2)

    hist=tk.Button(master=sidebar,text="History",font=("Arial",18),relief="raised",borderwidth=3,bg=colour4)
    hist.place(x=6,y=260)
    change_on_hover(hist,colour4,colour2)

    

    info=tk.Frame(master=window,width=500,height=200,bg=colour4,borderwidth=8, relief="raised")
    info.place(x=150,y=20)
    net=tk.Label(master=info,text="Net",font=("Times New Roman",30),bg=colour4,fg="black")
    net.grid(row=1,column=1,padx=60,pady=10) 
    stock=tk.Label(master=info,text="Stocks",font=("Times New Roman",30),bg=colour4,fg="black")
    stock.grid(row=1,column=2,padx=60,pady=10)
    shares=tk.Label(master=info,text="Shares",font=("Times New Roman",30),bg=colour4,fg="black")
    shares.grid(row=1,column=3,padx=60,pady=10)
    trades_taken=tk.Label(master=info,text="Trades",font=("Times New Roman",30),bg=colour4,fg="black")
    trades_taken.grid(row=1,column=4,padx=60,pady=10)

    if amount>=0:
        col="#53ff1a"
    else:
        col="#ff0000"
    
    net_sum=tk.Label(master=info,text=amount,font=("Arial Bold",30),bg=colour4,fg=col)
    net_sum.grid(row=2,column=1,padx=60,pady=20)
    stock_num=tk.Label(master=info,text=len(stocks),font=("Arial Bold",30),bg=colour4,fg="black")
    stock_num.grid(row=2,column=2,padx=60,pady=20)
    shar=0
    for i in stocks.values():
        shar+=i[0]
    shares_num=tk.Label(master=info,text=shar,font=("Arial Bold",30),bg=colour4,fg="black")
    shares_num.grid(row=2,column=3,padx=60,pady=20)
    trades_num=tk.Label(master=info,text=trades,font=("Arial Bold",30),bg=colour4,fg="black")
    trades_num.grid(row=2,column=4,padx=60,pady=20)
    update()

def stock_lister():

    global share_info,sidebar1,search,stock_name
    
    share_info=tk.Frame()
    
    stock_name=tk.Entry(window,width=20,font=("Arial",25))
    stock_name.insert(0,"Search")
    stock_name.place(x=200,y=40)
    
    search=tk.Button(master=window,text="Search",font=("Arial",18),relief="raised",borderwidth=3,bg=colour4,command=lambda:[remove_place(share_info),stock_display(stock_name.get())])
    search.place(x=600,y=40)
    
    
    sidebar1=tk.Frame(master=window,width=120,height=800,bg=colour4,borderwidth=8, relief="raised")
    sidebar1.place(x=0,y=0)
    
    back=tk.Button(master=sidebar1,text="<=",font=("Arial",20),width=3,height=1,borderwidth=3,bg=colour2,command=lambda:[remove_place(share_info),remove_place(search),remove_place(stock_name),remove_place(sidebar1),home()])
    back.place(x=15,y=20)
    
    stocks_button=tk.Button(master=sidebar1,text="Portfolio",font=("Arial",16),relief="raised",borderwidth=3,bg=colour4,command=lambda:[remove_place(share_info),remove_place(search),remove_place(stock_name),remove_place(sidebar1),portfolio()])
    stocks_button.place(x=4,y=105)
    #change_on_hover(stocks_button,colour4,colour2)

    wallet_button=tk.Button(master=sidebar1,text="Wallet ",font=("Arial",18),relief="raised",borderwidth=3,bg=colour4)
    wallet_button.place(x=6,y=180)
    #change_on_hover(wallet_button,colour4,colour2)

    hist=tk.Button(master=sidebar1,text="History",font=("Arial",18),relief="raised",borderwidth=3,bg=colour4)
    hist.place(x=6,y=260)
    #change_on_hover(hist,colour4,colour2)
    
def remove_lister():
    remove_place(sidebar1)
    remove_place(search)
    remove_place(stock_name)
    
def stock_display(sto):
    
    global share_info,price,live
    sto=sto.upper()
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    data=pd.DataFrame()

    
    if (sto+".csv") not in files:
        data=yf.download(sto)
    else:
        data=pd.read_csv(sto+".csv")
        
    if not(data.empty):
        data.to_csv(f"{sto}.csv")
        share_info=tk.Frame(master=window,width=500,height=200,bg=colour4,borderwidth=8,relief="raised")
        share_info.place(x=200,y=100)
        share_name=tk.Label(master=share_info,text=sto,font=("Arial Bold",20),bg=colour2,fg="black")
        share_name.grid(row=1,column=1,padx=20,pady=10)
        live=stock_info.get_live_price(sto)
        live=round(live,ndigits=2)
        if ".NS" in sto:
            ch=u'\u20B9'
        else:
            ch="$"
        price=tk.Label(master=share_info,text=ch+str(live),font=("Arial Bold",20),bg=colour2,fg="black")
        price.grid(row=1,column=2,padx=30,pady=10)
        view=tk.Button(master=share_info,text="View",font=("Arial Bold",15),relief="raised",borderwidth=3,bg=colour2,command=lambda:[ remove_place(share_info) , remove_lister(), stock_detail(sto)])
        view.grid(row=1,column=3,padx=30,pady=10)
        update_live(sto,ch)


def stock_detail(sto):
    global stname,budget_sum,back,graph,toolbar,buyy,selll,price,shares_qty
    stname=tk.Label(master=window,text="  "+sto+"  ",font=("Arial Bold",50),bg=colour4,fg="black",borderwidth=5, relief="raised",anchor="w")
    stname.place(x=100,y=15)
    budget_sum=tk.Label(master=window,text=u'\u20B9'+str(budget),font=("Arial Bold",40),relief="ridge",bg=colour2,fg="black")
    budget_sum.place(x=800,y=30)
    back=tk.Button(master=window,text="<=",font=("Arial",25),width=3,height=1,borderwidth=3,bg=colour2,command=lambda:[remove_stocks(),stock_lister()])
    back.place(x=15,y=20)
    fig = Figure(dpi = 100)
    
    df=pd.read_csv(sto+".csv")
    with pd.ExcelWriter(sto+".xlsx") as writer:
        df.to_excel(writer, sheet_name="MySheet")
        auto_adjust_xlsx_column_width(df, writer, sheet_name="MySheet", margin=0)
    df=pd.read_excel(sto+".xlsx")
    os.remove(sto+".xlsx")
    x=[]
    y=[]
    
    if df["Date"][0][2]!="-":
        for i in df["Date"]:
             x.append(pd.to_datetime(i[:4]))
    else:
        for i in df["Date"]:
            x.append(pd.to_datetime(i[6:]+i[2:6]+i[:2]))
    for i in df["Close"]:
        i=round(i,ndigits=2)
        y.append(i)
    plot1 = fig.add_subplot(111)
    fig.set_figwidth(12)
    fig.set_figheight(3)
    plot1.plot(x,y,linewidth=1)
    canvas = FigureCanvasTkAgg(fig,master=window)
    canvas.draw()
    canvas.get_tk_widget().place(x=100,y=150)
    
    toolbar = NavigationToolbar2Tk(canvas,window)
    toolbar.update()
    #canvas.get_tk_widget().place(x=100,y=150)
    graph=canvas.get_tk_widget()
    #plt.grid()
    #plt.title=(sto)
    #plt.show()
    live=stock_info.get_live_price(sto)
    live=round(live,ndigits=2)
    buyy=tk.Button(master=window,text=" BUY ",font=("Arial Bold",20),relief="raised",borderwidth=4,bg="#53ff1a",command=lambda:[remove_stocks(),buy(live,sto)])
    buyy.place(x=500,y=500)
    selll=tk.Button(master=window,text="SELL",font=("Arial Bold",20),relief="raised",borderwidth=4,bg="#ff0000",command=lambda:[remove_stocks(),sell(live,sto)])
    selll.place(x=650,y=500)
    shares_qty=tk.Entry(master=window,font=("Arial",15),relief="raised",borderwidth=4)
    shares_qty.place(x=800,y=500)
    shares_qty.insert(0,"Qty. (int)")
    
    if ".NS" in sto:
        ch=u'\u20B9'
    else:
        ch="$"
    price=tk.Label(master=window,text=ch+str(live),font=("Arial Bold",20),bg=colour2,fg="black")
    price.place(x=350,y=500)
    update_live(sto,ch)

def remove_stocks():
    global qty
    remove_place(stname)
    remove_place(budget_sum)
    remove_place(back)
    remove_place(graph)
    remove_place(toolbar)
    remove_place(buyy)
    remove_place(selll)
    remove_place(price)
    qty=shares_qty.get()
    remove_place(shares_qty)

def buy(live2,sto):
    global budget,stocks,trades,qty
    try:
        print("HELLO1")
        qty=int(qty)
        if qty<=0:
            qty=-qty
            
        if".NS" not in sto:
            live2*=83
        #print(budget-qty*live2)    
        if qty*live2<=budget:
            budget-=qty*live2
            print(sto in stocks.keys())
            if sto in stocks.keys():
                stocks[sto][0]+=qty
                stocks[sto][1]+=qty*live2
                
            else:
                print("HELLO3")
                stocks[sto]=[qty,qty*live2]
                
            trades+=1
            portfolio()
             
        else:
            stock_detail(sto)
            
            
    except Exception:
        stock_detail(sto)

def sell(live2,sto):
    global budget,stocks,trades,qty
    try:
        qty=int(qty)
        if qty<=0:
            qty=-qty
        if".NS" not in sto:
            live2*=83
            
        budget-=(qty*live2)
        if sto in stocks.keys() and stocks[sto][0]>=qty:
            stocks[sto][0]-=qty
            budget+=qty*live2
            trades+=1
            portfolio()
        
    except Exception:
        stock_detail(sto)
        

def wallet_sum():
    global budget,budget_sum,sidebar2,money

    budget_sum=tk.Label(master=window,text=u'\u20B9'+str(budget),font=("Arial Bold",40),relief="ridge",bg=colour2,fg="black")
    budget_sum.place(x=800,y=30)
    sidebar2=tk.Frame(master=window,width=120,height=800,bg=colour4,borderwidth=8, relief="raised")
    sidebar2.place(x=0,y=0)
    money=tk.Frame(master=window,width=200,height=400,bg=colour4,borderwidth=8, relief="raised")
    money.place(x=200,y=200)

    
    back=tk.Button(master=sidebar2,text="<=",font=("Arial",20),width=3,height=1,borderwidth=3,bg=colour2,command=lambda:[remove_wallet(),home()])
    back.place(x=15,y=20)
    stocks_button=tk.Button(master=sidebar2,text="Stocks",font=("Arial",18),relief="raised",borderwidth=3,bg=colour4,command=lambda:[remove_wallet(),stock_lister()])
    stocks_button.place(x=4,y=105)
    
    port_button=tk.Button(master=sidebar2,text="Portfolio",font=("Arial",16),relief="raised",borderwidth=3,bg=colour4,command=lambda:[remove_wallet(),portfolio()])
    port_button.place(x=6,y=180)
    
    hist=tk.Button(master=sidebar2,text="History",font=("Arial",18),relief="raised",borderwidth=3,bg=colour4)
    hist.place(x=6,y=260)

    thousand=tk.Button(master=money,text="+1000",font=("Arial",18),relief="raised",borderwidth=3,bg=colour4,command=lambda:[budgetplus(1000)])
    thousand.grid(row=1,column=1,padx=20,pady=20)
    tenthousand=tk.Button(master=money,text="+10000",font=("Arial",18),relief="raised",borderwidth=3,bg=colour4,command=lambda:[budgetplus(10000)])
    tenthousand.grid(row=1,column=2,padx=20,pady=20)
    lakh=tk.Button(master=money,text="+100000",font=("Arial",18),relief="raised",borderwidth=3,bg=colour4,command=lambda:[budgetplus(100000)])
    lakh.grid(row=2,column=1,padx=20,pady=20)
    tenlakh=tk.Button(master=money,text="+1000000",font=("Arial",18),relief="raised",borderwidth=3,bg=colour4,command=lambda:[budgetplus(1000000)])
    tenlakh.grid(row=2,column=2,padx=20,pady=20)

def remove_wallet():
    global money,sidebar2,budget_sum
    remove_place(money)
    remove_place(sidebar2)
    remove_place(budget_sum)
    
def budgetplus(n):
    global budget
    budget+=n
    budget_sum.config(text=budget)

        

    
########################

window=tk.Tk()
window.title("PaperTrade")
window.geometry("1920x1080")
window.configure(bg=colour1)
login()
window.mainloop()


