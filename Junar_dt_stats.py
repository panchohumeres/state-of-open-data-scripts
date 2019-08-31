
# coding: utf-8

# ## DATASETS STATS FOR BETA.DATOS.GOB.CL (OPEN-DATA PORTAL BASED ON JUNAR)
# ### F.Humeres

# © 2019 Fancisco Humeres M. This work is licensed under a Creative Commons Attribution License CC-BY 4.0. All code contained herein is licensed under an MIT license

# ### **Example Script for compiling stats from an Open-Data Portal based on Junar, and export them to Excel.**
# 
# Descriptive stats for all the datasets ("Conjuntos de Datos") published in [beta.datos.gob.cl](https://beta.datos.gob.cl), the future official Open Data Portal of the Chilean government, based on the SaaS platform [Junar](http://www.junar.com/). Resources metadata has been extracted from Junar's API.
# 
# ** NOTE: FIGURES MAY DIFFER SLIGHTLY FROM THE ONES REPORTED IN BETA.DATOS.GOB.CL. FOR OFFICIAL FIGURES, PLEASE REFER TO [beta.datos.gob.cl](https://beta.datos.gob.cl). **
# 
# ##### A Dashboard Demo built with KIbana, for visualizing these stats can be accesed at: https://d3bhn81c8dm26x.cloudfront.net//.
# 
# Demo made by [Francisco Humeres M.](https://www.linkedin.com/in/fhumeres/). More of my work can be seen in my [Portfolio](https://fjhumeres.myportfolio.com/). You can contact me at fhumeres[at]alum[dot]mit[dot]edu.

# In[6]:


import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings; warnings.simplefilter('ignore')
import IPython.core.display as di
from time import gmtime, strftime


# In[7]:


#TIMESTAMP OF QUERY
timestamp=strftime("%Y-%m-%d %H:%M:%S")


# In[8]:


#RELEVANT URLS, PLEASE CONTACT JUNAR FOR ACCESS TOKENS
url_datasets='https://api.beta.datos.gob.cl/api/v2/datasets/?auth_key=auth_key&format=json'
url_vistas='https://api.beta.datos.gob.cl/api/v2/datastreams/?auth_key=auth_key&format=json'
url_viz='https://api.beta.datos.gob.cl/api/v2/visualizations/?auth_key=auth_key&format=json'
url_colecciones='https://api.beta.datos.gob.cl/api/v2/dashboards/?auth_key=auth_key&format=json'
url_dgd_users='https://api.beta.datos.gob.cl/api/v2/account/users.json/?auth_key=auth_key' #usuarios DGD
url_usuarios='https://api.beta.datos.gob.cl/api/v2/account/children/users.json/?auth_key=auth_key' #url otros usuarios


# In[9]:


#USERS LIST
#In the case of the Chilean government future open-data portal (beta.datos.gob.cl), will operate a "Federated" model. 
#DGD (E-Government division) will operate main portal...
#while the data from portals of other organizations ("Fedarated") within the chilean state that use Junar, will be synced to the main portal
print "obtaining users list"
#dgd (E-GOVERNMENT DIVISION) USERS
dgd_users=requests.get(url_dgd_users) #consultar api
dgd_users=dgd_users.json() #convertir respuesta a json
#OTHER ORGANIZATION'S USERS ("FEDERATED" USERS)
fed_users=requests.get(url_usuarios) #consultar api
fed_users=fed_users.json() #convertir respuesta a json


# In[10]:


#GENERAR DF CON INFO DE USUARIOS
users=[]
#GET METADATA OF OTHER ORGANIZATION'S USERS ("FEDERATED" USERS)
for inst in fed_users:
    u=pd.DataFrame(inst['users'])
    u['Inst']=inst['account_name']
    users.append(u)
#get metadata of DGD users
u=pd.DataFrame(dgd_users)
u['Inst']='DGD'
users.append(u)
#consolidated metadata for users (both DGD and "Federated")
users=pd.concat(users,ignore_index=True)


# In[11]:


#Mapping of users with their state organizations (institutions)
user_mapping=dict(zip(users.nick,users.Inst))


# In[12]:


#DATASETS
print "obtaining datasets metadata"
datasets=requests.get(url_datasets) #query datasets url
datasets=datasets.json() #convert response to json
datasets=pd.DataFrame(datasets) #convertir response to pandas DataFrame
#decompose date of publication of the datasets
datasets['fecha']=pd.to_datetime(datasets['timestamp'],unit='ms') #date timestamp
datasets['dia']=datasets['fecha'].dt.date #day of the month
datasets['year']=datasets['fecha'].dt.year #year
datasets['mes']=datasets['fecha'].dt.month #month
datasets['inst']=datasets['user'].map(user_mapping) #organization mapping

#datasets.to_excel('Carga_historica_JUNAR.xlsx',encoding='utf-8')


# In[13]:


#count of Datasets sources (by Organization)
fuentes_d=pd.DataFrame(datasets.groupby(['inst'])['inst'].count().sort_values(ascending=False))
fuentes_d.columns=['Nº']
fuentes_d.index.names=['Fuente']


# In[14]:


#datasets segpres
#segpres=datasets[datasets['inst'].str.contains('Subsecretaria General de la Presidencia')]
#segpres.to_excel('Carga_historica_JUNAR_segpres.xlsx',encoding='utf-8')


# ### Total Number of Datasets by Organization

# In[15]:

#check sources df
#fuentes_d.head(20)


# In[16]:


# Organizations count
#pd.DataFrame.from_dict(user_mapping,orient='index')[0].unique().shape


# In[17]:


#CROSSTAB OF DATASETS PUBLISHED BY ORGANIZATION AND BY MONTH (WITHIN A GIVEN YEAR)
datasetsxinstxmes=pd.crosstab(datasets['inst'],[datasets['year'],datasets['mes']],margins=True, margins_name="Total",dropna=False)


# In[20]:

#check crosstab
#datasetsxinstxmes.head(20)


# In[19]:


#SAVE TO EXCEL
print "saving to excel"
name='Cargas_historicas_Junar_'+str(timestamp.replace(' ','_'))+'.xlsx'
print "file: "+name

with pd.ExcelWriter(name, engine='openpyxl') as writer:  # doctest: +SKIP
    fuentes_d.to_excel(writer, sheet_name='Datasets x Inst',encoding='utf-8') #DATASETS BY ORGANIZATION SHEET
    datasetsxinstxmes.to_excel(writer, sheet_name='Datasets x Inst x Mes',encoding='utf-8') #DATASETS BY ORGANIZATION BY MONTH SHEET

