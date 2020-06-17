
"""
This program is to scrape data on the post from a specific Facebook fan page.
In this program, we target the BIDVbankvietnam fanpage. However, one can change this configuration for his/her own needs.
After running this program, the excel and CSV files are produced.
Programmer: Phuong V. Nguyen
phuong.nguyen@economics.uni-kiel.de
"""

from facebook_scraper import get_posts
import pandas as pd
from IPython.display import display
get_ipython().run_line_magic('reload_ext', 'sql')
import sqlite3
Purple= '\033[95m'
Cyan= '\033[96m'
Darkcyan= '\033[36m'
Blue = '\033[94m'
Green = '\033[92m'
Yellow = '\033[93m'
Red = '\033[91m'
Bold = "\033[1m"
Reset = "\033[0;0m"
Underline= '\033[4m'
End = '\033[0m'

# One might change the following fanpage name base on his/her own needs
fanpage='BIDVbankvietnam'

class extract():
    
    print('----------------Thank'+'\033[0m'+ ' Mr. Nguyen'+'\033[0m'+' so much for providing this computer programe----------------')
    print('-----------------------------phuong.nguyen@economics.uni-kiel.de-----------------------------')
    
    def __init__(self,fanpage):
        print('\033[1m'+'Extract'+'\033[0m')
        self.name_fp=fanpage
        self.pages=5
        self.post_id,self.text,self.shared_text,self.time,self.image,self.likes,        self.comments,self.shares,self.post_url,self.link =self.scrape(self.name_fp,self.pages)
        
    def scrape(self,name_fp,page):
        print('I am scraping data from the '+ '\033[1m'+ name_fp+ End+' Facebook fanpage \n...')
        self.post_id,self.text,self.post_text,self.shared_text,self.time,self.image,self.likes,        self.comments,self.shares,self.post_url,self.link=[],[],[],[],[],[],[],[],[],[],[]
        for post in get_posts(name_fp, pages=page):
            self.post_id.append(post['post_id'])
            self.text.append(post['text'])
            self.post_text.append(post['post_text'])
            self.shared_text.append(post['shared_text'])
            self.time.append(post['time'])
            self.image.append(post['image'])
            self.likes.append(post['likes'])
            self.comments.append(post['comments'])
            self.shares.append(post['shares'])
            self.post_url.append(post['post_url'])
            self.link.append(post['link'])
        print('I am done!')
        return self.post_id,self.text,self.shared_text,self.time,self.image,self.likes,        self.comments,self.shares,self.post_url,self.link

class transform():
    
    def __init__(self,extract):
        print('\033[1m'+'Transform'+'\033[0m')
        self.post_id,self.text,self.post_text,self.shared_text,self.time,self.image,self.likes,        self.comments,self.shares,self.post_url,self.link =extract.post_id,extract.text,        extract.post_text,extract.shared_text,extract.time,extract.image,extract.likes,        extract.comments,extract.shares,extract.post_url,extract.link 
        self.trans_data=self.to_pandas(self.post_id,self.text,self.post_text,self.shared_text,self.time,
                                 self.image,self.likes,self.comments,self.shares,self.post_url,
                                 self.link)
        
    def to_pandas(self,post_id,text,post_text,shared_text,time,
                  image,likes,comments,shares,post_url,link):      
        print('I am building a Pandas DataFrame \n...')
        self.data= pd.DataFrame({'post_id':post_id,'text':text,'post_text':post_text,
                                     'shared_text':shared_text,'time':time,'image':image,
                                     'likes':likes,'comments':comments, 'shares':shares,
                                     'post_url':post_url,'link':link})
        self.no_obs=3
        print('The first %d observations'%self.no_obs +'\n...')
        display(self.data.head(self.no_obs).T)
        print('I am done!')
        return self.data
            
class load():
    
    def __init__(self,transform):
        print('\033[1m'+'Load'+'\033[0m')
        self.loaded_data=transform.trans_data
        #self.path=r'C:\Users\Phuong_1\Documents\PhuongDatabase'
        self.path=r'Phuong_database.db'
        self.connect=self.connect_sql()
        self.insert_data=self.persist_data(self.loaded_data)
        self.explor_tab=self.explor_table()
        self.ex_data=self.export_data(self.loaded_data,fanpage)
        
    def connect_sql(self):
        print('I am trying to connect to the database \n...')
        self.connect = get_ipython().run_line_magic('sql', 'sqlite:///Phuong_database.db')
        print(self.connect)
        print('The connection is success!')
        
    def persist_data(self,data):
        print('I am inserting data to the database \n...')
        self.check_data = get_ipython().run_line_magic('sql', 'DROP TABLE IF EXISTS data')
        self.insert_data = get_ipython().run_line_magic('sql', 'PERSIST data')
        print('I am done!')
        
    def explor_table(self):
        print('I am exploring the database \n...')
        self.explor_tabs = get_ipython().run_line_magic('sql', "SELECT name FROM sqlite_master WHERE type='table'")
        print(self.explor_tabs)
        self.explor_cols = get_ipython().run_line_magic('sql', 'SELECT * FROM data WHERE 1=0')
        display(self.explor_cols)
        self.explor_obs = get_ipython().run_line_magic('sql', 'SELECT * FROM data LIMIT 2')
        display(self.explor_obs)
        print('I understood the database structure!')
        return self.explor_obs
    
    def export_data(self,data,name_file):
        print('I am exporting data to the csv an excel files \n...')
        self.export_csv=data.to_csv(name_file+'.csv')
        self.export_exl=data.to_excel(name_file+'.xlsx')
        print('Data is exported successfully!')
        return self.export_csv

class main():
    extract=extract(fanpage)
    transform=transform(extract)
    load=load(transform)
    
if __name__ == '__main__':
    main()
