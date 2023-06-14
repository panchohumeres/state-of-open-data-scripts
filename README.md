# state-of-open-data
Set of scripts for compiling and visualizing publishing stats from Open Data portals, according to the technologies on which they are based such as Junar and CKAN.

# BI Projects
{ Currently offline due to changes in source data and APIs (government) }

* **NACK Search [2020]**
Replica search engine for the Chilean Government open data portal, based on open source-software CKAN. Search engine made with Elasticsearch, built with public and open data sources.
Tech Stach available at [https://github.com/panchohumeres/state-of-open-data-scripts](https://github.com/panchohumeres/NAKC)

* **State of Open Data [2019]**
Dashboard for visualizing real-time stats of the Chilean Government Open Data portal (datos.gob.cl), based on Kibana.
Tech Stach available at href="https://github.com/panchohumeres/state-of-open-data-scripts

# Notebooks
[https://anaconda.org/fhumeres/ckan_stats/notebook](Jupyter Notebook for getting datasets metadata from Chilean Open Data Portal) { might not work due to changes in source API }

# Files:
* **"CKAN_stats.py": Example Script for compiling stats from an Open-Data Portal based on CKAN, and export them to Excel (Python 2.7).**
Descriptive stats for all the resources (datasets) published in datos.gob.cl, the Chilean Government official Open Data Portal, based on open-source software [CKAN](https://en.wikipedia.org/wiki/CKAN). Datasets metadata has been extracted using [CKAN's official API, v3](https://docs.ckan.org/en/2.8/api/). 
A Dashboard Demo built with Kibana, for visualizing these stats can be accesed at: http://www.estado.datos.gob.cl.s3-website-sa-east-1.amazonaws.com/. You can access the Jupyter Notebook version [here](https://anaconda.org/fhumeres/ckan_stats/notebook)


* **"Junar_dt_stats.py": Example Script for compiling stats (only datasets) from an Open-Data Portal based on Junar, and export them to Excel (Python 2.7).**
Descriptive stats for all the datasets ("Conjuntos de Datos") published in [beta.datos.gob.cl](https://beta.datos.gob.cl), the future official Open Data Portal of the Chilean government, based on the SaaS platform [Junar](http://www.junar.com/). Resources metadata has been extracted from Junar's API. 
**NOTE: FIGURES MAY DIFFER SLIGHTLY FROM THE ONES REPORTED IN BETA.DATOS.GOB.CL. FOR OFFICIAL FIGURES, PLEASE REFER TO [beta.datos.gob.cl](https://beta.datos.gob.cl).** A Dashboard Demo built with Kibana, for visualizing these stats can be accesed at: http://www.state.junar.s3-website-sa-east-1.amazonaws.com/.
Demo made by [Francisco Humeres M.](https://www.linkedin.com/in/fhumeres/). You can access the Jupyter Notebook version [here](https://anaconda.org/fhumeres/junar_dt_stats/notebook).

* **"Junar_stats.py": Example Script for compiling stats (all resources) from an Open-Data Portal based on Junar, and export them to Excel (Python 2.7).**
Descriptive stats for all the resources ("Recursos") published in [beta.datos.gob.cl](https://beta.datos.gob.cl), the future official Open Data Portal of the Chilean government, based on the SaaS platform [Junar](http://www.junar.com/). Resources metadata has been extracted from Junar's API. 
**NOTE: FIGURES MAY DIFFER SLIGHTLY FROM THE ONES REPORTED IN BETA.DATOS.GOB.CL. FOR OFFICIAL FIGURES, PLEASE REFER TO [beta.datos.gob.cl](https://beta.datos.gob.cl).** A Dashboard Demo built with Kibana, for visualizing these stats can be accesed at: http://www.state.junar.s3-website-sa-east-1.amazonaws.com/.
Demo made by [Francisco Humeres M.](https://www.linkedin.com/in/fhumeres/). You can access the Jupyter Notebook version [here](https://anaconda.org/fhumeres/junar_stats/notebook).

* **"Junar_stats_charts.py": Example Script for compiling stats (all resources) from an Open-Data Portal based on Junar, and generating python visualizations (Python 2.7).**
Same code as "Junar_stats.py", but with additional code for visualizing stats using Python's visualization libraries (Matplotlib, Seaborn). Please consider running on Ipython or Jupyter Notebook environments.
You can access the Jupyter Notebook version [here](https://anaconda.org/fhumeres/junar_stats/notebook).



Demo made by [Francisco Humeres M.](https://www.linkedin.com/in/fhumeres/). More of my work can be seen in my [Portfolio](https://fjhumeres.myportfolio.com/). You can contact me at fhumeres[at]alum[dot]mit[dot]edu.

#### © 2019 Fancisco Humeres M. This work is licensed under a Creative Commons Attribution License CC-BY 4.0. All code contained herein is licensed under an MIT license
