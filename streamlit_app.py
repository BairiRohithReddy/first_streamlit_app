import streamlit
import pandas as pd

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

#new section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
import requests

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response.json())
