
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector as pymysql

top=Tk()
top.title("BILLING")
top.geometry("900x600")
#****************global variable for entries*********

#1}*************QUANTITY,COST,RATE****************
def quantityfieldlistener(a,b,c):
    global quantityvar
    global costvar
    global itemrate
    quantity=quantityvar.get()
    if quantity!="":
        try:
            quantity=float(quantity)
            itemrate=float(itemrate)
            cost=quantity*itemrate
            cost=float(cost)
            costvar.set("%.2f"%cost)
        except ValueError:
            quantity=quantity[:-1]
            quantityvar.set("%.2f"%quantity)
    else:
        quantity=0
        quantityvar.set("%.2f"%quantity)


def costfieldlistener(a,b,c):
    global quantityvar
    global costvar
    global itemrate
    cost=costvar.get()
    if cost!="":
        try:
            cost=float(cost)
            itemrate=float(itemrate)
            quantity=cost/itemrate
            quantity=float(quantity)
            quantityvar.set("%.2f"%quantity)
            costvar.set(cost)
        except ValueError:
            cost=cost[:-1]
    else:
        cost=0
        costvar.set("%.2f"%cost)
 
    
#****************loginvariable**************
usernamevar=StringVar()
passwordvar=StringVar()

#****************main window variable*********
options=[]
ratedict=()
itemvariable=StringVar()
quantityvar=StringVar()
quantityvar.trace("w",quantityfieldlistener)
itemrate=1
costvar=StringVar()
costvar.trace("w",costfieldlistener)
ratevar=StringVar()
ratevar.set("%.2f"%itemrate)
#***************in treeview**************

#A}********MAINWINDOW TREEVIEW***********
billstv=ttk.Treeview(height=15,column=("quantity","rate","cost"))

#b]********UPDATEWINDOW TREEVIEW*********
updatetv=ttk.Treeview(height=15,columns=("name","rate","type","store_type"))

#***************add item ***************
storeOptions=["Frozen","FRESH","PACKED"]
additemnamevar=StringVar()
additemratevar=StringVar()
additemtypevar=StringVar()
additemstoredvar=StringVar()
additemstoredvar.set(storeOptions[0])

itemlists=list()
totalcost=0.0
totalcostvar=StringVar()
totalcostvar.set(totalcost)
updateitemid=""

#*************CLEAR BILL***********************
def clearbill():
    conn=pymysql.connect(host="localhost",user="root",passwd="student",db="billservice")
    cursor=conn.cursor()
    query="DELETE FROM bill"
    cursor.execute(query)
    conn.commit()
    conn.close()
    updatebillview()

#************GENERATING BILL********************    
def generate_bill():
    global itemvariable
    global quantityvar
    global itemrate
    global costvar
    global itemlists
    global totalcost
    global totalcostvar
    global updateitemid
    itemname=itemvariable.get()
    itemrate=ratevar.get()
    quantity=quantityvar.get()
    cost=costvar.get()
    conn=pymysql.connect(host="localhost",user="root",passwd="student",db="billservice")
    cursor=conn.cursor()
    totalcost+=float(cost)
    query="insert into bill (name,id,rate,quantity,cost) values('{}','{}','{}','{}','{}')"
    cursor.execute(query.format(itemname,itemname,quantity,itemrate,cost))
    conn.commit()
    conn.close()
    listdict={"name":itemname,"rate":itemrate,"quantity":quantity,"cost":cost}
    itemlists.append(listdict)
    totalcost+=float(eval(cost))
   # print(itemlists)
    quantityvar.set("0")
    costvar.set("0")
    updatebillview()
    totalcostvar.set(totalcost/2) 

#**************UPDATE BILL ******************
def updatebillview():
    records=billstv.get_children()

    for elements in records:
        billstv.delete(elements)
    conn=pymysql.connect(host="localhost",user="root",passwd="student",db="billservice")
    cursor=conn.cursor(dictionary=True)
    query="select * from bill"
    cursor.execute(query)
    data=cursor.fetchall()
#    print(data)
    for row in data:
        billstv.insert('','end',text=row['name'],values=(row["quantity"],row["rate"],row["cost"]))
