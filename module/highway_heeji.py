from bs4 import BeautifulSoup
import requests

class Highway:
    
    def __init__(self, highway):
        
        self.highway = highway
        self.url = f'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query={highway}'
        self.response = requests.get(self.url)
        print(self.response)
        self.dom = BeautifulSoup(self.response.text , 'html.parser')
        self.h = self.dom.select('#main_pack > section.sc_new.cs_traffic._cs_real_traffic > div > div.api_cs_wrap > div.t_area > div.t_rt > div > div:nth-child(4) > ul')
        
    def bot_sum(self):
        h_up = self.h[0]
        h_down = self.h[1]

        li_h_up = []
        for data in h_up.select('li'):
            d = data.text.split()   # ['구간','거리', '시속,', '상태']
            if 'JC' in d[0] or 'IC' in d[0]:
                # d[2] = d[2].replace(',','')
                
                li_h_up.append(d)
            

        li_h_down = []
        for data in h_down.select('li'):
            d = data.text.split()
            if 'JC' in d[0] or 'IC' in d[0]:  
                # d[2] = d[2].replace(',','')
                li_h_down.append(d)
            
        dic = {
            'up':[],
            'down':[]
        }
            
        for down in li_h_down[:2]:
            dic['down'].append({'section' : down[0], 'distance': down[2], 'speed' : down[3].replace(',',''), 'conditions':down[-1]})


        for up in li_h_up[:2]:
            # dic['up'].append({'section' : up[0], 'distance': up[2], 'speed' :'희지ㅡㅡ', 'conditions':up[-1]})
            dic['up'].append({'section' : up[0], 'distance': up[2], 'speed' : up[3].replace(',',''), 'conditions':up[-1]})
            
        return dic
    
    def web_full(self):
        h_up = self.h[0]
        h_down = self.h[1]
        
        li_h_up = []
        for data in h_up.select('li'):
            d = data.text.split()
            if 'JC' in d[0] or 'IC' in d[0]:
                # d[2] = d[2].replace(',','')
                li_h_up.append(d)
            
            
        li_h_down = []
        for data in h_down.select('li'):
            d = data.text.split()
            if 'JC' in d[0] or 'IC' in d[0]:  
                # d[2] = d[2].replace(',','')
                li_h_down.append(d)
            
        dic = {
            'up':[],
            'down':[]
        }
            
        for down in li_h_down:
            dic['down'].append({'section' : down[0], 'distance': down[2], 'speed' : down[3].replace(',',''), 'conditions':down[-1]})


        for up in li_h_up:
            dic['up'].append({'section' : up[0], 'distance': up[2], 'speed' : up[3].replace(',',''), 'conditions':up[-1]})
            
        return dic
        
    