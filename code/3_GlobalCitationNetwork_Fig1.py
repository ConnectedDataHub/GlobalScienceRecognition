"""
Build the Source Data file for Figure 1 (required by Nature Communications).

usage: python 3_GlobalCitationNetwork_Fig1.py
"""
import pandas as pd

from sourcedatautils import load_country_auc, write_source_data


def fig1(country_auc_df):
    title = 'Figure 1: Illustration of the measure of national citation preference.'
    description = ('National citation preference of Japan (JP) towards articles published in 2017 by '
                   'Switzerland (CH), Australia (AU), and India (IN). '
                   'AUC: area under the curve comparing the 5-year citations (c5) from Japan to articles from the '
                   'target country against articles from all countries; Variance: DeLong variance of the AUC; '
                   'N: number of target-country articles cited by Japan; Z-score = (AUC - 0.5)/sqrt(Variance); '
                   'p-value: normal tail probability of |Z-score|. '
                   'Network link: sign of the citation preference if statistically significant after the '
                   'Holm-Sidak correction (alpha = 0.01) across all country pairs in 2017.')

    panels = [('Top', 'CH'), ('Middle', 'AU'), ('Bottom', 'IN')]
    rows = []
    for panel, cited_c in panels:
        row = country_auc_df[(country_auc_df['CitingCountry'] == 'JP') & (country_auc_df['CitedYear'] == 2017)
                             & (country_auc_df['CitedCountry'] == cited_c)].iloc[0]
        if not row['Significant']:
            link = 'None'
        elif row['Zscore'] > 0:
            link = 'Positive'
        else:
            link = 'Negative'
        rows.append([panel, row['CitingCountry'], row['CitedCountry'], row['CitedYear'], row['AUC'],
                     row['Cov'], int(row['N']), row['Zscore'], row['pvalue'], link])

    df = pd.DataFrame(rows, columns=['Panel', 'Citing country', 'Cited country', 'Cited year', 'AUC',
                                     'Variance', 'N', 'Z-score', 'p-value', 'Network link'])
    tables = [('Citation preferences', 'AUC and significance of the three illustrated country pairs.', df)]
    return title, description, tables


if __name__ == '__main__':
    country_auc_df = load_country_auc()

    write_source_data('SourceData_1_Fig1.xlsx', *fig1(country_auc_df))
