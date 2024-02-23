import pandas as pd
import requests
import base64
import os
import urllib3
import io
urllib3.disable_warnings()
import datetime
import json

class VisierDataConnector:
    """Class to manage ingestion of Visier data connectors

    See Visier user documentation for more information (you will need to log in to the service portal first): 
    https://my.visier.com/csm?id=kb_article_view&sysparm_article=KB0014851

    Parameters
    ----------
    company : str
        The company name used to connect to the Visier application e.g. [company].visier.com
    
    api_key : str
        The API key generated in the admin panel of the Visier application

    user : str
        The username used to connect to the data_connectors (typically email). This user must 
        have access to all data connectors that you intend to connect to with this Class

    pword : str
        The associated password for :code:`user`

    proxies : dict
        Dictionary containing 'http_proxy' and 'https_proxy' keys
    
    sslVerify: bool
        Defaults to True. If set to False, bypasses HTTPS Certificate verification (very dangerous)
    """
    def __init__(self, company, api_key, user, pword, proxies=None, sslVerify=True):

        self.company = company
        self.api_key = api_key
        self.proxies = proxies
        self.sslVerify = sslVerify

        self.auth = "Basic {}==".format(base64.b64encode(bytes("{}:{}".format(user,pword),"utf-8")).decode("utf-8"))

        self.url_base = f"https://{company}.api.visier.io/api/dataconnector/getData"

    def get_connector(self, connector_id, fName=None):
        """Function to make API call to Visier Data Connectors

        Parameters
        ----------
        connector_id: String
            String of id of data connector, available from Visier

        fName: String, optional
            Full file path, including csv extension that you want to give your file if you want to save it. If not declared, no file will be saved.

        Returns
        -------
        df: Pandas Dataframe
            Pandas Dataframe of returned data from the connector

        """
        urllib3.disable_warnings()
        params = {
                'id': connector_id,
                'apikey': self.api_key,
                'a':'b'
            }

        header = {"Authorization":self.auth}

        save=True
        if fName is None:
            save=False
            fName='temp.csv'

        r = requests.get(
            self.url_base, 
            params=params, 
            headers=header, 
            verify=self.sslVerify,
            proxies=self.proxies)

        if r.status_code == 200:
            f=open(fName,'wb')
            f.write(r.content)
            f.close()
        else:
            raise ValueError(f'API call failed with status code: {r.status_code}')

        df = pd.read_csv(fName)

        if not save:
            os.remove(fName)
        
        return df
    

class VisierAPI:
    """
        Class to help manage the authentication side of dealing with 
        the Visier Data Query API endpoints

        Parameters
        ----------
        uname: str
            The username of the API user

        pword: str
            The password of the API user

        apikey: str
            The company-wide API key accessed via the Visier Studio
            admin panel. Contact your admin if you are not sure.

        vanity_name: str
            The name associated with a Visier Cloud tenant. For example, 
            a tenant for an organization called Jupiter would have the 
            vanity name Jupiter. All tenants should use their own vanity 
            name in the API URL. When making changes to an analytic tenant 
            that you manage, the tenant is specified by its tenant code 
            in the API call.

            E.g. https://<<vanity_name>>.visier.com
        """
    def __init__(self, uname, pword, apikey, vanity_name='experian', proxies=None):
        
        self.uname = uname
        self.pword = pword
        self.apikey = apikey
        self.baseurl = f'https://{vanity_name}.api.visier.io/v1'
        self.proxies = proxies
        self._get_security_code()
    

    def _get_security_code(self):
        data = {
            'username': self.uname,
            'password': self.pword
        }

        resp = requests.post(
            f'{self.baseurl}/admin/visierSecureToken',
            data=data,
            proxies=self.proxies
        )

        if resp.status_code==200:
            self.security_code = resp.content.decode('ascii')
            self.security_code_expires = datetime.datetime.now() + datetime.timedelta(minutes=4, seconds=45)

        else:
            raise Exception(
                f'Security Code failed to generate with html status code: {resp.status_code}; Request URL: {self.baseurl}'
            )

    def query_api(self, api_path, method='get', data=None, custom_headers=None):
        """Function to query Visier Data Query APIs

        Parameters
        ----------
        api_path: Str
            The path of the url you wish to query. Must begin with '/'
            e.g. '/data/model/analytic-objects/Employee/dimensions'

        method: Str must be either 'get' or 'post'
            The type of http request you are trying to make

        data: Dictionary
            If your 'method' is 'post', this is the data you wish send 
            as part of the request.
        """
        headers = {
            'apikey': self.apikey,
            'Content-type': 'application/json',

        }

        if custom_headers is not None:
            for k,v in custom_headers.items():
                headers[k] = v

        cookies = {}

        if datetime.datetime.now() < self.security_code_expires:
            cookies['VisierASIDToken'] =  self.security_code
        else:
            self._get_security_code()
            cookies['VisierASIDToken'] =  self.security_code


        if method=='get':
            resp = requests.get(
                f'{self.baseurl}{api_path}',
                headers=headers,
                cookies=cookies,
                proxies=self.proxies
                )

        elif method=='post':
            resp = requests.post(
                f'{self.baseurl}{api_path}',
                headers=headers,
                cookies=cookies,
                data=data,
                proxies=self.proxies)

        if resp.ok:
            return resp
        else:
            raise Exception(f"""
                API call failed with html status code: {resp.status_code}\n
                {resp.json()}
            """)

    def _ttm_split(self, string):
        try:
            return string.split('/')[1]
        except:
            return string

    def _generate_df_from_agg_query(self, resp):
        data = io.StringIO(resp.content.decode('utf-8').replace('\r',''))

        df = pd.read_csv(data, dtype='str')

        df['DateInRange'] = df['DateInRange'].apply(lambda x: x.split(' - ')[0])
        df['DateInRange'] = df['DateInRange'].apply(lambda x: self._ttm_split(x))
        df['DateInRange'] = pd.to_datetime(df['DateInRange'])
        df['DateInRange'] = df['DateInRange'] - datetime.timedelta(days=1)
        df['DateInRange'] = df['DateInRange'].dt.strftime('%Y-%m-%d')

        df = df.fillna('')
        cols = list(df.columns)

        df = df.groupby(cols[cols.index('DateInRange'):]).sum().reset_index()

        return df 

    def get_aggregation_query(self, query):

        resp = self.query_api(
            '/data/query/aggregate',
            method='post',
            data=json.dumps(query),
            custom_headers={
                'Accept':'text/csv'
            }
        )

        df = self._generate_df_from_agg_query(resp)

        return df
    
    def get_list_query(self, query):
        resp = self.query_api(
            '/data/query/list',
            method='post',
            data=json.dumps(query),
            custom_headers={
                'Accept':'text/csv'
            }
        )

        data = io.StringIO(resp.content.decode('utf-8').replace('\r',''))

        df = pd.read_csv(data, dtype='str')

        return df
    
    def get_properties_list(self, analyticObjectId):
        resp = self.query_api(
            f'/data/model/analytic-objects/{analyticObjectId}/properties',
            method='get',
        )
        
        try:
            return resp.json()
        except:
            return resp.content