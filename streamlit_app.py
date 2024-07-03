
# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: customise Your Smothie!:cup_with_straw:")
st.write(
    """ Choose Fruits You want in your **CUSTOM SMOTHIE!**
    """
)

import streamlit as st

name_on_order = st.text_input("Name on Smothie:")
st.write("the name on your smothi is", name_on_order)

# option = st.selectbox(
#    "What is your favorite Fruit?",
#    ("banana", "Strawberries", "Peaches"))

# st.write("Your Favorite Fruit IS:", option)



session = get_active_session()
# my_dataframe = session.table("smoothies.public.fruit_options")
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list=st.multiselect(
    'Choose up Five ingredients:'
    ,my_dataframe
    ,max_selections=5
    )
if ingredients_list:
#    st.write(ingredients_list)
#    st.text(ingredients_list)
    
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

#    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+ """')"""

#    st.write(my_insert_stmt)
#    st.stop()
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered, '+ name_on_order + "!", icon="✅")





