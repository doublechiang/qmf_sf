from typing import OrderedDict
from numpy import append
import requests
from bs4 import BeautifulSoup
import requests_cache

import settings

def login_seesion(sess, payload):
    url = 'http://10.243.20.207/RACK_WEB/'
    login_cred = {
        'username' : settings.username,
        'password' : settings.password,
        'btnLogin' : 'Login'
    }
    r = sess.get(url)
    asp_tags = get_hidden_input(r.content)
    login_cred.update(asp_tags)
    r= sess.post(url, data=login_cred)
    tags = get_hidden_input(r.content)
    return tags



def get_hidden_input(content):
    """ Return the dict contain the hidden input 
    """
    tags = dict()
    soup =BeautifulSoup(content, 'html.parser')
    hidden_tags = soup.find_all('input', type='hidden')
    # print(*hidden_tags)
    for tag in hidden_tags:
        tags[tag.get('name')] = tag.get('value')
    
    return tags


def wip_test_monitor():
    racks = []

    with requests_cache.CachedSession('big_data_cache') as sess:
    # with requests.Session() as sess:
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

        url = 'http://10.243.20.207/RACK_WEB/Forms/Report/frmWIPDetail.aspx'
        p=sess.post(url, data=payload)
        # print(p.text)
        d =OrderedDict()
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


def base_query_racklink(sn):

    main_frm = 'http://10.243.20.207/RACK_WEB/Forms/Main/frmMain.aspx'
    base_frm = 'http://10.243.20.207/RACK_WEB/Forms/Report/frmRacklinkQuery.aspx'
    racklink_payload = {
        'dlSite' : 'QMF',
        'dlReportType' : 'RackLink',
        'dlConditions' : 'RackSN',
        'txtConditionsValue' : sn,
        'txtDateStart' : None,
        'txtDateEnd' : None,
        'btnQuery' : 'Query',
        'btnExcel' : 'To Excel(csv)'
    }

    racklink=[]

    # with requests_cache.CachedSession('big_data_cache') as sess:
    with requests.Session() as sess:
        payload = {}
        headers = {
            'User-Agent' : 'Mozilla/5.0'
        }

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
            # '__EVENTTARGET' : 'btnQuery',
            '__EVENTTARGET' : 'btnExcel',
            'dlSite': 'QMF',
            'dlReportType': 'RackLink',
            'dlConditions': 'RackSN',
            'txtConditionsValue' : sn
        }

        # sess.headers.update(headers)
        asp_tags = login_seesion(sess, payload)

        r=sess.get(base_frm)
        asp_tags = get_hidden_input(r.content)
        payload = asp_tags
        payload.update(sel_report_type)
        r=sess.post(base_frm, data=payload)
        asp_tags = get_hidden_input(r.content)
        payload = asp_tags
        payload.update(sel_conditions)
        r=sess.post(base_frm, data=payload) 
        asp_tags = get_hidden_input(r.content)
        payload=asp_tags
        payload.update(sel_racksn)
        r=sess.post(base_frm, data=payload)
        if (r.status_code == 200):
            # Processing CSV code, tab separated.
            buf = r.text.splitlines()
            header = False
            for line in buf:
                if header is False:
                    header = line.split('\t')
                row = dict(zip(header, line.split('\t')))
                racklink.append(row)
        
        print(racklink)
        return racklink
        

if __name__ == '__main__':
    # racks = wip_test_monitor()    
    base_query_racklink('R21932204000601E')
     



    


