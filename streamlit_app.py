import streamlit, pandas as pd, requests, snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
display_fruits = my_fruit_list.loc[fruits]
# Display the table on the page.
streamlit.dataframe(display_fruits)

def get_fruityvice_data(fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
  streamlit.error()

if streamlit.button("Get Fruit Load List"):
    my_cur = snowflake.connector.connect(**streamlit.secrets["snowflake"]).cursor()
    my_data_rows = my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST").fetchall()
    streamlit.dataframe(my_data_rows)

streamlit.stop()
new_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.text("Thanks for adding " + new_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
