import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header ('Breakfast Favourites')
streamlit.text(' 🥣 Omega 3 and blueberry oatmeal')
streamlit.text('🥗 Kale,spinach and rocket smoothie')
streamlit.text('🐔 Hard-Boiled Free range egg')
streamlit.text('🥑🍞 Avacado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


#Create a repeatable code block (called the Function)t
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return (fruityvice_normalized)
    
    
#New section to display Fruity Vice API Response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get the information.")
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
    streamlit.error()

streamlit.header("View our Fruit list.Add your favourites!")
#Snowflake-related functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur :
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

#Add button to load the fruit
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows=get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows) 

#Allow the end user to add the fruit to the list 
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur :
      my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +"')")
      return "Thanks for adding " + new_fruit
        
add_my_fruit=streamlit.text_input('what fruit would you like to add ?')
if streamlit.button('Add a fruit to the list'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_function = insert_row_snowflake(add_my_fruit)
      my_cnx.close()
      streamlit.text(back_from_function)


#don't run anything past here until we troubleshoot
streamlit.stop();
my_cnx=snowflake.connector.connect(**streamlit.secrets["Snowflake"])
my_cur=my_cnx.cursor()
my_cur.execute("select * from fruit_load_list ")
my_data_rows=my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe=(my_data_rows)
