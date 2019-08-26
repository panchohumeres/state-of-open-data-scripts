
# coding: utf-8

# ## ANALYTICS DATOS.GOB.CL (Chilean Government Official Open-Data Portal)
# ### Francisco Humeres

# © 2019 Fancisco Humeres M. This work is licensed under a Creative Commons Attribution License CC-BY 4.0. All code contained herein is licensed under an MIT license

# ### **Example Script for compiling stats from an Open-Data Portal based on CKAN, and export them to Excel.**
# 
# Descriptive stats for all the resources (datasets) published in datos.gob.cl, the Chilean Government official Open Data Portal, based on open-source software [CKAN](https://en.wikipedia.org/wiki/CKAN). Datasets metadata has been extracted using [CKAN's official API, v3](https://docs.ckan.org/en/2.8/api/). 
# 
# ##### A Dashboard Demo built with KIbana, for visualizing these stats can be accesed at: http://www.estado.datos.gob.cl.s3-website-sa-east-1.amazonaws.com/.
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


# In[2]:


#TIMESTAMP OF QUERY
timestamp=strftime("%Y-%m-%d %H:%M:%S")


# In[3]:


#print timestamp #test timestamp


# In[4]:


#LIST OF RELEVANT CKAN URLS, IN THIS EXAMPLE, THE URLs corresponding to the Chilean Government Open Data Portal (datos.gob.cl)
#CKAN´s official API, version 3 https://docs.ckan.org/en/2.8/api/
url_ckan='http://datos.gob.cl/api/3/action/package_list' #url for getting the list of packages
url_package='http://datos.gob.cl/api/3/action/package_show?id=' #url for showing all packages
url_package_search='http://datos.gob.cl/api/3/action/package_search?' #url for searching all packages


# In[5]:


#List CKAN packages with their ID
ckan_packages=requests.get(url_ckan) #QUERY API
ckan_packages=ckan_packages.json() #CONVERT RESPONSE TO JSON


# In[6]:


#test number of packages (against the stats on the portal homepage for example)
#print len(ckan_packages['result'])


# In[7]:


#OBTAIN ALL THE PACKAGES METADATA
print 'obtaining packages metadata from '+url_package_search
#------------check before any rate limits or abuse policy in the portal of interest-------------------
#rows and range parameter can be changed for getting only some packages metadata
rows=str(1000) #MAX NUMBER OF RESULTS RETURNED BY CKAN'S PACKAGE SEARCH QUERY, by page
packs=[] #CONTAINER FOR RESULTS
for s in range(0,(len(ckan_packages['result'])/1000)+1): #LOOP OVER ALL THE LIST OF PACKAGES
    start=str(s*int(rows)) #PAGINATION START POINT
    packages=requests.get(url_package_search+'rows='+rows+'&'+'start='+start)
    packages=packages.json()
    packs.extend(packages['result']['results'])  
print 'finished with obtaining package metadata from '+url_package_search

# In[8]:


#len(packs) #TEST NUMBER OF PACKAGES RETURNED (NOT NECESSARILY WILL BE THE SAME AS THOSE RETURNED BY THE PACKAGE LIST)


# In[9]:


#EXTRACT FIELDS OF INTEREST FROM THE PACKAGES
#in this example (containers for the data):
maintainer_mails=[] #mantainaer emails
author_mails=[] #author emails
creado=[] #created time
titulo=[] #package title
inst=[] #institution
author=[] #package author
mantainer=[] #package mantainer
modified=[] #package modification date
org_id=[] #organization (institution) id
for p in packs:
    maintainer_mails.append(p["maintainer_email"])
    titulo.append(p['title'])
    if 'organization' in p.keys(): #if organization info. exists
        if p['organization']!=None:
            inst.append(p['organization']['title']) #if organization title info. exists, include it
            org_id.append(p['organization']['id'])
        else:
            inst.append(None)
    author_mails.append(p['author_email'])
    author.append(p['author'])
    mantainer.append(p['maintainer'])
    creado.append(p["metadata_created"])
    modified.append(p['metadata_modified'])
    
    


# In[10]:


#CONVERT PACKAGE METADATA TO PANDAS DATAFRAME
packsDF=[titulo,inst,creado,modified,author,author_mails,mantainer,maintainer_mails,org_id]
packsDF=pd.DataFrame(packsDF).T
packsDF.columns=['Tit.','Inst.','Creado','Modificado','Autor','E-mail Autor','Mantenedor','E-mail Mantenedor','InstID']

packsDF['Modificado']=pd.to_datetime(packsDF['Modificado']) #CONVERT MODIFIED DATE TO DATETIME FORMAT
packsDF['Creado']=pd.to_datetime(packsDF['Creado']) #CONVERT CREATED DATE TO DATETIME FORMAT
#EXTRA FIELDS WITH LAST MODIFIED DATE INFORMATION
packsDF['Fecha Mod.']=packsDF['Modificado'].dt.date #DATE
packsDF['Year Mod.']=packsDF['Modificado'].dt.year #YEAR
packsDF['Month Mod.']=packsDF['Modificado'].dt.month #MONTH
packsDF['Day Mod.']=packsDF['Modificado'].dt.day #DAY OF THE MONTH

