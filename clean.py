import pandas as pd

df1 = pd.read_csv('/Users/chengyin/Documents/GitHub/Your-Next-Book/books-copy.csv')
df2 = pd.read_csv('/Users/chengyin/Documents/GitHub/Your-Next-Book/books 2.csv')
# Assuming you have loaded both datasets as df1 and df2
df1['Book Name'] = df1['Book Name'].str.lower().str.replace('[^\w\s]', '')  # Normalize the 'Book Name' column
df2['title'] = df2['title'].str.lower().str.replace('[^\w\s]', '')  # Normalize the 'title' column

# Merge the two datasets on the 'Book Name' and 'title' columns
combined_df = pd.merge(df1, df2, left_on='Book Name', right_on='title', how='left')

print(combined_df.head(10))
combined_df.to_csv("datatesting.csv", index=False)