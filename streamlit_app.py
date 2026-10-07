# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie
  """
)

import streamlit as st

Name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", Name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe, max_selections=5
)
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen 

    #st.write(ingredients_list)

    insert_stmt = f"INSERT INTO smoothies.public.orders (ingredients, Name_on_order, order_uid) SELECT '{ingredients_string}', '{Name_on_order}', UUID_STRING()"

    st.write(insert_stmt)
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {Name_on_order}!', icon="✅")
