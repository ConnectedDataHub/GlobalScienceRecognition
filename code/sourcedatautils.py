"""
Shared helpers to load the citation preferences, build the citation preference network, and write the
Source Data files.

The network construction follows GlobalCitationNetwork_analysisfigures.
"""
import os
import re
import numpy as np
import pandas as pd
import scipy.stats as spstats
from statsmodels.stats.multitest import multipletests as holm

path2repo = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
# the processed data used as input by the analysis code
path2data = os.path.join(path2repo, 'data')
# the Source Data: the data behind each figure and table
path2sourcedata = os.path.join(path2repo, 'Source Data')

syear, eyear = 1990, 2017

# the five communities inferred using the degree-corrected stochastic block model
comm2country = {0:['AE', 'BD', 'CN', 'CY', 'DZ', 'EG', 'ID', 'IN', 'IQ', 'IR', 'JO', 'KH', 'KR', 'KW', 'MA', 'MY', 'OM', 'PK', 'QA', 'SA', 'SG', 'TH', 'TN', 'TR', 'TW', 'VN'],
1:['AR', 'BN', 'BO', 'BR', 'BW', 'BY', 'CL', 'CM', 'CO', 'CR', 'GE', 'HK', 'HR', 'LU', 'MZ', 'NC', 'PA', 'PE', 'RU', 'SJ', 'ST', 'UY', 'VE'],
2:['AT', 'BE', 'CA', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GR', 'HU', 'IE', 'IL', 'IS', 'IT', 'JP', 'MX', 'NL', 'NO', 'NP', 'NZ', 'PH', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK'],
3:['AU', 'CH', 'GB', 'US'],
4:['BH', 'ET', 'GH', 'KE', 'MW', 'NG', 'TZ', 'UG', 'ZA', 'ZM', 'ZW']}

country2comm = {c:ci for ci,clist in comm2country.items() for c in clist}

# community labels (1-5) as numbered in Fig. 3E and the Supplementary connection probability figure
renumber_blocks = {3:0, 2:1, 1:4, 0:2, 4:3}
country2commlabel = {c:renumber_blocks[ci] + 1 for c, ci in country2comm.items()}


def load_country_auc():
    # the national citation preferences without the same organization and self citations
    country_auc_df = pd.read_csv(os.path.join(path2data, 'oa_countrycites_nosameorg_auc.csv.gz'))
    country_auc_df = country_auc_df[country_auc_df['N']>=50].copy()
    country_auc_df['CitedYear'] = country_auc_df['CitedYear'].astype(int)

    country_auc_df['Zscore'] = (country_auc_df['AUC'] - 0.5)/np.sqrt(country_auc_df['Cov'])
    # one-sided test in the direction of the observed preference: H1 is AUC > 0.5 (over-citation)
    # when Z > 0, and AUC < 0.5 (under-citation) when Z < 0
    country_auc_df['pvalue'] = spstats.norm.sf(np.abs(country_auc_df['Zscore'].values))

    def reject_holm(pvalues):
        reject, pvalues, _, _ = holm(pvalues, alpha=0.01, method='hs', is_sorted=False, returnsorted=False)
        return reject
    country_auc_df['Significant'] = country_auc_df.groupby('CitedYear')['pvalue'].transform(reject_holm)
    return country_auc_df


def load_net_auc(country_auc_df):
    # the significant international edges between 1990 and 2017
    net_auc = country_auc_df[country_auc_df['CitingCountry'] != country_auc_df['CitedCountry']]
    net_auc = net_auc[net_auc['Significant']]
    net_auc = net_auc[(net_auc['CitedYear'] >= syear) & (net_auc['CitedYear'] <= eyear)]
    return net_auc.sort_values(by=['CitedYear', 'CitedCountry']).reset_index(drop=True)


def cumulative_network(net_auc):
    # each country pair keeps its most recent significant citation preference
    return net_auc.sort_values('CitedYear').drop_duplicates(subset=['CitingCountry', 'CitedCountry'], keep='last')


edge_columns = {'CitingCountry':'Citing country', 'CitedCountry':'Cited country', 'CitedYear':'Cited year',
                'AUC':'AUC', 'Cov':'Variance', 'N':'N', 'Zscore':'Z-score', 'pvalue':'p-value'}


def write_source_data(fname, title, description, tables):
    """
    Write one plain table per sheet (header in the first row) so each sheet can be read with
    pd.read_excel(fname, sheet_name=sheet_name). The title, description and sheet contents are
    listed in a README sheet, and the README.txt for all Source Data files is updated.

    tables: list of (sheet_name, sheet_description, df)
    """
    os.makedirs(path2sourcedata, exist_ok=True)
    path2out = os.path.join(path2sourcedata, fname)

    readme = pd.DataFrame([['Title', title], ['Description', description]] +
                          [['Sheet: ' + sheet_name, sheet_description] for sheet_name, sheet_description, _ in tables],
                          columns=['Item', 'Content'])

    with pd.ExcelWriter(path2out, engine='openpyxl') as writer:
        readme.to_excel(writer, sheet_name='README', index=False)
        for sheet_name, _, df in tables:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print('wrote', os.path.normpath(path2out))
    write_readme_txt()


def write_readme_txt():
    # one README.txt listing the introduction of every Source Data Excel file
    # the main text files (SourceData_<n>_...) first, then the Supplementary files (SourceData_FigS<n>, SourceData_<n>_TableS<n>)
    fnames = [f for f in os.listdir(path2sourcedata) if re.match(r'SourceData_(\d+|FigS\d+)(_.*)?\.xlsx$', f)]

    def order(f):
        item = f.split('_')[1]
        if item.isdigit():
            return (0, int(item), f)
        return (1, int(re.match(r'FigS(\d+)', item).group(1)), f)
    fnames = sorted(fnames, key=order)

    path2txt = os.path.join(path2sourcedata, 'README.txt')
    with open(path2txt, 'w') as outfile:
        outfile.write('Source Data\n\n')
        outfile.write('Each Excel file contains a README sheet followed by one table per sheet '
                      '(header in the first row).\n')

        for fname in fnames:
            sheets = pd.read_excel(os.path.join(path2sourcedata, fname), sheet_name=None)
            readme = dict(sheets['README'][['Item', 'Content']].values)

            outfile.write('\n' + '=' * 80 + '\n')
            outfile.write(fname + '\n\n')
            outfile.write(readme['Title'] + '\n\n')
            outfile.write(readme['Description'] + '\n\n')
            outfile.write('Sheets:\n')
            outfile.write('- README: title, description and sheet contents.\n')
            for sheet_name, df in sheets.items():
                if sheet_name == 'README':
                    continue
                columns = ', '.join(map(str, df.columns))
                outfile.write('- {}: {} {} rows. Columns: {}.\n'.format(sheet_name, readme['Sheet: ' + sheet_name],
                                                                       df.shape[0], columns))

    print('wrote', os.path.normpath(path2txt))
