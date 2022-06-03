import requests
from bs4 import BeautifulSoup
import requests_cache

import settings


class Pu9sf:
    """ PU 9 Shop flow API 
    """

    def __get_hidden_input(self, content):
        """ Return the dict contain the hidden input 
        """
        tags = dict()
        soup =BeautifulSoup(content, 'html.parser')
        hidden_tags = soup.find_all('input', type='hidden')
        # print(*hidden_tags)
        for tag in hidden_tags:
            tags[tag.get('name')] = tag.get('value')
        
        return tags

    def __login_session(self, sess):
        url = f'http://{settings.ip}/RACK_WEB/'
        login_cred = {
            'username' : settings.username,
            'password' : settings.password,
            'btnLogin' : 'Login'
        }
        r = sess.get(url)
        asp_tags = self.__get_hidden_input(r.content)
        login_cred.update(asp_tags)
        r= sess.post(url, data=login_cred)
        tags = self.__get_hidden_input(r.content)
        return tags

    def wip(self):
        racks = []

        # with requests_cache.CachedSession('big_data_cache') as sess:
        with requests.Session() as sess:
            # p = sess.post(url, data=payload)
            # print(p.text)

            payload = {
                'Title': 'TEST MONITOR',
                'Site' : 'QMF',
                'Item' : 'RackTesting',
                'Type' : 'PO',
                'Customer' : '',
                'Model' : '',
                'Num' : ''
            }

            url = f'http://{settings.ip}/RACK_WEB/Forms/Report/frmWIPDetail.aspx'
            p=sess.post(url, data=payload)
            d =dict()
            soup = BeautifulSoup(p.text, 'html.parser')
            wip_html = soup.find(id='gv2')
            # for th in wip_html.select('th'):
            #     print(th.text.strip())
            header = list(map(lambda x: x.text.strip(), wip_html.select('th')))
            # print(header)

            for r in wip_html.select('tr')[1:]:
                rack_info = list(map(lambda x: x.text.strip(), r.select('td')))
                d = dict(zip(header, rack_info))
                racks.append(d)

        return racks

    def racklink(self, racksn):
        base_frm = f'http://{settings.ip}/RACK_WEB/Forms/Report/frmRacklinkQuery.aspx'

        payload = {}

        sel_report_type =  {
            '__EVENTTARGET' : 'dlReportType',
            'dlSite' : 'QMF',
            'dlReportType' : 'RackLink',
            'dlConditions' : 'RackSN',
            'txtConditionsValue' : None
        }

        sel_conditions =  {
            '__EVENTTARGET': 'dlConditions',
            'dlSite': 'QMF',
            'dlReportType': 'RackLink',
            'dlConditions': 'RackSN',
            'txtDateStart': None,
            'txtDateEnd': None 
        }

        sel_racksn = {
            '__EVENTTARGET' : 'btnExcel',
            'dlSite': 'QMF',
            'dlReportType': 'RackLink',
            'dlConditions': 'RackSN',
            'txtConditionsValue' : racksn
        }
        racklink=[]

        # with requests_cache.CachedSession('big_data_cache') as sess:
        with requests.Session() as sess:

            # sess.headers.update(headers)
            self.__login_session(sess)
            r=sess.get(base_frm)
            attrs = self.__get_hidden_input(r.content)
            attrs.update(sel_report_type)
            r=sess.post(base_frm, data=attrs)
            attrs = self.__get_hidden_input(r.content)
            attrs.update(sel_conditions)
            r=sess.post(base_frm, data=attrs) 
            attrs = self.__get_hidden_input(r.content)
            attrs.update(sel_racksn)
            r=sess.post(base_frm, data=attrs)
            if (r.status_code == 200):
                # Processing CSV code, tab separated.
                buf = r.text.splitlines()
                header = False
                for line in buf:
                    if header is False:
                        header = line.split('\t')
                    row = dict(zip(header, line.split('\t')))
                    racklink.append(row)
            
            return racklink


    def __init__(self):
        self.ip = settings.ip

   

if __name__ == '__main__':
    pass
     



    


