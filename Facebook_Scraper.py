"""
This program is to scrape data on the post from a specific Facebook fan page.
In this program, we target the bank.hvnh fanpage. However, one can change this configuration for his/her own needs.
After running this program, the excel and CSV files are produced
Programmer: Phuong V. Nguyen
phuong.nguyen@economics.uni-kiel.de
"""

from facebook_scraper import get_posts
import pandas as pd
from IPython.display import display

pages=10
def main():
    post_id=[]
    text=[]
    post_text=[]
    shared_text=[]
    time=[]
    image=[]
    likes=[]
    comments=[]
    shares=[]
    post_url=[]
    link=[]
    for post in get_posts('bank.hvnh', pages=pages):
        post_id.append(post['post_id'])
        text.append(post['text'])
        post_text.append(post['post_text'])
        shared_text.append(post['shared_text'])
        time.append(post['time'])
        image.append(post['image'])
        likes.append(post['likes'])
        comments.append(post['comments'])
        shares.append(post['shares'])
        post_url.append(post['post_url'])
        link.append(post['link'])
    df= pd.DataFrame({'post_id':post_id,
                 'text':text,
                'post_text':post_text,
                 'shared_text':shared_text,
                 'time':time,
                  'image':image,
                 'likes':likes,
                 'comments':comments,
                 'shares':shares,
                 'post_url':post_url,
                 'link':link})
    display(df.head(5).T)
    #print(df.head(5).T)
    df.to_excel("Fanpage_fb.xlsx")  
    df.to_csv("Fanpage_fb.csv")
    print('DONE !')
    
    
if __name__ == '__main__':
    main()