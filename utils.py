import chardet
import io, os
import pandas as pd

def get_null_cols(df):
  return [col for col in df.columns if df[col].isnull().any()]

def drop_null_cols(df):
  cols_with_missing = get_null_cols(df)
  return df.drop(cols_with_missing, axis=1)  #it returns a copy of df without missing cols

def get_cols_cardinality(df):
  # "Cardinality" means the number of unique values in a column
  # Select categorical columns with relatively low cardinality (convenient but arbitrary)
  max_categories_to_check = 10
  low_cardinality_cols = [cname for cname in df.columns if df[cname].nunique() < max_categories_to_check and 
                          df[cname].dtype == "object"]
  return low_cardinality_cols

def get_numerical_col(df):
  # Select numerical columns
  numerical_cols = [cname for cname in df.columns if df[cname].dtype in ['int64', 'float64']]
  return numerical_cols

def get_categorical_variables(df):
  object_cols = [col for col in df.columns if df[col].dtype == "object"]
  # s = (df.dtypes == 'object')
  # object_cols = list(s[s].index)
  return object_cols

def get_unique_entries_categorical_cols(df):
  # Get number of unique entries in each column with categorical data
  object_cols = get_categorical_variables(df)
  object_nunique = list(map(lambda col: df[col].nunique(), object_cols))
  d = dict(zip(object_cols, object_nunique))

  # Print number of unique entries by column, in ascending order
  return sorted(d.items(), key=lambda x: x[1])

# In the case that the validation data contains values that don't also appear in the training data, 
# the encoder will throw an error, because these values won't have an integer assigned to them.
def remove_categorical_cols_not_matching(X_train, X_valid):
  # All categorical columns
  object_cols = get_categorical_variables(X_train)

  # Columns that can be safely label encoded
  good_label_cols = [col for col in object_cols if 
                    set(X_train[col]) == set(X_valid[col])]
          
  # Problematic columns that will be dropped from the dataset
  bad_label_cols = list(set(object_cols)-set(good_label_cols))

  print('Categorical columns that will be label encoded:', good_label_cols)
  print('\nCategorical columns that will be dropped from the dataset:', bad_label_cols)
  return good_label_cols

def check(file_url):
  with open(file_url, 'rb') as rawdata:
      result = chardet.detect(rawdata.read(100000))
  st.write(result)

def load_multiple_csv_files(files_list):
  data = pd.DataFrame()
  # files_2018 = "/content/drive/My Drive/datasets/2018/" + pd.DataFrame(os.listdir("/content/drive/My Drive/datasets/2018"))
  # files_2019 = "/content/drive/My Drive/datasets/2019/" + pd.DataFrame(os.listdir("/content/drive/My Drive/datasets/2019"))
  # files_to_read = pd.concat([files_2018,files_2019,pd.DataFrame(["/content/drive/My Drive/datasets/registro-obsequios-funcionarios-publicos-20201009.csv"])]).reset_index()
  for idx, filename in files_list.values:
      print("Loading: "+filename)
      if filename.endswith("csv"):
          data = pd.concat([data, pd.read_csv(filename)], axis=0)