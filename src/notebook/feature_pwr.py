#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed 13th Nov 2019
@author: Xuqing Liu
"""
## Import libraries ##
###################################################################################################################
import codecs
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import iqr, boxcox, chi2_contingency
from scipy.stats import chisquare
import scipy.special as sc
from sklearn.metrics import roc_auc_score
from collections import defaultdict, Counter
#from sklearn.preprocessing import QuantileTransformer, MinMaxScaler, StandardScaler, LabelEncoder
from multiprocessing import Pool, cpu_count
import multiprocessing
import timeit
import os, gc, time, pickle, sys
#from tqdm import tqdm_notebook as tqdm
from tqdm import  tqdm
from glob import glob
import warnings
warnings.filterwarnings('ignore')
from utils import *


## Feature Power Class ##
###################################################################################################################


class feature_power():
    def __init__(self, OUTPUTDIR, df, table_name, target, object_variable_list, numeric_variable_list):
        
        self.OUTPUTDIR = OUTPUTDIR # A directory for saving output dataframes as pickles
        self.df = df # A dataframe of processed datamart of a data source table
        self.table_name = table_name # Table name of the source
        self.target = target # The expression of the target
        self.object_variable_list = object_variable_list
        self.numeric_variable_list = numeric_variable_list
        
        
        # Usage Sample:
        # fp = feature_power(df, table_name, target, object_variable_list, numeric_variable_list)
        # odds_ratio = fp.calc_odds() # a dataframe contains feature power value calculated by
        #                           # log odds ratio will retured with each feature name 
       
        
## Categorical Features ##        
    def calc_odds(self):
        log_odds_list = {} 
        for var in tqdm(self.object_variable_list):
            p = self.df.groupby(var)[self.target].sum()/self.df.groupby(var)[self.target].count()
            q = 1-p
            label_df = pd.DataFrame(p)
            label_df.columns = ['p']
            label_df['q'] = q
            label_df['odds'] = (p*(1-q))/((1-p)*q)
            label_df['lodr'] = label_df['odds'].apply(lambda x: np.log1p(x))
            if label_df['lodr'].min() != 0:
                log_odds_list[var] = (label_df['lodr'].max() ,label_df['lodr'].max()/label_df['lodr'].min())
            else:
                log_odds_list[var] = (label_df['lodr'].max() ,label_df['lodr'].max())
        outdf = pd.DataFrame(log_odds_list).T
        outdf.columns = ['lodr_max', 'lodr_max2min']
        outdf['table_name'] = table_name
        outdf.reset_index(inplace=True, drop=False)
        return outdf 
    
    
    def calc_chisq(self):
        chisq_list={}
        for var in tqdm(self.object_variable_list):
            obs = self.df.groupby(var)[self.target].sum()
            label_df = pd.DataFrame(obs)
            label_df.columns = ['obs']
            p = self.df[self.target].sum()/len(df)
            exp = self.df.groupby(var)[self.target].count() * p
            chisq_list[var] = chisquare(obs, exp)
            normalizer = len(df[var].unique())
        #print(auc_list)
        outdf = pd.DataFrame(chisq_list).T
        outdf.columns = ['chi_stats', 'chi-pvalue']
        outdf['chi_stats'] = outdf['chi_stats']/normalizer
        outdf['table_name'] =  table_name
        outdf.reset_index(inplace=True, drop=False)
        return outdf

## Numerical Features ##      
    def calc_auc(self):
        auc_list={}
        for var in tqdm(self.numeric_variable_list):
            self.df.sort_values(by=var, ascending =False,inplace=True)
            self.df.reset_index(inplace=True, drop=True)
            y_true = self.df[self.target].values
            y_pred = self.df[var].values
            auc = np.abs(roc_auc_score(y_true, y_pred)-0.5)
            auc_list[var] = [auc]
        #print(auc_list)
        outdf = pd.DataFrame(auc_list).T
        outdf.columns = ['auc']
        outdf['table_name'] = table_name
        outdf.reset_index(inplace=True, drop=False)
        return outdf
      
    def calc_ks(self):
        ks_list={}
        for var in tqdm(self.numeric_variable_list):
            self.df.sort_values(by=var, ascending =False,inplace=True)
            self.df.reset_index(inplace=True, drop=True)
            tgt_sum = self.df[self.target].sum()
            ntgt_sum = len(df) - tgt_sum
            self.df['rank'] = self.df[var].rank(ascending=True).astype('int')
            self.df['p'] = self.df[self.target].cumsum(axis=0)/tgt_sum
            self.df['q'] = ( self.df['rank']-self.df[self.target].cumsum(axis=0) )/ntgt_sum
            self.df['ks'] = np.abs(self.df['p'] - self.df['q'])
            ks_list[var] = [self.df['ks'].sum()/len(self.df)]
        #print(ks_list)
        outdf = pd.DataFrame(ks_list).T
        outdf.columns = ['ks']
        outdf['table_name'] = table_name
        outdf.reset_index(inplace=True, drop=False)
        return outdf
    
    def get_feat_pwr_num(self, ifsave = False):
        if len(numeric_variable_list) > 0:
            # Numerical variables
            print('Processing KS value ...')
            t_ks = self.calc_ks()

            print('Processing AUC ...')
            t_auc = self.calc_auc()

            print('Merging ...')
            fp_numv = pd.merge(t_ks,t_auc, on =['index', 'table_name'], how='left')

            print('\n Merge Finished! \n')


            fp_numv = fp_numv[['table_name', 'index', 'ks', 'auc']]
            fp_numv.rename(columns = {'index': 'feature'},inplace=True)

            if ifsave:
                file_name = table_name.replace(f'{self.OUTPUTDIR}/', '').replace('.txt','')
                with open(f'{self.OUTPUTDIR}/'+file_name+'_num_feature_power_df.pickle', mode = 'wb') as f:
                    pickle.dump(fp_numv, f, protocol=4)
            else:
                pass
        else:
            print('No applicable variables')
        return fp_numv
    
    def get_feat_pwr_cat(self, ifsave = False):
        if len(object_variable_list) > 0:

            # Categorical variables
            print('Processin Chi-squared Stats ...')
            t_chisq = self.calc_chisq()

            print('Processing log odds ratio ...')
            t_lodr = self.calc_odds()

            print('Merging ...')
            fp_catv = pd.merge(t_chisq, t_lodr, on =['index', 'table_name'], how='left')
            print('\n Merge Finished!')

            fp_catv = fp_catv[['table_name', 'index', 'chi_stats', 'chi-pvalue',  'lodr_max', 'lodr_max2min']]
            fp_catv.rename(columns = {'index': 'feature'},inplace=True)
            if ifsave:
                file_name = table_name.replace(f'{self.OUTPUTDIR}/', '').replace('.txt','')

                with open(f'{self.OUTPUTDIR}/'+file_name+'_cat_feature_power_df.pickle', mode = 'wb') as f:
                    pickle.dump(fp_catv, f, protocol=4)
            else:
                pass
        else:
            print('No applicable variables')
        return fp_catv
        
