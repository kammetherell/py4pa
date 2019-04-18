import pandas as pd
import numpy as np
import datetime
import os


def clean_email_data(dir, files='all', include_subject=False, engine='c', encoding='latin', delete_old_file=False):
    start = datetime.datetime.now()
    print('Starting: ', str(start.hour).zfill(2) + ':'+ str(start.minute).zfill(2))

    if files == 'all':
        files_to_process =  [f for f in os.listdir(dir) if f.endswith('.csv')]
    else:
        files_to_process = files

    num_files = len(files_to_process)
    print(f'{num_files} to process')

    cols_to_load = ['message_id','SenderAddress','RecipientAddress','Received','Size','Status']

    if include_subject:
        cols_to_load.append('Subject')

    for idx, file in enumerate(files_to_process):
        path = dir + file

        df_emails = pd.read_csv(
            path,
            usecols=cols_to_load,
            engine=engine,
            encoding=encoding,
            error_bad_lines=False)

        output_fname = dir + file[:-4] + '_cleaned.csv'

        df_emails.to_csv(output_fname, index=False)

        if delete_old_file:
            os.unlink(path)

        finish = datetime.datetime.now()
        print(f'File {idx+1}/{num_files}: {file} finished at: {str(finish.hour).zfill(2)}:{str(finish.minute).zfill(2)}')

    return None


def _get_density(df_nodes, row, target_attribute):
    if row['sender_group'] == row['recipient_group']:
        node_count = df_nodes[df_nodes[target_attribute]==row['recipient_group']]['email'].count()
        density = row['num_edges']/(node_count * (node_count - 1))
        return density
    else:
        node_count_sender = df_nodes[df_nodes[target_attribute]==row['sender_group']]['email'].count()
        node_count_recipient = df_nodes[df_nodes[target_attribute]==row['recipient_group']]['email'].count()
        density = row['num_edges']/(node_count_sender * node_count_recipient)
        return density


def calc_density(df_nodes, df_edges, target_attribute):
    """Calculates the density of connections between the groups in a specific target target_attribute

    Parameters
    ----------
    df_nodes


    Returns
    ----------
    Pandas DataFrame containing the densities
    """

    df_edges['sender_group'] = df_edges['SenderAddress'].map(df_nodes.set_index('email')[target_attribute])
    df_edges['recipient_group'] = df_edges['RecipientAddress'].map(df_nodes.set_index('email')[target_attribute])

    df_densities = pd.DataFrame({'num_edges': df_edges.groupby(['sender_group','recipient_group'])['weight'].agg('count')}).reset_index()

    print(df_densities.head())

    df_densities['density'] = df_densities.apply(lambda row: _get_density(df_nodes, row, target_attribute), axis=1)

    df_densities = df_densities[['sender_group','recipient_group','density']]
    df_densities['density'] = round(df_densities['density']*100,2)

    return df_densities


def _get_modularity(df_edges, row, target_attribute, weighted, source):
    if source == 'sender':
        source_group = 'sender_group'
        end_group = 'recipient_group'
    else:
        source_group = 'recipient_group'
        end_group = 'sender_group'

    if weighted:
        num_same_group = df_edges[(df_edges[source_group]==row[source_group]) & (df_edges[end_group]==row[source_group])]['weight'].count()
        num_diff_group = df_edges[(df_edges[source_group]==row[source_group]) & (df_edges[end_group]!=row[source_group])]['weight'].count()
    else:
        num_same_group = df_edges[(df_edges[source_group]==row[source_group]) & (df_edges[end_group]==row[source_group])]['weight'].sum()
        num_diff_group = df_edges[(df_edges[source_group]==row[source_group]) & (df_edges[end_group]!=row[source_group])]['weight'].sum()

    if num_same_group != 0:
        modularity = num_same_group/num_diff_group
        return modularity
    else:
        return np.nan


def calc_modularity(df_nodes, df_edges, target_attribute, weighted=False, source='sender'):

    if source == 'sender':
        source_group = 'sender_group'
        end_group = 'recipient_group'
    else:
        source_group = 'recipient_group'
        end_group = 'sender_group'

    df_edges['sender_group'] = df_edges['SenderAddress'].map(df_nodes.set_index('email')[target_attribute])
    df_edges['recipient_group'] = df_edges['RecipientAddress'].map(df_nodes.set_index('email')[target_attribute])

    if weighted:
        df_modularities = pd.DataFrame({'num_edges': df_edges.groupby([source_group])['weight'].agg('sum')}).reset_index()
    else:
        df_modularities = pd.DataFrame({'num_edges': df_edges.groupby([source_group])['weight'].agg('count')}).reset_index()

    df_modularities['modularity'] = df_modularities.apply(
        lambda row: _get_modularity(
            df_edges,
            row,
            target_attribute,
            weighted,
            source)
        , axis=1)

    df_modularities = df_modularities[[source_group,'modularity']]

    return df_modularities