#**********DOUBLE CLICK**********************
def doubleclick(event):  
    global additemnamevar
    global additemratevar
    global additemtypevar
    global additemstoredvar 
    item = updatetv.selection()
    #print(item)
    updateitemid=updatetv.item(item,"text")
    itemdetail=updatetv.item(item,"values")
    itemindex=storeOptions.index(itemdetail[3])
    additemtypevar.set(itemdetail[2])
    additemratevar.set(itemdetail[1])
    additemnamevar.set(itemdetail[0])
        
    additemstoredvar.set(storeOptions[itemindex])
        
def updateitemview():
    records=updatetv.get_children()

    for elements in records:
        updatetv.delete(elements)
    conn=pymysql.connect(host="localhost",user="root",passwd="student",db="billservice")
    cursor=conn.cursor(dictionary=True)
    query="select * from itemlist"
    cursor.execute(query)
    data=cursor.fetchall()
    for row in data:
        updatetv.insert('','end',text=row['nameid'],values=(row["name"],row["rate"],row["type"],row["storedtype"]))

    updatetv.bind("<Double-1>",doubleclick)
    billstv.grid_forget()

    conn.close()    

def print_bill():
    import time
    import datetime as dt
    global itemlists
    global totalcost
    global localtime
    localtime=time.asctime(time.localtime(time.time()))
 
    print("************************RECEIPT*********************\n")
    print("TIME=",localtime)
 
    print("************************RECEIPT********************* ")
    print("{:<20}{:<10}{:<15}{:<10}".format("NAME","RATE","QUANTITY","COST"))#left  aligning
    print("************************RECEIPT*********************")
    for item in itemlists:
        print("{:<20}{:<10}{:<15}{:<10}".format(item["name"],item["rate"],item["quantity"],item["cost"]))

    print("************************RECEIPT*********************")
    print("{:<20}{:<10}{:<15}{:<10}".format("TOTAL COST"," "," ",totalcost/2))

    itemlists=[]
    totalcost=0.0
    updatebillview()
    totalcostvar.set(totalcost/2) 


############LOGOUT########
def logout():
    removeallwidgets()
    additionalwindow()
    billstv.grid_forget()
    #messagebox.showinfo("thank you","THANK YOU..PLEASE CLOSE THE WINDOW")
def movetoupdate():
    removeallwidgets()
    updateitemwindow()
    billstv.grid_forget()
def movetomain1():
    removeallwidgets()
    additionalwindow()
    billstv.grid_forget()
def movetomain():
    removeallwidgets()
    additionalwindow()
    updatetv.grid_forget()
   
#***************update item***************
delnamevar=StringVar()

#*************read all data***********
def readalldata():
    global options
    global ratedict
    global itemvariable
    global itemrate
    global ratevar
    options=[]
    ratedict={}
    conn=pymysql.connect(host="localhost",user="root",passwd="student",db="billservice")
    cursor=conn.cursor(dictionary=True)

    query="select * from itemlist"
    cursor.execute(query)
    data=cursor.fetchall()
    count=0
    for row in data:
        count+=1
        options.append(row['nameid'])
        ratedict[row['nameid']]=row['rate']
        itemvariable.set(options[0])
        itemrate=int(ratedict[options[0]])
    conn.close()
    ratevar.set("%.2f"%itemrate)
    if count==0:
        removeallwidgets()
        itemaddwindow()
    else:
        removeallwidgets()
        mainwindow()

def optionmenulistener(event):
    global itemvariable
    global ratedict
    global itemrate
    item=itemvariable.get()
    itemrate=int(ratedict[item])
    ratevar.set("%.2f"%itemrate)    
        
def removeallwidgets():
   list=top.grid_slaves()
   if updatetv in list:
       list.remove(updatetv)
   if billstv in list:
      list.remove(billstv)
   for l in list:
       l.destroy()
        
def adminlogin():
    global usernamevar
    global passwordvar

    username=usernamevar.get()
    password=passwordvar.get()
    conn=pymysql.connect(host="localhost",user="root",passwd="student",db="billservice")
    cursor=conn.cursor()
    query="select username,password from users where username='{}' and password='{}'".format(username,password)
    cursor.execute(query)
    data=cursor.fetchall()
    admin=False
    for row in data:
        admin=True
    conn.close()
    if admin:
        removeallwidgets()
        additionalwindow()
    else:
        messagebox.showerror("invalid user","credentials entries are invalid")
def additemlistener():
    removeallwidgets()
    itemaddwindow()
    billstv.grid_forget()

