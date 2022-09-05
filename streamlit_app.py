
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


def get_fruits_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
        my_data_row = my_cur.fetchall()
        return my_data_row


def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get(
        "https://fruityvice.com/api/fruit/"+this_fruit_choice)
    fruityvice_response_jsonnormalized = pandas.json_normalize(
        fruityvice_response.json())

    return fruityvice_response_jsonnormalized


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
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input(
        'What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        fruityvice_response_jsonnormalized = get_fruityvice_data(
            this_fruit_choice=fruit_choice)
        streamlit.dataframe(fruityvice_response_jsonnormalized)
except URLError as e:
    streamlit.error()

if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.text("The fruit load list contains:")
    my_data_row = get_fruits_load_list()
    streamlit.dataframe(my_data_row)

add_my_fruit = streamlit.text_input(
        'What fruit would you like to add?', 'jackfruit')
streamlit.text("Thanks for adding "+add_my_fruit)
