import streamlit as st
from PIL import Image
from tabulate import tabulate
import pandas as pd
import mysql.connector
con=mysql.connector.connect(host="localhost",user="root",password="root",database="library")
res=con.cursor()
def get_userid():
    qry = "select user_id from users"
    res.execute(qry)
    result = res.fetchall()
    list_of_ids = []
    for i in result:
        list_of_ids.append(i[0])
    return list_of_ids
def get_user_password():
    qry = "select password from users"
    res.execute(qry)
    result = res.fetchall()
    list_of_password = []
    for i in result:
        list_of_password.append(i[0])
    return list_of_password
def emp_id():
    emp_ids = []
    qry = "select employee_id from employee"
    res.execute(qry)
    data = res.fetchall()
    for i in data:
        emp_ids.append(i[0])
    return emp_ids  
def emps_password():
    emp_password = []
    qry = "select passsword from employee"
    res.execute(qry)
    data = res.fetchall()
    for i in data:
        emp_password.append(i[0])
    return emp_password   
     


st.sidebar.title("options")
user=st.sidebar.radio("Book Store",["customer","Employee"])
if user=="customer":
   cust=st.sidebar.radio("CUSTOMER",["register","login"])
   if cust=="register":
       st.image('library.jpg', caption='Image Caption', use_column_width=True)
       st.title("REGISTER")
       id=st.number_input("enter your user id",step=2)
       name=st.text_input("enter your name")
       email=st.text_input("enter your email_id")
       city=st.text_input("enter your city")
       password=st.number_input("enter your password",step=2)
       phone_no=st.number_input("enter your mobile_number",step=2)
       if st.button("signup"):
          qry='insert into users values(%s,%s,%s,%s,%s,%s)'
          val=(id,name,email,city,password,phone_no)
          res.execute(qry,val)
          con.commit()
          st.info("Registration Successful")
   if cust=="login":
        st.title("LOGIN")
        id=st.number_input("enter your user_id",step=2)
        password=st.number_input("enter your password",step=2)
        if st.button("login"):
           if id in get_userid():
                if password in get_user_password():
                   st.info("login successfully")
                   st.session_state.login=True
           else:
               st.info("incorrect password or user id please check it")
   if st.session_state.get("login", False):
       option= st.sidebar.radio("Options", ["order","view products", "Profile"])
       if option=="order":
           st.title("order page")
           order_id=st.number_input("enter your order id",step=2)
           customer_name=st.text_input("enter your name")
           book_name=st.text_input("enter the book name")
           price=st.number_input("enter the price",step=2)
           quantity=st.number_input("enter the quantity",step=2)
           total_price=quantity*price
           if st.button("place order"):
              qry='insert into orders values(%s,%s,%s,%s,%s,%s)'
              val=(order_id,customer_name,book_name,price,total_price,quantity)
              res.execute(qry,val)
              con.commit()
              st.info("successfully order placed")
       elif option == "view products":
           st.title("Product List")
           qry = 'SELECT * FROM books'
           res.execute(qry)
           result = res.fetchall()
           title=["aurthor","genere","price","stock","book_name"]
           df=pd.DataFrame(result,columns=title)
           st.dataframe(df)
       elif option == "Profile":
           st.title("User Profile")
           id = st.number_input("Enter your id",step=3)

           if st.button("View Profile"):
              qry = 'SELECT * FROM users WHERE user_id=%s'
              val = (id,)
              res.execute(qry, val)
              result = res.fetchone()
              title= ["User ID", "Name", "Email", "City", "Password", "Phone Number"]
              df=pd.DataFrame([result],columns=title)
              st.dataframe(df)
if user=="Employee":
    emp=st.sidebar.radio("Employee",["register","login"])
    if emp=="register":
        employee_id=st.number_input("enter your id",step=2)
        employee_name=st.text_input("enter your name")
        emp_password=st.number_input("enter your password",step=2)
        if st.button("register"):
            qry='insert into employee values(%s,%s,%s)'
            val=(employee_id,employee_name,emp_password)
            res.execute(qry,val)
            con.commit()
            st.info("Register successfull")
    if emp=="login":
        employeeid=st.number_input("enter your id",step=2)
        emp_password=st.number_input("enter your password",step=2)
        if st.button("login"):
           if employeeid in emp_id():
               if emp_password in emps_password():
                   st.info("login successfully")
                   st.session_state.login=True
                    
           else:
               st.info("incorrect password or user id")
    if st.session_state.get("login", False):
        option=st.sidebar.radio("employee services",["update_product","stock_update","update_price","remove_product","show_order"])
        if option=="update_product":
            aurthor=st.text_input("aurthor name")
            genere=st.text_input("enter genere")
            price=st.number_input("enter price",step=2)
            stock=st.number_input("enter stock quantity",step=2)
            name=st.text_input("enter book name")
            if st.button("add"):
               qry = '''insert into books values (%s,%s,%s,%s,%s)'''
               val = (aurthor,genere,price,stock,name)
               res.execute(qry,val)
               con.commit()
               st.info("product added")
        elif option=="stock_update":
            product_name=st.text_input("enter book name")
            quantity=st.number_input("enter the updated quantity",step=2)
            if st.button("update"):
                qry="update books set stock = %s where book_name = %s" 
                val=(quantity,product_name)
                res.execute(qry,val)
                con.commit()
                st.info("stock quantity successfully updated")
        elif option=="update_price":
            product_name=st.text_input("enter book name")
            price=st.number_input("enter price")
            if st.button("update"):
                qry="update books set price = %s where product_name = %s" 
                val=(price,product_name)
                res.execute(qry,val)
                con.commit()
                st.info("product price successfully updated")
        elif option=="remove_product":
            product_name=st.text_input("enter book name")
            if st.button("delete"):
                qry = 'DELETE FROM books WHERE book_name = %s'
                val = (product_name,)
                res.execute(qry,val)
                con.commit()
                st.info("product removed")
        elif option=="show_order" :
            qry='select * from orders'
            res.execute(qry)
            result=res.fetchall()
            title= ["order_id", "customer_Name", "book_name", "price", "total_price", "quantity"]
            df=pd.DataFrame(result,columns=title)
            st.dataframe(df)
    



    
        
            
    
        
                     
    
         
           

    


        
        