def additem():
    global additemnamevar
    global additemratevar
    global additemtypevar
    global additemstoredvar
    name=additemnamevar.get()
    rate=additemratevar.get()
    type=additemtypevar.get()
    storedtype=additemstoredvar.get()
    nameid=name.replace(" ","_")
    conn=pymysql.connect(host="localhost",user="root",passwd="student",db="billservice")
    cursor=conn.cursor()
    query="insert into itemlist (name,nameid,rate,type,storedtype)values('{}','{}','{}','{}','{}')"
    cursor.execute(query.format(name,nameid,rate,type,storedtype))
    conn.commit()
    conn.close()
    additemnamevar.set("")
    additemratevar.set("")
    additemtypevar.set("")

def updateitem():
    global additemnamevar
    global additemratevar
    global additemtypevar
    global additemstoredvar
    name=additemnamevar.get()
    rate=additemratevar.get()
    type=additemtypevar.get()
    storedtype=additemstoredvar.get()
    updateitemid=name.replace(" ","_")
    conn=pymysql.connect(host="localhost",user="root",passwd="student",db="billservice")
    cursor=conn.cursor()
    query="update itemlist set name='{}',rate='{}',type='usernamevar{}',storedtype='{}' where nameid='{}'".format(name,rate,type,storedtype,updateitemid)
    cursor.execute(query)
    conn.commit()
    conn.close()    
    additemnamevar.set("")
    additemratevar.set("")
    additemtypevar.set("")
    updateitemview()
def delitem(): 
    global delnamevar  
    ID=delnamevar.get()
    conn=pymysql.connect(host="localhost",user="root",passwd="student",db="billservice")
    cursor=conn.cursor()
    query="delete from itemlist where nameid='{}'"
    cursor.execute(query.format(ID))
    conn.commit()
    conn.close()
    delnamevar.set("")
    updateitemview()
def exit():
    top.destroy()
def goback():
    updatetv.grid_forget()
    readalldata() 
def loginwindow():
    titlelabel=Label(top,text="KAJB GENERAL STORE",font="ARIAL 40",fg="red")
    titlelabel.grid(row=0,column=3,columnspan=2,padx=(40,0),pady=(10,0))

    loginlabel=Label(top,text="ADMIN LOGIN",font="arial 20")
    loginlabel.grid(row=1,column=2,padx=20,pady=10)

    usernamelabel=Label(top,text="username",font="arial 15")
    usernamelabel.grid(row=2,column=2,padx=20,pady=10)

    passwordlabel=Label(top,text="password",font="arial 15")
    passwordlabel.grid(row=3,column=2,padx=20,pady=10)

    usernameentry=Entry(top,textvariable=usernamevar)
    usernameentry.grid(row=2,column=3,padx=20,pady=10)

    passwordentry=Entry(top,textvariable=passwordvar,show="*")
    passwordentry.grid(row=3,column=3,padx=20,pady=10)

    loginbutton=Button(top,text="LOG  IN",bg="red",fg="black",width=20,height=2,command=lambda:adminlogin())
    loginbutton.grid(row=4,column=2,padx=20,pady=10)


def mainwindow():
    
    titlelabel=Label(top,text="BILLING SYSTEM",font="ARIAL 40",fg="green")
    titlelabel.grid(row=0,column=0,columnspan=3,padx=(40,0),pady=(10,0))               

    addnewitem=Button(top,text="ADD ITEM",width=15,height=2,bg="blue",command=lambda:additemlistener())
    addnewitem.grid(row=1,column=0,padx=(10,0),pady=(10,0))

    updateitem=Button(top,text="UPDATE  ITEM",width=15,height=2,bg="green",command=lambda:movetoupdate())
    updateitem.grid(row=1,column=1,padx=(10,0),pady=(10,0))