packsDF['Inst.']=packsDF['Inst.'].fillna("") #cambiar los NaNs de institucion para poder hacer slices


# In[11]:


#SAMPLE SLICE, BY ORGANIZATIONS THAT CONTAIN THE WORD "Planeamiento" (Planning)
packsDF[packsDF['Inst.'].str.contains('Planeamiento')]


# In[12]:


#EXTRACT RESOURCES WITHIN PACKAGES, WITH FIELDS OF INTEREST, AND CONVERT THEM TO PANDAS DATAFRAME
recursos=[] #resources container
for p in packs: #loop over the packages
    for r in p['resources']:
        d={} #container for values
        d['pack_revision_id']=p['revision_id']
        d['pack_title']=p['title'] #title of containing package
        d['pack_name']=p['name']
        d['name']=r['name']
        d['timestamp']=r['last_modified'] #last modification
        d['formato_tipeado']=r['format'] #typed format (as reported by the publisher)
        d['extension']=r['url'].split('.')[-1]
        if ('/' in d['extension']) or ('?' in d['extension']) or ('=' in d['extension']): #if extension is a URL
            d['extension']='url' #add extension
        d['desc.']=r['description']
        d['url']=r['url']
        d['size']=r['size']
        d['mimetype']=r['mimetype']
        d['pack_name_url']='http://datos.gob.cl/dataset/'+p['name'] #url of the package (named version)
        d['pack_url']='http://datos.gob.cl/dataset/'+p['id'] #package url
        d['resource_url']=d['pack_url']+'/resource/'+r['id'] #resource url
        d['resource_name_url']=d['pack_name_url']+'/resource/'+r['id'] #url of the resource (named version)
        if 'organization' in p.keys(): #if there exists info of the organization
            if p['organization']!=None:
                d['inst.']=p['organization']['title'] #if there is organization title info., add it
            else:
                d['inst.']=None
        else:
            d['inst.']=None
        recursos.append(d)
recursosDF=pd.DataFrame(recursos) #convert resources list to pandas dataframe
fecha=pd.to_datetime(recursosDF['timestamp']) #strip hour from timestamp
#decompose resource's datetime data
recursosDF['Fecha Carga']=fecha.dt.date #date
recursosDF['Year']=fecha.dt.year #year
recursosDF['Month']=fecha.dt.month #month
recursosDF['Day']=fecha.dt.day #day of the month
recursosDF=recursosDF.drop_duplicates() #drop duplicates
recursosDF['idx']=recursosDF.index #add index column to df


# In[13]:


#recursosDF.shape #test number of resources


# In[14]:


#print len(recursosDF['inst.'].unique()) #test number of organizations


# In[15]:


#CROSSTAB OF RESOURCES BY INSTITUTION
recursosxinst=recursosDF.fillna('None').groupby(recursosDF['inst.'].fillna('None'))['inst.'].count() #recursos por institución


# In[16]:


#CROSSTAB OF RESOURCES BY INSTITUTION AND TYPED FORMAT (AS REPORTED BY PUBLISHER)
formatosxinst=pd.crosstab(recursosDF['inst.'],recursosDF['formato_tipeado'],margins=True, margins_name="Total",dropna=False)


# In[17]:


#CROSSTAB OF RESOURCES BY INSTITUTION AND FORMAT (EXTRACTED FROM FILE EXTENSION)
extensionxinst=pd.crosstab(recursosDF['inst.'],recursosDF['extension'],margins=True, margins_name="Total",dropna=False)


# In[18]:


#CROSSTAB OF RESOURCES BY INSTITUTION AND YEAR OF PUBLICATION
cargasxanoxinst=pd.crosstab(recursosDF['inst.'],recursosDF['Year'],margins=True, margins_name="Total",dropna=False)


# In[19]:


#SAVE TO EXCEL
name='Cargas_historicas_CKAN_'+str(timestamp.replace(' ','_'))+'.xlsx'

print 'saving data to file '+name
with pd.ExcelWriter(name) as writer:  # doctest: +SKIP
    recursosDF.to_excel(writer, sheet_name='Data CKAN_Recursos',encoding='utf-8') #raw resources data
    packsDF.to_excel(writer, sheet_name='Data CKAN_Paquetes',encoding='utf-8') #raw packages data
    cargasxanoxinst.to_excel(writer, sheet_name='Datasets x Inst x Year',encoding='utf-8') 
    extensionxinst.to_excel(writer, sheet_name='Datasets x Inst x Formato',encoding='utf-8')
    formatosxinst.to_excel(writer, sheet_name='Datasets x Inst x Formato Tip.',encoding='utf-8')
print 'finished saving data to excel file'
