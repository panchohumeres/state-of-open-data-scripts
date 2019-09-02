
# coding: utf-8

# ## ANALYTICS BETA.DATOS.GOB.CL
# ### Francisco Humeres

# © 2019 Fancisco Humeres M. This work is licensed under a Creative Commons Attribution License CC-BY 4.0. All code contained herein is licensed under an MIT license

# ### **Stats from an Open-Data Portal based on Junar (beta.datos.gob.cl).**
# 
# Descriptive stats for all the resources ("Recursos") published in [beta.datos.gob.cl](https://beta.datos.gob.cl), the future official Open Data Portal of the Chilean government, based on the SaaS platform [Junar](http://www.junar.com/). Resources metadata has been extracted from Junar's API.
# 
# ** NOTE: FIGURES MAY DIFFER SLIGHTLY FROM THE ONES REPORTED IN BETA.DATOS.GOB.CL. FOR OFFICIAL FIGURES, PLEASE REFER TO [beta.datos.gob.cl](https://beta.datos.gob.cl). **
# 
# ** Resources Dictionary: **
# * "Datasets"=Datasets (Archives)
# * "Vistas"=Data Views
# * "Visualizaciones"=Visualizations
# * "Colecciones"=Collections (Reports)    
#     
# ##### A Dashboard Demo built with KIbana, for visualizing these stats can be accesed at: https://d3bhn81c8dm26x.cloudfront.net//.
# 
# Demo made by [Francisco Humeres M.](https://www.linkedin.com/in/fhumeres/). More of my work can be seen in my [Portfolio](https://fjhumeres.myportfolio.com/). You can contact me at fhumeres[at]alum[dot]mit[dot]edu.

# In[1]:


import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings; warnings.simplefilter('ignore')
import IPython.core.display as di
from time import gmtime, strftime
import seaborn as sns
import math


# In[2]:


#TIMESTAMP OF QUERY
timestamp=strftime("%Y-%m-%d %H:%M:%S")


# ### Timestamp

# In[3]:


timestamp


# In[4]:


#RELEVANT URLS, PLEASE CONTACT JUNAR FOR ACCESS TOKENS
url_datasets='https://api.beta.datos.gob.cl/api/v2/datasets/?auth_key=auth_key'
url_vistas='https://api.beta.datos.gob.cl/api/v2/datastreams/?auth_key=auth_key&format=json'
url_viz='https://api.beta.datos.gob.cl/api/v2/visualizations/?auth_key=auth_key&format=json'
url_colecciones='https://api.beta.datos.gob.cl/api/v2/dashboards/?auth_key=auth_key&format=json'
url_dgd_users='https://api.beta.datos.gob.cl/api/v2/account/users.json/?auth_key=auth_key' #usuarios DGD
url_usuarios='https://api.beta.datos.gob.cl/api/v2/account/children/users.json/?auth_key=auth_key' #url otros usuarios


# In[5]:


#USERS LIST
#In the case of the Chilean government future open-data portal (beta.datos.gob.cl), will operate a "Federated" model. 
#DGD (E-Government division) will operate main portal...
#while the data from portals of other organizations ("Fedarated") within the chilean state that use Junar, will be synced to the main portal
#dgd (E-GOVERNMENT DIVISION) USERS
dgd_users=requests.get(url_dgd_users) #consultar api
dgd_users=dgd_users.json() #convertir respuesta a json
#OTHER ORGANIZATION'S USERS ("FEDERATED" USERS)
fed_users=requests.get(url_usuarios) #consultar api
fed_users=fed_users.json() #convertir respuesta a json


# In[6]:


#GENERATE PANDAS DF WITH USER'S METADATA
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


# In[7]:


#Mapping of users with their state organizations (institutions)
user_mapping=dict(zip(users.nick,users.Inst))


# In[8]:


#DATASETS
datasets=requests.get(url_datasets) #query datasets url
datasets=datasets.json() #convert response to json
datasets=pd.DataFrame(datasets) #converting response to pandas DataFrame
#decompose date of publication of the datasets
datasets['fecha']=pd.to_datetime(datasets['timestamp'],unit='ms')#date timestamp
datasets['dia']=datasets['fecha'].dt.date#day of the month
datasets['year']=datasets['fecha'].dt.year#year
datasets['mes']=datasets['fecha'].dt.month#month
datasets['inst']=datasets['user'].map(user_mapping) #organization mapping

#datasets.to_excel('Carga_historica_JUNAR.xlsx',encoding='utf-8')


# In[9]:


#VISTAS=DATAVIEWS
#SAME WORKFLOW AS OUTLINED FOR DATASETS
vistas=requests.get(url_vistas) #consultar api
vistas=vistas.json() #convertir respuesta a json
vistas=pd.DataFrame(vistas) #convertir respuesta a pandas DF
#fechas en que fueron agregados vistas
vistas['fecha']=pd.to_datetime(datasets['timestamp'],unit='ms')
vistas['dia']=vistas['fecha'].dt.date
vistas['year']=vistas['fecha'].dt.year
vistas['mes']=vistas['fecha'].dt.month
vistas['inst']=vistas['user'].map(user_mapping) #mapeo de la institucion


# In[10]:


#VIZUALIZACIONES=VIZUALIZATIONS
#SAME WORKFLOW AS OUTLINED FOR DATASETS
viz=requests.get(url_viz) #consultar api
viz=viz.json() #convertir respuesta a json
viz=pd.DataFrame(viz) #convertir respuesta a pandas DF
#fechas en que fueron agregados vizualizaciones
viz['fecha']=pd.to_datetime(datasets['timestamp'],unit='ms')
viz['dia']=viz['fecha'].dt.date
viz['year']=viz['fecha'].dt.year
viz['mes']=viz['fecha'].dt.month
viz['inst']=viz['user'].map(user_mapping) #mapeo de la institucion


# In[11]:


#COLECCIONES=COLLECTIONS
#SAME WORKFLOW AS OUTLINED FOR DATASETS
col=requests.get(url_colecciones) #consultar api
col=col.json() #convertir respuesta a json
col=pd.DataFrame(col) #convertir respuesta a pandas DF
#fechas en que fueron agregados colecciones
col['fecha']=pd.to_datetime(datasets['timestamp'],unit='ms')
col['dia']=col['fecha'].dt.date
col['year']=col['fecha'].dt.year
col['mes']=col['fecha'].dt.month
col['inst']=col['user'].map(user_mapping) #mapeo de la institucion


# In[12]:


#Datasets count by organization (institution)
fuentes_d=pd.DataFrame(datasets.groupby(['inst'])['inst'].count().sort_values(ascending=False))
fuentes_d.columns=['Nº']
fuentes_d.index.names=['Fuente']


# In[13]:


#Data Views count by organization (institution)
fuentes_v=pd.DataFrame(vistas.groupby(['inst'])['inst'].count().sort_values(ascending=False))
fuentes_v.columns=['Nº']
fuentes_v.index.names=['Fuente']


# In[14]:


#Vizualizations count by organization (institution)
fuentes_viz=pd.DataFrame(viz.groupby(['inst'])['inst'].count().sort_values(ascending=False))
fuentes_viz.columns=['Nº']
fuentes_viz.index.names=['Fuente']


# In[15]:


#Collections count by organization (institution)
fuentes_c=pd.DataFrame(col.groupby(['inst'])['inst'].count().sort_values(ascending=False))
fuentes_c.columns=['Nº']
fuentes_c.index.names=['Fuente']


# In[16]:


#Pandas DF of resources count by type and organization (institution)
fuentes=pd.concat([fuentes_d,fuentes_v,fuentes_viz,fuentes_c],axis=1,keys=['Datasets', 'Vistas','Visualizaciones','Colecciones'])
fuentes.columns=fuentes.columns.droplevel(1)
fuentes.ix['Suma']=fuentes.sum()
fuentes['Suma']=fuentes.sum(axis=1)


# In[17]:


#CROSSTAB OF RESOURCES BY INSTITUTION AND DATE
recursoxdia=pd.concat([datasets['dia'],vistas['dia'],viz['dia'],col['dia']],keys=['datasets','vistas','vizualizaciones','colecciones'])
recursoxdia=recursoxdia.reset_index(level=0)
recursoxdia.columns=['Tipo Recurso','dia']
recursoxdia=pd.crosstab(recursoxdia['Tipo Recurso'],recursoxdia['dia'],margins=True, margins_name="Total",dropna=False)


# In[18]:


#CROSSTAB OF RESOURCES BY INSTITUTION AND MONTH
recursoxmes=pd.concat([datasets[['year','mes']],vistas[['year','mes']],viz[['year','mes']],col[['year','mes']]],keys=['datasets','vistas','vizualizaciones','colecciones'])
recursoxmes=recursoxmes.reset_index(level=0)
recursoxmes.columns=['Tipo Recurso','year','mes']
recursoxmes=pd.crosstab(recursoxmes['Tipo Recurso'],[recursoxmes['year'],recursoxmes['mes']],margins=True, margins_name="Total",dropna=False)


# In[19]:


#CROSSTAB OF RESOURCES BY INSTITUTION AND YEAR
recursosxano=recursoxmes.T.groupby('year').sum().drop('Total',axis=1).drop('Total')


# In[20]:


#CROSSTAB OF DATASETS PUBLISHED BY ORGANIZATION AND BY MONTH (WITHIN A GIVEN YEAR)
datasetsxinstxmes=pd.crosstab(datasets['inst'],[datasets['year'],datasets['mes']],margins=True, margins_name="Total",dropna=False)


# In[21]:


#CROSSTAB OF VIEWS PUBLISHED BY ORGANIZATION AND BY MONTH (WITHIN A GIVEN YEAR)
vistasxinstxmes=pd.crosstab(vistas['inst'],[vistas['year'],vistas['mes']],margins=True, margins_name="Total",dropna=False)


# In[22]:


#CROSSTAB OF VIZUALIZATIONS PUBLISHED BY ORGANIZATION AND BY MONTH (WITHIN A GIVEN YEAR)
vizxinstxmes=pd.crosstab(viz['inst'],[viz['year'],viz['mes']],margins=True, margins_name="Total",dropna=False)


# In[23]:


#CROSSTAB OF COLLECTIONS PUBLISHED BY ORGANIZATION AND BY MONTH (WITHIN A GIVEN YEAR)
colsxinstxmes=pd.crosstab(col['inst'],[col['year'],col['mes']],margins=True, margins_name="Total",dropna=False)


# ### Total de Recursos por Tipo

# In[24]:


#TABLE OF TOTAL RESOURCES BY TYPE
pd.DataFrame(fuentes.ix['Suma'])


# In[25]:


#PIE-CHART OF TOTAL RESOURCES BY TYPE
fuentes.loc['Suma'][['Datasets','Vistas','Visualizaciones','Colecciones']].plot(kind='pie')


# ### Carga Histórica de Recursos por Tipo

# In[26]:


#HISTORICAL RECORD OF RESOURCE PUBLISHING BY TYPE AND DATE (CUMULATIVE SUM)
recursoxdia.cumsum(axis=1).T.drop('Total',axis=1).drop('Total').plot(kind='area',stacked='True')


# ### Carga Histórica de Datasets (Acumulado)

# In[27]:


#HISTORICAL RECORD OF DATASETS PUBLISHING BY DATE (CUMULATIVE SUM)
datasets.groupby(['fecha'])['fecha'].count().cumsum().plot(kind='area')


# ### Carga Anual de Recursos por Tipo

# In[28]:


#NUMBER OF RESOURCES PUBLISHED BY YEAR AND TYPE
recursosxano.plot(kind='bar',stacked='True')