##

    logoutbutton=Button(top,text="EXIT",width=20,height=2,bg="violet",command=lambda:logout())
    logoutbutton.grid(row=1,column=5,pady=(10,0))

    itemlabel=Label(top,text="SELECT ITEM",font="arial 10")
    itemlabel.grid(row=2,column=0,padx=(5,0))
    
    itemdropdown=OptionMenu(top,itemvariable,*options,command=optionmenulistener)
    itemdropdown.grid(row=2,column=1,padx=(10,0))
    
    ratelabel=Label(top,text="RATE",font="arial 10")
    ratelabel.grid(row=1,column=2,pady=(10,0))

    ratevalue=Entry(top,textvariable=ratevar)
    ratevalue.grid(row=1,column=3,pady=(10,0))

    clearbills=Button(top,text="CLEAR BILLS",width=20,bg="pink",command=lambda:clearbill())
    clearbills.grid(row=7,column=0) 


    quantitylabel=Label(top,text="QUANTITY",font="arial 10")
    quantitylabel.grid(row=2,column=2,padx=(5,0))

    quantityentry=Entry(top,textvariable=quantityvar)
    quantityentry.grid(row=2,column=3,padx=(5,0),pady=(10,0))

    costlabel=Label(top,text="COST",font="arial 10",)
    costlabel.grid(row=3,column=2,pady=(10,0))

    costentry=Entry(top,textvariable=costvar)
    costentry.grid(row=3,column=3,pady=(10,0))
    

    buttonbill=Button(top,text="ADD TO LIST",width=20,bg="red",command=lambda:generate_bill())
    buttonbill.grid(row=3,column=5)
    
    billlabel=Label(top,text="BILLS",font="ariel 20")
    billlabel.grid(row=4,column=2,padx=(10,0),pady=(10,0))


    billstv.grid(row=6,column=0,columnspan=5)

    scrollbar=Scrollbar(top,orient="vertical",command=billstv.yview)
    scrollbar.grid(row=6,column=4,sticky="NSE")

    billstv.configure(yscrollcommand=scrollbar.set)

    billstv.heading('#0',text="ITEM NAME")
    billstv.heading('#1',text="RATE")
    billstv.heading('#2',text="QUANTITY")
    billstv.heading('#3',text="COST")

    totalcostlabel=Label(top,text="TOTAL COST",font="arial 15")
    totalcostlabel.grid(row=7,column=1)

    totalcostentry=Entry(top,textvariable=totalcostvar)
    totalcostentry.grid(row=7,column=2)


    generatebill=Button(top,text="GENERATE BILL",width=15,fg="green",bg="orange",command=lambda:print_bill())
    generatebill.grid(row=7,column=3)
    updatebillview()
def itemaddwindow():
    backbutton=Button(top,text="BACK",command=lambda: movetomain1())
    backbutton.grid(row=0,column=0,columnspan=4,pady=(10,0))
    
    titlelabel=Label(top,text="BILLING SYSTEM",font="ARIAL 40",fg="green")
    titlelabel.grid(row=0,column=4,columnspan=3,padx=(40,0),pady=(10,0))
    
    itemlabel=Label(top,text="NAME")
    itemlabel.grid(row=1,column=1,pady=(10,0))

    itementry=Entry(top,textvariable=additemnamevar)
    itementry.grid(row=1,column=2,pady=(10,0))

    ratelabel=Label(top,text="RATE")
    ratelabel.grid(row=1,column=5,pady=(10,0))

    rateentry=Entry(top,textvariable=additemratevar)
    rateentry.grid(row=1,column=6,pady=(10,0))

    typelabel=Label(top,text="TYPE")
    typelabel.grid(row=2,column=1,pady=(10,0))

    typeentry=Entry(top,textvariable=additemtypevar)
    typeentry.grid(row=2,column=2,pady=(10,0))

    storetypelabel=Label(top,text="STOREDTYPE")
    storetypelabel.grid(row=2,column=5,pady=(10,0))

    storetypeentry=OptionMenu(top,additemstoredvar,*storeOptions)
    storetypeentry.grid(row=2,column=6,pady=(10,0))

    additembutton=Button(top,text="ADD ITEM",width=20,height=2,command=lambda:additem())
    additembutton.grid(row=3,column=3,pady=(10,0))

