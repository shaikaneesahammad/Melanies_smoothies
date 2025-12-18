 # Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas as pd
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
  "Choose the fruits you want in your custom smoothie!"
)

#Adding name in smoothie:
name_on_order = st.text_input('Name on Smoothie')
st.write ('Name on your smoothie:',name_on_order)

#Selecting ingredients
cnx =st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
#st.dataframe(data=my_dataframe, use_container_width=True);
ingredients_list = st.multiselect ( 'Choose up to 5 ingredients :',my_dataframe,max_selections = 5)




#if ingredients list present then save it into table.
if ingredients_list:
 #   st.write(ingredients_list)
 #   st.text(ingredients_list)
    ingredients_string = ''
    
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit+' ';
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+each_fruit)
        sf_df = st.dataframe(smoothiefroot_response.json(),use_container_width = True)
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', each_fruit,' is ', search_on, '.')

    #st.write('Ingredient list is',ingredients_string);
          

    #my_insert_stmt = """insert into smoothies.public.orders(ingredients) values ('"""+ingredients_string+"""')""";
    #st.write(my_insert_stmt);
    #my_insert_stmt = """insert into smoothies.public.order(ingredients,name_on_order) values('"""+ingredients_string + ""","""+ name_on_order +"""')"""
    
    my_insert_stmt = """insert into smoothies.public.orders(ingredients,name_on_order) values('""" + ingredients_string + """' ,'"""+ name_on_order + """')"""
    #st.write(my_insert_stmt);

    time_to_insert = st.button('Submit order')
    #st.write(time_to_insert) #this is boolean

    if time_to_insert:
      RESULT = session.sql(my_insert_stmt).collect()
      #st.write (RESULT)
      st.success("Your smoothie is ordered!",icon = "✅");
      




    
    