# ### Carga Mensual de Recursos por Tipo

# In[29]:


#NUMBER OF RESOURCES PUBLISHED BY MONTH AND TYPE
#chart code obtained from stack overflow answer: https://stackoverflow.com/a/51824748
n_subplots = len(recursoxmes.drop('Total',axis=1).drop('Total').T.index.levels[0])-1
fig, axes = plt.subplots(nrows=1, ncols=n_subplots, sharey=True, figsize=(14, 8)) 
graph = dict(zip(recursoxmes.drop('Total',axis=1).drop('Total').T.index.levels[0], axes))
plots = list(map(lambda x: recursoxmes.drop('Total',axis=1).drop('Total').T.xs(x).plot(kind='bar', stacked='True', ax=graph[x], legend=False).set_xlabel(x, weight='bold'), graph))
plt.legend()
plt.show()


# ### Total de Datasets por Institución (Top 20)

# In[30]:


#TOTAL NUMBER OF DATASETS PUBLISHED BY TOP 20 ORGANIZATIONS
print fuentes_d.head(20)


# In[31]:


datasets.groupby(['inst'])['inst'].count().sort_values(ascending=False).head(20).plot(kind='bar')
plt.show()

# ### Datasets cargados por Mes y por Institución (Top 20)

# In[32]:


#TOTAL NUMBER OF DATASETS PUBLISHED BY TOP 20 ORGANIZATIONS, BY MONTH (HEATMAP)
sns.heatmap(datasetsxinstxmes.replace({0:np.nan}).sort_values(by='Total',ascending=False).drop('Total',axis=1).drop('Total').head(20))
plt.show()

# ### Total de Vistas por Institución (Top 20)

# In[33]:


#TOTAL NUMBER OF DATA VIEWS PUBLISHED BY TOP 20 ORGANIZATIONS
print fuentes_v.head(20)


# In[34]:


vistas.groupby(['inst'])['inst'].count().sort_values(ascending=False).head(20).plot(kind='bar')
plt.show()

# ### Vistas cargadas por Mes y por Institución (Top 20)

# In[35]:


#TOTAL NUMBER OF DATA VIEWS PUBLISHED BY TOP 20 ORGANIZATIONS, BY MONTH (HEATMAP)
sns.heatmap(vistasxinstxmes.replace({0:np.nan}).sort_values(by='Total',ascending=False).drop('Total',axis=1).drop('Total').head(20))
plt.show()

# ### Total de Vizualizaciones por Institución

# In[36]:


#TOTAL NUMBER OF VISUALIZATIONS PUBLISHED BY ORGANIZATION
print fuentes_viz.head(20)


# In[37]:


viz.groupby(['inst'])['inst'].count().sort_values(ascending=False).head(20).plot(kind='bar')
plt.show()

# ### Vizualizaciones cargadas por Mes y por Institución

# In[38]:


#TOTAL NUMBER OF VISUALIZATIONS PUBLISHED BY ORGANIZATION, BY MONTH (HEATMAP)
sns.heatmap(vizxinstxmes.replace({0:np.nan}).sort_values(by='Total',ascending=False).drop('Total',axis=1).drop('Total').head(20))
plt.show()

# ### Total de Colecciones por Institución

# In[39]:


#TOTAL NUMBER OF COLECCTIONS PUBLISHED BY ORGANIZATION
print fuentes_c.head(20)


# In[40]:


col.groupby(['inst'])['inst'].count().sort_values(ascending=False).head(20).plot(kind='bar')
plt.show()

# ### Colecciones cargadas por Mes y por Institución

# In[41]:


#TOTAL NUMBER OF COLLECTIONS PUBLISHED BY ORGANIZATION, BY MONTH (HEATMAP)
sns.heatmap(colsxinstxmes.replace({0:np.nan}).sort_values(by='Total',ascending=False).drop('Total',axis=1).drop('Total').head(20))
plt.show()