def updateitemwindow():
    backbutton=Button(top,text="BACK",command=lambda: movetomain())
    backbutton.grid(row=0,column=0,columnspan=4,pady=(10,0))

    deletelabel=Label(top,text="DELETE ITEM")
    deletelabel.grid(row=8,column=3,pady=(0,10))
    delentry=Entry(top,textvariable=delnamevar)
    delentry.grid(row=8,column=2,pady=(0,10))
    dellabel=Label(top,text="ITEM ID")
    dellabel.grid(row=8,column=1,pady=(0,10))
    delitembutton=Button(top,text="DELETE ITEM",width=20,height=2,command=lambda:delitem())
    delitembutton.grid(row=8,column=3,pady=(10,0))
    
    titlelabel=Label(top,text="BILLING SYSTEM",font="ARIAL 40",fg="green")
    titlelabel.grid(row=0,column=4,columnspan=3,padx=(40,0),pady=(10,0))
    
    itemlabel=Label(top,text="NAME")
    itemlabel.grid(row=1,column=1,pady=(10,0))

    itementry=Entry(top,textvariable=additemnamevar)
    itementry.grid(row=1,column=2,pady=(10,0))

    ratelabel=Label(top,text="RATE")
    ratelabel.grid(row=1,column=5,pady=(10,0))

    rateentry=Entry(top,textvariable=additemratevar)
    rateentry.grid(row=1,column=6,pady=(10,0))

    typelabel=Label(top,text="TYPE")
    typelabel.grid(row=2,column=1,pady=(10,0))

    typeentry=Entry(top,textvariable=additemtypevar)
    typeentry.grid(row=2,column=2,pady=(10,0))

    storetypelabel=Label(top,text="STOREDTYPE")
    storetypelabel.grid(row=2,column=5,pady=(10,0))

    storetypeentry=OptionMenu(top,additemstoredvar,*storeOptions)
    storetypeentry.grid(row=2,column=6,pady=(10,0))

    additembutton=Button(top,text="UPDATE ITEM",width=20,height=2,command=lambda:updateitem())
    additembutton.grid(row=3,column=3,pady=(10,0))

    updatetv.grid(row=4,column=0,columnspan=5)
    scrollbar=Scrollbar(top,orient="vertical",command=updatetv.yview)
    scrollbar.grid(row=4,column=4,sticky="NSE")

    updatetv.configure(yscrollcommand=scrollbar.set)

    updatetv.heading('#0',text="ITEM ID")
    updatetv.heading('#1',text="ITEM NAME")
    updatetv.heading('#2',text="RATE")
    updatetv.heading('#3',text="TYPE")
    updatetv.heading('#4',text="STORED TYPE")
    updateitemview()

def additionalwindow():

    titlelabel=Label(top,text="   MENU   ",font="ARIAL 40",fg="green")
    titlelabel.grid(row=0,column=0,columnspan=2,padx=(40,0),pady=(10,0))
    
    titlelabel2=Label(top,text="------------------------  ",font="ARIAL 40",fg="green")
    titlelabel2.grid(row=1,column=0,padx=(40,0),pady=(10,0))
    
    main1=Button(top,text="1.GENERAL STORE BILLING SECTION",width=60,bg="red",command=lambda:readalldata())
    main1.grid(row=3,column=7,padx=(10,0),pady=(10,0))

    main1=Button(top,text="2.ITEM ADD SECTION",width=60,bg="green",command=lambda:additemlistener())
    main1.grid(row=5,column=7,padx=(10,0),pady=(10,0))

    main1=Button(top,text="3. UPDATE ITEM ",width=60,bg="orange",command=lambda:movetoupdate())
    main1.grid(row=7,column=7,padx=(10,0),pady=(10,0))

    main1=Button(top,text="4.CAFE BILLING SECTION",width=60,bg="blue",command=lambda:cafe())
    main1.grid(row=9,column=7,padx=(10,0),pady=(10,0))

    main1=Button(top,text="5.EXIT",width=60,bg="violet",command=lambda:exit())
    main1.grid(row=11,column=7,padx=(10,0),pady=(10,0))


