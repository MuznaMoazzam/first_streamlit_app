import streamlit
streamlit.title('My Parents New Healthy Diner')
streamlit.header ('Breakfast Favourites')
streamlit.text(' 🥣 Omega 3 and blueberry oatmeal')
streamlit.text('🥗 Kale,spinach and rocket smoothie')
streamlit.text('🐔 Hard-Boiled Free range egg')
streamlit.text('🥑🍞 Avacado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
import pandas
my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fryit_list)
