import streamlit
import pandas
import requests
streamlit.title("My Parents New Healthy Dinner")
streamlit.header("Breakfast Menu")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text(" 🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruits_list = pandas.read_csv(
    "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruits_list = my_fruits_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(
    my_fruits_list.index), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruits_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)
fruit_choice = streamlit.text_input(
    'What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered ', fruit_choice)
streamlit.header("Fruityvice Fruit Advice!")
fruityvice_response = requests.get(
    "https://fruityvice.com/api/fruit/"+fruit_choice)
fruityvice_response_jsonnormalized = pandas.json_normalize(
    fruityvice_response.json())
streamlit.dataframe(fruityvice_response_jsonnormalized)