def cafe():
    removeallwidgets()
    import random
    import time
    import pickle
    import datetime as dt
    Tops=Frame(top,bg="white",width = 1600,height=50,relief=SUNKEN)
    Tops.pack(side=TOP)

    f1=Frame(top,width = 900,height=700,relief=SUNKEN)
    f1.pack(side=LEFT)

    f2=Frame(top ,width = 400,height=700,relief=SUNKEN)
    f2.pack(side=RIGHT)
    ############################TO DISPLAY TIME#####################################
    global localtime
    localtime=time.asctime(time.localtime(time.time()))
    #-----------------PAGE DESIGNING------------
    lblinfo = Label(Tops, font=( 'aria' ,30, 'bold' ),text="STEAMING COFFEE",fg="Black",bd=10,anchor='w')
    lblinfo.grid(row=0,column=0)
    lblinfo = Label(Tops, font=( 'aria' ,20, ),text=localtime,fg="steel blue",anchor=W)
    lblinfo.grid(row=1,column=0)

    #definition of functions>>>>>>>>>>>>>>>>>>>>>>


    def Ref():
        x=random.randint(12980, 50876)
        randomRef = str(x)
        rand.set(randomRef)

        cof =float(Fries.get())
        colfries= float(Largefries.get())
        cob= float(Burger.get())
        cofi= float(Filet.get())
        cochee= float(Cheese_burger.get())
        codr= float(Drinks.get())

        costoffries = cof*25
        costoflargefries = colfries*60
        costofburger = cob*200
        costoffilet = cofi*550
        costofcheeseburger = cochee*210
        costofdrinks = codr*90
        p=costoffries +  costoflargefries + costofburger + costoffilet + costofcheeseburger + costofdrinks

        costofmeal = "Rs.",str('%.2f'% (p))
        PayTax=((p)*0.03)  
        Totalcost=p
        Ser_Charge=((p)/99)
        Service="Rs.",str('%.2f'% Ser_Charge)
        OverAllCost="Rs.",str(int( PayTax + Totalcost + Ser_Charge))
        PaidTax="Rs.",str('%.2f'% PayTax)

        Service_Charge.set(Service)
        cost.set(costofmeal)
        Tax.set(PaidTax)
        Subtotal.set(costofmeal)
        Total.set(OverAllCost)

        
        t=dt.datetime.now()
        t=str(t)
        date,tm=t.split()
        t1,t2=tm.split('.',2)
        time=t1

        
        
        over=int(Totalcost+PayTax+Ser_Charge)    #variable to hold grand total
        
        
        fin=open('caferecord.txt','ab')
        dictu={"orderno":x,"date":date,"time":t1,"total Price":over}
        pickle.dump(dictu,fin)
        print("-" *80)
        fin.close()
        print("ORDER NO","DATE","TIME","TOTAL PRICE",sep="\t\t")
        for i in dictu.values():
            print(i,end="\t\t")
        
              
            



    def qexit():
        Tops.pack_forget()
        f1.pack_forget()
        f2.pack_forget()
        movetomain1() 
    def reset():
        rand.set("")
        Fries.set("")
        Largefries.set("")
        Burger.set("")
        Filet.set("")
        Subtotal.set("")
        Total.set("")
        Service_Charge.set("")
        Drinks.set("")
        Tax.set("")
        cost.set("")
        Cheese_burger.set("")


    #---------------------------------------------------------------------------------------
    rand = StringVar()
    Fries = StringVar()
    Largefries = StringVar()
    Burger = StringVar()
    Filet = StringVar()
    Subtotal = StringVar()
    Total = StringVar()
    Service_Charge = StringVar()
    Drinks = StringVar()
    Tax = StringVar()
    cost = StringVar()
    Cheese_burger = StringVar()


    lblreference = Label(f1, font=( 'aria' ,16, 'bold' ),text="Order No.",fg="brown",bd=20,anchor='w')
    lblreference.grid(row=0,column=0)
    txtreference = Entry(f1,font=('ariel' ,16,'bold'), textvariable=rand , bd=6,insertwidth=6,bg="yellow" ,justify='right')
    txtreference.grid(row=0,column=1)

    lblfries = Label(f1, font=( 'aria' ,16, 'bold' ),text=" French Fries ",fg="blue",bd=10,anchor='w')
    lblfries.grid(row=2,column=0)
    txtfries = Entry(f1,font=('ariel' ,16,'bold'), textvariable=Fries , bd=6,insertwidth=4,bg="white" ,justify='right')
    txtfries.grid(row=2,column=1)

    lblLargefries = Label(f1, font=( 'aria' ,16, 'bold' ),text="Lunch ",fg="blue",bd=10,anchor='w')
    lblLargefries.grid(row=3,column=0)
    txtLargefries = Entry(f1,font=('ariel' ,16,'bold'), textvariable=Largefries , bd=6,insertwidth=4,bg="white" ,justify='right')
    txtLargefries.grid(row=3,column=1)


    lblburger = Label(f1, font=( 'aria' ,16, 'bold' ),text="Burger ",fg="blue",bd=10,anchor='w')
    lblburger.grid(row=4,column=0)
    txtburger = Entry(f1,font=('ariel' ,16,'bold'), textvariable=Burger , bd=6,insertwidth=4,bg="white" ,justify='right')
    txtburger.grid(row=4,column=1)

    lblFilet = Label(f1, font=( 'aria' ,16, 'bold' ),text="Pizza ",fg="blue",bd=10,anchor='w')
    lblFilet.grid(row=5,column=0)
    txtFilet = Entry(f1,font=('ariel' ,16,'bold'), textvariable=Filet , bd=6,insertwidth=4,bg="white" ,justify='right')
    txtFilet.grid(row=5,column=1)

    lblCheese_burger = Label(f1, font=( 'aria' ,16, 'bold' ),text="Cheese burger",fg="blue",bd=10,anchor='w')
    lblCheese_burger.grid(row=6,column=0)
    txtCheese_burger = Entry(f1,font=('ariel' ,16,'bold'), textvariable=Cheese_burger , bd=6,insertwidth=4,bg="white" ,justify='right')
    txtCheese_burger.grid(row=6,column=1)

    #--------------------------------------------------------------------------------------
    lblDrinks = Label(f1, font=( 'aria' ,16, 'bold' ),text="Drinks",fg="blue",bd=10,anchor='w')
    lblDrinks.grid(row=1,column=0)
    txtDrinks = Entry(f1,font=('ariel' ,16,'bold'), textvariable=Drinks , bd=6,insertwidth=4,bg="white" ,justify='right')
    txtDrinks.grid(row=1,column=1)

    lblcost = Label(f1, font=( 'aria' ,16, 'bold' ),text="Cost",fg="black",bd=10,anchor='w')
    lblcost.grid(row=2,column=2)
    txtcost = Entry(f1,font=('ariel' ,16,'bold'), textvariable=cost , bd=6,insertwidth=4,bg="white" ,justify='right')
    txtcost.grid(row=2,column=3)

    lblService_Charge = Label(f1, font=( 'aria' ,16, 'bold' ),text="Service Charge",fg="black",bd=10,anchor='w')
    lblService_Charge.grid(row=3,column=2)
    txtService_Charge = Entry(f1,font=('ariel' ,16,'bold'), textvariable=Service_Charge , bd=6,insertwidth=4,bg="white" ,justify='right')
    txtService_Charge.grid(row=3,column=3)

    lblTax = Label(f1, font=( 'aria' ,16, 'bold' ),text="Tax",fg="black",bd=10,anchor='w')
    lblTax.grid(row=4,column=2)
    txtTax = Entry(f1,font=('ariel' ,16,'bold'), textvariable=Tax , bd=6,insertwidth=4,bg="white" ,justify='right')
    txtTax.grid(row=4,column=3)

    lblSubtotal = Label(f1, font=( 'aria' ,16, 'bold' ),text="Subtotal",fg="black",bd=10,anchor='w')
    lblSubtotal.grid(row=5,column=2)
    txtSubtotal = Entry(f1,font=('ariel' ,16,'bold'), textvariable=Subtotal , bd=6,insertwidth=4,bg="white" ,justify='right')
    txtSubtotal.grid(row=5,column=3)

    lblTotal = Label(f1, font=( 'aria' ,16, 'bold' ),text="Total",fg="green",bd=10,anchor='w')
    lblTotal.grid(row=6,column=2)
    txtTotal = Entry(f1,font=('ariel' ,16,'bold'), textvariable=Total , bd=6,insertwidth=4,bg="grey" ,justify='right')
    txtTotal.grid(row=6,column=3)

    #-----------------------------------------buttons------------------------------------------
    lblTotal = Label(f1,text="---------------------",fg="white")
    lblTotal.grid(row=7,columnspan=3)

    btnTotal=Button(f1,padx=16,pady=8, bd=10 ,fg="black",font=('ariel' ,16,'bold'),width=10, text="TOTAL", bg="red",command=Ref)
    btnTotal.grid(row=8, column=1)

    btnreset=Button(f1,padx=16,pady=8, bd=10 ,fg="black",font=('ariel' ,16,'bold'),width=10, text="RESET", bg="red",command=reset)
    btnreset.grid(row=8, column=2)

    btnexit=Button(f1,padx=16,pady=8, bd=10 ,fg="black",font=('ariel' ,16,'bold'),width=10, text="EXIT", bg="red",command=qexit)
    btnexit.grid(row=8, column=3)

    def price():
        roo = Tk()
        roo.geometry("600x220+0+0")
        roo.title("Price List")
        lblinfo = Label(roo, font=('aria', 15, 'bold'), text="ITEM", fg="black", bd=5)
        lblinfo.grid(row=0, column=0)
        lblinfo = Label(roo, font=('aria', 15,'bold'), text="_____________", fg="white", anchor=W)
        lblinfo.grid(row=0, column=2)
        lblinfo = Label(roo, font=('aria', 15, 'bold'), text="PRICE", fg="black", anchor=W)
        lblinfo.grid(row=0, column=3)
        lblinfo = Label(roo, font=('aria', 15, 'bold'), text="French Fries", fg="steel blue", anchor=W)
        lblinfo.grid(row=1, column=0)
        lblinfo = Label(roo, font=('aria', 15, 'bold'), text="25", fg="steel blue", anchor=W)
        lblinfo.grid(row=1, column=3)
        lblinfo = Label(roo, font=('aria', 15, 'bold'), text="Lunch ", fg="steel blue", anchor=W)
        lblinfo.grid(row=2, column=0)
        lblinfo = Label(roo, font=('aria', 15, 'bold'), text="40", fg="steel blue", anchor=W)
        lblinfo.grid(row=2, column=3)
        lblinfo = Label(roo, font=('aria', 15, 'bold'), text="Burger ", fg="steel blue", anchor=W)
        lblinfo.grid(row=3, column=0)
        lblinfo = Label(roo, font=('aria', 15, 'bold'), text="200", fg="steel blue", anchor=W)
        lblinfo.grid(row=3, column=3)
        lblinfo = Label(roo, font=('aria', 15, 'bold'), text="Pizza ", fg="steel blue", anchor=W)
        lblinfo.grid(row=4, column=0)
        lblinfo = Label(roo, font=('aria', 15, 'bold'), text="550", fg="steel blue", anchor=W)
        lblinfo.grid(row=4, column=3)
        lblinfo = Label(roo, font=('aria', 15, 'bold'), text="Cheese Burger", fg="steel blue", anchor=W)
        lblinfo.grid(row=5, column=0)
        lblinfo = Label(roo, font=('aria', 15, 'bold'), text="210", fg="steel blue", anchor=W)
        lblinfo.grid(row=5, column=3)
        lblinfo = Label(roo, font=('aria', 15, 'bold'), text="Drinks", fg="steel blue", anchor=W)
        lblinfo.grid(row=6, column=0)
        lblinfo = Label(roo, font=('aria', 15, 'bold'), text="90", fg="steel blue", anchor=W)
        lblinfo.grid(row=6, column=3)

        roo.mainloop()
    btnprice=Button(f1,padx=16,pady=8, bd=10 ,fg="black",font=('ariel' ,16,'bold'),width=10, text="PRICE", bg="red",command=price)
    btnprice.grid(row=8, column=0)

##def passwo():
##    #credentials saver
##    name = input("Please enter your name. ")
##    age = input("Now please enter you age. ")
##
##    username = name[0:3] + age
##    print ("Your username has been created and is", username, ".")
##
##    password = input("Now please create a password. ")
##
##    file = open("Login.txt","a")
##    file.write (username)
##    file.write (",")
##    file.write (password)
##    file.write("\n")
##    file.close()
##    print ("Your login details have been saved. ")
##
##    logged_in = False
##    with open('Login.txt', 'r') as file:
##        for line in file:
##            username, password = line.split(',')
##            # Check the username against the one supplied
##            if username == supplied_username:
##                logged_in = password == supplied_password
##                break
##
##    if logged_in:# our code 
##        
##    else:
##        
##        print('Sorry Your Credentials are invalid')
##
##       
##
##
##
##
##    def main():
##        username, password = get_name_and_password()
##        registered_users = read_pwdfile('pwd_filename')
##        if usr_pass_registered(username, password, registered_users):
##            registered = True
##        else:
##            registered = get_registration(username, password, 'pwd_filename')
##        if registered:
##            run_quiz(username)
    
loginwindow()
top.mainloop()
