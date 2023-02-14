import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv('ND_Crawl.csv')



def Data_Plot(nodes, edges):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    plt.figure(figsize=(15, 15))
    plt.title('Active Businesses Starting with X')


for i, row in df.iterrows():
    temp = df.at[i,'TITLE']
    temp1 = temp.replace('   ','*')
    temp2 = temp1.replace('|','')
    temp3 = temp2.replace(' ','')
    temp4 = temp3.replace('*',' ')
    df.at[i,'TITLE'] = temp4


df_new = df[['TITLE','Commercial Registered Agent','Registered Agent','Owner Name']].copy()
df_new.to_csv('Useful_4_columns.csv',index=False) 
print(df_new.head())