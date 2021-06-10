#!/usr/bin/env python
# coding: utf-8

# In[38]:


import shutil, os
from dotenv import load_dotenv
import requests
import zipfile
# In[39]:


load_dotenv()


# In[40]:


cloud_url = os.getenv('CLOUD_URL')
cloud_token = os.getenv('CLOUD_TOKEN')


# In[41]:


download_link = cloud_url + 'download/carl/client'


# In[42]:

try:
	r = requests.get(download_link, headers={"Authorization":f"Token {cloud_token}"})
except Exception as e :
	print('error while downloading the zip')



# In[43]:


# Saves the zip file
try :
	with open("latest.zip", "wb") as code:
    		code.write(r.content)
except Exception as e:
	print('error while saving the zip')


# In[65]:


# unzips it
directory_to_extract_to = '/home/pi/carlpi/'
filename = ''
with zipfile.ZipFile('latest.zip', 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)


# In[ ]:


#os.system("sudo shutdown -r now")


# In[ ]:



