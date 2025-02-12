import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: customise Your Smothie!:cup_with_straw:")
st.write(
    """ Choose Fruits You want in your **CUSTOM SMOTHIE!**
    """
)

name_on_order = st.text_input("Name on Smothie:")
st.write("the name on your smothi is", name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list=st.multiselect(
    'Choose up Five ingredients:'
    ,my_dataframe
    ,max_selections=5
    )
if ingredients_list:
    
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+ """')"""

    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered, '+ name_on_order + "!", icon="✅")





