import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Parents New Healthy Diner");
streamlit.header("Breakfast Favorites");
streamlit.text("🥣Omega 3 & Blueberry Oatmeal");
streamlit.text("🥗Kale, Spinach & Rocket Smoothie");
streamlit.text("🐔Hard-Boiled Free-Range Egg");
streamlit.text("🥑🍞Avocado Toast");

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


# including a pick list so the user can select what ever they want
fruits_picked = streamlit.multiselect("pick some fruits: ", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_picked]

streamlit.dataframe(fruits_to_show)

#create a repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice)
    #streamlit.text(fruityvice_response.json()) #just writes the data back to the screen
    #now we take the json version of the data and normalize it
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

#new section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input("What Fruit Information Would You Like? ")
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    #now we want to print this output in a table
    streamlit.dataframe(back_from_function)
    #streamlit.dataframe(fruityvice_normalized)

except URLError as e:
    streamlit.error()

streamlit.header("The fruit_load_list contains:")
#snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
#add a button to load the fruit
if streamlit.button('get fruit list load'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])  
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)


streamlit.stop()
#allowing the user to add a fruit of his choice
add_my_fruit = streamlit.text_input("What Fruit Would You Like to Add?")
streamlit.write("Thanks for adding:",add_my_fruit)
my_cur.execute("insert into fruit_load_list values('from streamlit')");
