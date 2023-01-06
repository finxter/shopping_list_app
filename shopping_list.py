import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime, date
import calendar
from isoweek import Week
import db as db
from pprint import pprint

#---SETTINGS---#
page_title = "Weekly dinner and shopping app"
page_icon = ":pouch:"
layout = "centered"

#---PAGE CONFIG---#

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(f"{page_title} {page_icon}")

#---PERIOD VALUES---#
year = datetime.today().year
month = datetime.today().month
day = datetime.today().day
months = list(calendar.month_name[1:])
week_number = date(year, month, day).isocalendar()[1]
week = Week(year, week_number)
week_plus1 = Week(year, week_number+1)


#---DICT INIT---#
shopping_list = {
    "fruit_and_veg" : {"title" : "Fruit and Veggies", "items" : []},
    "meat_and_fish" : {"title" :"Fresh meat and fish", "items" : []},
    "housekeeping" : {"title" :"Housekeeping supplies", "items" : []},
    "carbs" : {"title" : "Potatoes, rice, pasta, etc", "items" : []},
    "snacks" : {"title" : "Snacks", "items" : []},
    "dairy" : {"title" : "Dairy", "items" : []},
    "personal_care" : {"title" : "Personal care", "items" : []},
    "pets" : {"title" : "Pets", "items" : []},
    "beverages" : {"title" : "Beverages", "items" : []},
    "spices_and_cond" : {"title" : "Spices and condiments", "items" : []},
    "frozen" : {"title" : "Frozen", "items" : []}
    }

key_dict = {
    'fruit_and_veg': [], 
    'meat_and_fish': [], 
    'housekeeping': [], 
    'carbs': [], 
    'snacks': [], 
    'dairy': [], 
    'personal_care': [], 
    'pets': [], 
    'beverages': [], 
    'spices_and_cond': [], 
    'frozen': []
    }

#---NAV BARS---#
nav_menu = option_menu(
    menu_title = None,
    options = ["Enter shopping list", "Check current shopping list", "Weekly recipes"],
    icons = ["pencil-square", "list-task", "cup-straw" ],
    orientation = "horizontal"
) 

#---INPUT FORM---#
if nav_menu == "Enter shopping list":
    st.header(f"Shopping list for week from Thursday {week.thursday()} to Wednesday {week_plus1.wednesday()}")

    with st.form("entry_form", clear_on_submit=True):
        st.subheader(f"Enter item for shopping list: ")
        
        for k, value in shopping_list.items():
            st.text_input(f"{shopping_list[k]['title']}:", key=k)
                    
        "---"
        submitted = st.form_submit_button("Save shopping list items")     
        if submitted:
            if db.get_shopping_list(week_number):
                
                for key in key_dict:
                    update_dict = {}
                    if st.session_state[key] != '':
                            items = st.session_state[key].split(",")
                            for item in items:
                                item = item.strip()
                            update_dict[key] = items                  
                            db.update_shopping_list(str(week_number), update_dict)
                
            else:     
                period =  f"Shopping list for week from Thursday {week.thursday()} to Wednesday {week_plus1.wednesday()}"  
                
                for key, value in shopping_list.items():                
                    
                    if st.session_state[key] != '':
                        items = st.session_state[key].split(",")
                        for item in items:
                            item = item.strip()
                            shopping_list[key]['items'].append(item)                 
                    db.enter_shopping_list_items(week_number, period, shopping_list)      

if nav_menu == "Check current shopping list":
    
    current_shopping_list = db.get_shopping_list(week_number)
        
    st.subheader(current_shopping_list["title"])         
    "---"
        
    for k, value in current_shopping_list["shopping_list"].items():
        st.subheader(value["title"])
        for item in value["items"]:
            st.button(label = item, on_click=db.remove_item_shopping_list, args= (str(week_number), k, item))
        "----"    

if nav_menu == "Weekly recipes":
    
    st.subheader("This week's recipes:")     
           
     






