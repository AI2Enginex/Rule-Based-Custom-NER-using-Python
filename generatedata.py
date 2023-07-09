
'''
This file contains the code for generating data which will
later be used for generating training data
the code is written for both single and multiple data Entries
'''
import json

# for creating multiple data files
def get_arr(feature_name,entity_name,name,data):
    try:
        df_ = data[data[feature_name] == entity_name]   # filtering data set value based on categories
        return df_[name].tolist()  # creating list of names associated with the category
    except Exception as e:
        return e

# iterating through list of categories and storing
# each category value into json file
def createjson(path,feature_name,name,list_name,dataset):

    for data_name in list_name:   # iterating through list of values
        
        # filtering values from dataframe and storing it in a list
        entity_data = get_arr(feature_name=feature_name,entity_name=data_name,name=name,data=dataset)
        
        # storing list data into json file
        with open(path + data_name + '.json', "w", encoding="utf-8") as f_:
            json.dump(entity_data, f_, indent=4)
        f_.close()


'''
The following block of code having same functionality as the above code, rather than list
of values before we are storing data for a single entity value
'''
def get_single_arr(feature_name,entity_name,name,data):
    try:
        df_ = data[data[feature_name] == entity_name]
        return df_[name].tolist()
    except Exception as e:
        return e
    
def create_single_json(file_name,feature_name,name,entity_name,dataset):

    entity_data = get_arr(feature_name=feature_name,entity_name=entity_name,name=name,data=dataset)
    with open(file_name, "w", encoding="utf-8") as f_:
        json.dump(entity_data, f_, indent=4)
    f_.close()