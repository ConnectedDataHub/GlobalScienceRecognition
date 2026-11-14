"""
Build the Source Data file for Figure 2 (required by Nature Communications).

usage: python 4_GlobalCitationNetwork_Fig2.py
"""
import numpy as np
import pandas as pd

from sourcedatautils import (load_country_auc, load_net_auc, cumulative_network, country2commlabel,
                             edge_columns, syear, eyear, write_source_data)


def fig2(cumulative_net):
    title = 'Figure 2: International network of scientific citation preferences.'
    description = ('Cumulative international citation preference network ({}-{}): each directed edge from the citing '
                   'country to the cited country is the most recent statistically significant citation preference '
                   '(N >= 50, Holm-Sidak correction with alpha = 0.01 within each year). '
                   'A) positive edges (Z-score > 0); B) negative edges (Z-score < 0) between the countries shown in A. '
                   'Node area is the in-degree in each panel; node colour is the community inferred using the '
                   'degree-corrected stochastic block model (labelled 1-5 as in Fig. 3E). '
                   'AUC, Variance (DeLong), N, Z-score and p-value as defined in Figure 1.').format(syear, eyear)

    pcumnet = cumulative_net[cumulative_net['Zscore'] > 0]
    countries = np.sort(np.unique(pcumnet[['CitingCountry', 'CitedCountry']].values.flatten()))

    # the negative network is drawn on the same countries as the positive network
    ncumnet = cumulative_net[cumulative_net['Zscore'] < 0]
    ncumnet = ncumnet[ncumnet['CitingCountry'].isin(countries) & ncumnet['CitedCountry'].isin(countries)]

    nodes = pd.DataFrame({'Country':countries})
    nodes['Community'] = nodes['Country'].map(country2commlabel)
    nodes['Positive in-degree (A)'] = nodes['Country'].map(pcumnet['CitedCountry'].value_counts()).fillna(0).astype(int)
    nodes['Negative in-degree (B)'] = nodes['Country'].map(ncumnet['CitedCountry'].value_counts()).fillna(0).astype(int)

    def edge_table(edges):
        edges = edges.sort_values(['CitingCountry', 'CitedCountry'])[list(edge_columns)].rename(columns=edge_columns)
        edges.insert(2, 'Citing community', edges['Citing country'].map(country2commlabel))
        edges.insert(3, 'Cited community', edges['Cited country'].map(country2commlabel))
        return edges

    tables = [('Nodes', 'Countries in A and B with their community and in-degree in each panel.', nodes),
              ('Positive edges', 'A) Positive edges of the cumulative network.', edge_table(pcumnet)),
              ('Negative edges', 'B) Negative edges of the cumulative network between the countries in A.',
               edge_table(ncumnet))]
    return title, description, tables


if __name__ == '__main__':
    country_auc_df = load_country_auc()
    cumulative_net = cumulative_network(load_net_auc(country_auc_df))

    write_source_data('SourceData_2_Fig2.xlsx', *fig2(cumulative_net))
