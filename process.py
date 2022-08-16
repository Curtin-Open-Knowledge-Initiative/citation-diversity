# Reporting template
#
# Copyright 2020-21 ######
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: COKI Team
import json
from pathlib import Path
import os
import copy

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from typing import Optional, Callable, Union

from google.cloud import bigquery

from observatory.reports import report_utils, provndoc_utils
from precipy.analytics_function import AnalyticsFunction
from report_data_processing.parameters import *
from report_data_processing.sql import *

# Insert applicable graphs once created
# from report_graphs import (
#     Alluvial, OverallCoverage, BarLine, ValueAddBar, ValueAddByCrossrefType, ValueAddByCrossrefTypeHorizontal,
#     PlotlyTable
# )

# Replace with applicable project name
PROJECT_ID = 'coki-scratch-space'
TEMPDIR = Path('tempdir')


def process_sql_templates_to_queries(af: AnalyticsFunction,
                                     rerun: bool=RERUN):

    parameters = dict(

    )
    provndoc_utils.process_sql_to_queries(af,
                                          SQL_TEMPLATE_PARAMETERS,
                                          rerun,
                                          SQL_TEMPLATES_DIRECTORY,
                                          SQL_PROCESSED_DIRECTORY)

def provenance_n_documentation(af: AnalyticsFunction,
                               rerun: bool = RERUN):

    provndoc_utils.build_sql_dag(af, rerun, SQL_PROCESSED_DIRECTORY)


def create_global_citation_diversity_table(af: AnalyticsFunction,
                                           rerun: bool = RERUN,
                                           verbose: bool = True):
    """
    Run global_citations_query.sql_templates to generate article level citation diversity data
    """

    query = load_sql_to_string('global_citation_query.sql',
                               directory=SQL_PROCESSED_DIRECTORY)

    if not report_utils.bigquery_rerun(af, rerun, verbose):
        print(f"""Query is:            
            {query}

            """)
        print(f'Destination Table: {CITATION_DIVERSITY_TABLE}')
        return

    with bigquery.Client() as client:
        job_config = bigquery.QueryJobConfig(destination=CITATION_DIVERSITY_TABLE,
                                             create_disposition="CREATE_IF_NEEDED",
                                             write_disposition="WRITE_TRUNCATE")

        # Start the query, passing in the extra configuration.
        query_job = client.query(query, job_config=job_config)  # Make an API request.
        query_job.result()  # Wait for the job to complete.

    print("...completed")


def get_data(af: AnalyticsFunction):
    """
    Create main citation diversity table and save as new table in BigQuery
    """

    print("Generating the Citation Diversity Table")

    for year in YEAR_RANGE:
        query = load_sql_to_string('cit_div_vs_cit_count.sql_templates',
                                   parameters=dict(year=year),
                                   directory='report_data_processing/sql_templates')

        # Start the query, passing in the extra configuration.
        query_job = client.query(global_citation_query, job_config=job_config)  # Make an API request.
        query_job.result()  # Wait for the job to complete.

    print("...completed")


def pull_data(af: AnalyticsFunction):
    """
    Pull data down for analysis
    """

    print("Pulling data from Bigquery")
    data = pd.read_gbq(query=global_citation_query)
    data.to_csv(TEMPDIR / 'file.csv')
    af.add_existing_file(TEMPDIR / 'file.csv')
    print('...completed')


def plot_boxplot_div_by_cit_group(df, method='GiniSim', group='Countries', year=2019):
    # input variables method is either GiniSim or Shannon, group is one of Institutions, Countries, Subregions,
    # or Regions or Fields
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_' + str(method)].loc[df.is_oa],
                         x=df['cit_group'].loc[df.is_oa], name='OPEN', marker_color='#E7664C'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_' + str(method)].loc[~df.is_oa],
                         x=df['cit_group'].loc[~df.is_oa], name='CLOSED', marker_color='gray'))
    fig.update_layout(title='Figure: Box plots of ' + str(method) + ' index on citing ' + str(group)
                            + ' by citation groups for ' + str(year) +
                            '<br><sup>(A total of 56000 papers. '
                            'Each group consists of a sample 2000 OA papers and 2000 non-OA papers)</sup>',
                      xaxis_title="Groups by citation count",
                      yaxis_title=str(method) + " index",
                      boxmode='group')
    return fig


def create_boxplot_div_by_cit_group(af: AnalyticsFunction):
    # create plots for all years, groupings, and diversity metrics
    print('... start boxplot_div_by_cit_group')
    for year in YEARS:
        df_ = pd.read_csv('tempdata/samples_by_cit_group_and_oa_' + str(year) + '.csv', dtype={'cit_group': str})
        df_['cit_group'] = pd.Categorical(df_['cit_group'], ["2", "3", "4", "5-6", "7-9", "10-11", "12-14",
                                                             "15-16", "17-19", "20-23", "24-29", "30-42",
                                                             "43-59", ">=60"])
        df_ = df_.sort_values('cit_group')

        for group in GROUPS:
            for metric in METRICS:
                fig = plot_boxplot_div_by_cit_group(df=df_, method=metric, group=group, year=year)
                if not os.path.exists('report_graphs/box_div_by_cit_group'):
                    os.makedirs('report_graphs/box_div_by_cit_group')
                fig.write_image('report_graphs/box_div_by_cit_group/box_div_by_cit_group_'
                                + metric + '_' + group + '_' + str(year) + '.png', scale=FIG_SCALE, width=FIG_WIDTH,
                                height=FIG_HEIGHT)
                af.add_existing_file('report_graphs/box_div_by_cit_group/box_div_by_cit_group_'
                                     + metric + '_' + group + '_' + str(year) + '.png')
    print('... completed')


def plot_boxplot_div_by_oa_group(df, method='GiniSim', group='Countries', year=2019):
    # input variables method is either GiniSim or Shannon, group is one of Institutions, Countries, Subregions,
    # or Regions or Fields
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_' + str(method)].loc[df.s_noa], name='CLOSED',
                         marker_color='gray'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_' + str(method)].loc[df.s_oa], name='OPEN',
                         marker_color='#E7664C'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_' + str(method)].loc[df.s_gold], name='GOLD',
                         marker_color='#FFD700'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_' + str(method)].loc[df.s_green], name='GREEN',
                         marker_color='#006400'))
    fig.update_layout(
        title='Figure: Box plots of ' + str(method) + ' index on citing ' + str(group) + ' by OA status for '
              + str(year) +
              '<br><sup>(samples of 10000 non-OA, 10000 OA, '
              '10000 gold and 10000 green papers.)</sup>',
        xaxis_title="OA status",
        yaxis_title=str(method) + " index")
    return fig


def create_boxplot_div_by_oa_group(af: AnalyticsFunction):
    # create plots for all years, groupings, and diversity metrics
    print('... start boxplot_div_by_oa_group')
    for year in YEARS:
        df_ = pd.read_csv('tempdata/samples_by_oa_' + str(year) + '.csv')
        df_.fillna(value=False, inplace=True)
        for group in GROUPS:
            for metric in METRICS:
                fig = plot_boxplot_div_by_oa_group(df=df_, method=metric, group=group, year=year)
                if not os.path.exists('report_graphs/box_div_by_oa_group'):
                    os.makedirs('report_graphs/box_div_by_oa_group')
                fig.write_image('report_graphs/box_div_by_oa_group/box_div_by_oa_group_'
                                + metric + '_' + group + '_' + str(year) + '.png', scale=FIG_SCALE, width=FIG_WIDTH,
                                height=FIG_HEIGHT)
                af.add_existing_file('report_graphs/box_div_by_oa_group/box_div_by_oa_group_'
                                     + metric + '_' + group + '_' + str(year) + '.png')
    print('... completed')


def plot_boxplot_uniq_cit_by_cit_group(df, group='Countries', year=2019):
    # input variable group is one of Institutions, Countries, Subregions,
    # or Regions or Fields
    # print(df[df['is_oa'] == True][['CitingCountries_Shannon']])
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_count_uniq'].loc[df.is_oa],
                         x=df['cit_group'].loc[df.is_oa], name='OPEN', marker_color='#E7664C'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_count_uniq'].loc[~df.is_oa],
                         x=df['cit_group'].loc[~df.is_oa], name='CLOSED', marker_color='gray'))
    fig.update_layout(title='Figure: Box plots of number of unique citing ' + str(group)
                            + ' by citation groups for ' + str(year) +
                            '<br><sup>(A total of 56000 papers. '
                            'Each group consists of a sample 2000 OA papers and 2000 non-OA papers)</sup>',
                      xaxis_title="Groups by citation count",
                      yaxis_title="number of unique citing " + str(group),
                      boxmode='group')
    return fig


def create_boxplot_uniq_cit_by_cit_group(af: AnalyticsFunction):
    # create plots for all years, groupings, and diversity metrics
    print('... start boxplot_uniq_cit_by_cit_group')

    for year in YEARS:
        df_ = pd.read_csv('tempdata/samples_by_cit_group_and_oa_' + str(year) + '.csv', dtype={'cit_group': str})
        df_['cit_group'] = pd.Categorical(df_['cit_group'], ["2", "3", "4", "5-6", "7-9", "10-11", "12-14",
                                                             "15-16", "17-19", "20-23", "24-29", "30-42",
                                                             "43-59", ">=60"])
        df_ = df_.sort_values('cit_group')
        for group in GROUPS:
            fig = plot_boxplot_uniq_cit_by_cit_group(df=df_, group=group, year=year)
            if not os.path.exists('report_graphs/box_uniq_cit_by_cit_group'):
                os.makedirs('report_graphs/box_uniq_cit_by_cit_group')
            fig.write_image('report_graphs/box_uniq_cit_by_cit_group/box_uniq_cit_by_cit_group_'
                            + group + '_' + str(year) + '.png', scale=FIG_SCALE, width=FIG_WIDTH, height=FIG_HEIGHT)
            af.add_existing_file('report_graphs/box_uniq_cit_by_cit_group/box_uniq_cit_by_cit_group_'
                                 + group + '_' + str(year) + '.png')
    print('... completed')


def plot_boxplot_uniq_cit_by_oa_group(df, group='Countries', year=2019):
    # input variable group is one of Institutions, Countries, Subregions,
    # or Regions or Fields
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_count_uniq'].loc[df.s_noa], name='CLOSED',
                         marker_color='gray'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_count_uniq'].loc[df.s_oa], name='OPEN',
                         marker_color='#E7664C'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_count_uniq'].loc[df.s_gold], name='GOLD',
                         marker_color='#FFD700'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_count_uniq'].loc[df.s_green], name='GREEN',
                         marker_color='#006400'))
    fig.update_layout(title='Figure: Box plots of number of unique citing ' + str(group) + ' by OA status for '
                            + str(year) +
                            '<br><sup>(samples of 10000 non-OA, 10000 OA, '
                            '10000 gold and 10000 green papers.)</sup>',
                      xaxis_title="OA status",
                      yaxis_title="number of unique citing " + str(group))
    return fig


def create_boxplot_uniq_cit_by_oa_group(af: AnalyticsFunction):
    # create plots for all years, groupings, and diversity metrics
    print('... start boxplot_uniq_cit_by_oa_group')

    for year in YEARS:
        df_ = pd.read_csv('tempdata/samples_by_oa_' + str(year) + '.csv')
        df_.fillna(value=False, inplace=True)
        for group in GROUPS:
            fig = plot_boxplot_uniq_cit_by_oa_group(df=df_, group=group, year=year)
            if not os.path.exists('report_graphs/box_uniq_cit_by_oa_group'):
                os.makedirs('report_graphs/box_uniq_cit_by_oa_group')
            fig.write_image('report_graphs/box_uniq_cit_by_oa_group/box_uniq_cit_by_oa_group_'
                            + group + '_' + str(year) + '.png', scale=FIG_SCALE, width=FIG_WIDTH, height=FIG_HEIGHT)
            af.add_existing_file('report_graphs/box_uniq_cit_by_oa_group/box_uniq_cit_by_oa_group_'
                                 + group + '_' + str(year) + '.png')
    print('... completed')


def plot_line_div_vs_cit_count(df, method='GiniSim', group='Countries', year=2019):
    # input variables method is either GiniSim or Shannon, group is one of Institutions, Countries, Subregions,
    # or Regions or Fields
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['CitationCount'],
                             y=df['Citing' + str(group) + '_' + str(method) + '_perc0'],
                             name='min', line=dict(color='firebrick', dash='dot')))
    fig.add_trace(go.Scatter(x=df['CitationCount'],
                             y=df['Citing' + str(group) + '_' + str(method) + '_perc25'],
                             name='1stQ', line=dict(color='firebrick')))
    fig.add_trace(go.Scatter(x=df['CitationCount'],
                             y=df['Citing' + str(group) + '_' + str(method) + '_perc75'],
                             name='3rdQ', line=dict(color='royalblue')))
    fig.add_trace(go.Scatter(x=df['CitationCount'],
                             y=df['Citing' + str(group) + '_' + str(method) + '_perc100'],
                             name='max', line=dict(color='royalblue', dash='dot')))
    fig.add_trace(go.Scatter(x=df['CitationCount'],
                             y=df['Citing' + str(group) + '_' + str(method) + '_perc50'],
                             name='median', line=dict(color='black', width=3)))
    fig.update_layout(title='Figure: Citation count versus ' + str(method) + ' index of citing ' + str(group) + ' for '
                            + str(year),
                      xaxis_title="Citation count",
                      yaxis_title=str(method) + " index")
    fig.update_layout(xaxis_type='category')
    return fig


def create_line_div_vs_cit_count(af: AnalyticsFunction):
    # create plots for all years, groupings, and diversity metrics
    # Fields exclude due to small numbers
    print('... start line_div_vs_cit_count')

    df_ = pd.read_csv('tempdata/cit_div_vs_cit_count.csv')
    for year in YEARS:
        df_year = df_[df_.year == year]
        df_year = df_year.sort_values('CitationCount')
        for group in GROUPS_NOT_FIELDS:
            for metric in METRICS:
                fig = plot_line_div_vs_cit_count(df=df_year, method=metric, group=group, year=year)
                if not os.path.exists('report_graphs/line_div_vs_cit_count'):
                    os.makedirs('report_graphs/line_div_vs_cit_count')
                filepath = f'report_graphs/line_div_vs_cit_count/line_div_vs_cit_count_{metric}_{group}_{str(year)}.png'
                fig.write_image(filepath, scale=FIG_SCALE, width=FIG_WIDTH, height=FIG_HEIGHT)
                af.add_existing_file(filepath)
    print('... completed')


def plot_bar_div_vs_year(df, method='GiniSim', group='Countries', c_loc='mean'):
    # input variables:
    # metric = 'GiniSim' or 'Shannon';
    # group = Institutions, Countries, Subregions, or Regions or Fields;
    # c_loc = 'mean' or 'median'
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['year'],
                         y=df['noa_' + str(group) + '_' + str(method) + '_' + str(c_loc)],
                         name='CLOSED', line=dict(color='gray')))
    fig.add_trace(go.Scatter(x=df['year'],
                         y=df['oa_' + str(group) + '_' + str(method) + '_' + str(c_loc)],
                         name='OPEN', line=dict(color='#E7664C')))
    fig.add_trace(go.Scatter(x=df['year'],
                         y=df['gold_' + str(group) + '_' + str(method) + '_' + str(c_loc)],
                         name='GOLD', line=dict(color='#FFD700')))
    fig.add_trace(go.Scatter(x=df['year'],
                         y=df['green_' + str(group) + '_' + str(method) + '_' + str(c_loc)],
                         name='GREEN', line=dict(color='#006400')))
    fig.update_layout(title='Figure: The ' + str(c_loc) + ' ' + str(method) + ' index of citing ' + str(group) + ' ',
                      xaxis_title="year",
                      yaxis_title=str(method) + " index")
    fig.update_layout(xaxis_type='category')
    return fig


def create_bar_div_vs_year(af: AnalyticsFunction):
    # create plots for all years, groupings, and diversity metrics
    # data = 'all_papers' or 'atleast2cit'; the latter is used below.
    df_ = pd.read_csv('tempdata/summary_stats_by_year_atleast2cit.csv')

    print('... start bar_div_vs_year')

    for group in GROUPS:
        for metric in METRICS:
            for c_loc in C_LOCS:
                fig = plot_bar_div_vs_year(df=df_, method=metric, group=group, c_loc=c_loc)
                if not os.path.exists('report_graphs/bar_div_vs_year'):
                    os.makedirs('report_graphs/bar_div_vs_year')
                filepath = f'report_graphs/bar_div_vs_year/bar_div_vs_year_{metric}_{group}_{c_loc}.png'
                fig.write_image(filepath, scale=FIG_SCALE, width=FIG_WIDTH, height=FIG_HEIGHT)
                af.add_existing_file(filepath)
    print('... completed')


def create_bar_doi_count_combined(af: AnalyticsFunction):
    # input variables:
    # data = 'all_papers' or 'atleast2cit', latter used here
    df = pd.read_csv('tempdata/summary_stats_by_year_atleast2cit.csv')
    print('... start bar_doi_count_combined')

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['doi_count'],
                         name='doi count', marker_color='grey'))
    fig.update_layout(title='Figure: Annual DOI counts',
                      xaxis_title="year",
                      yaxis_title="doi count")
    fig.update_layout(xaxis_type='category')
    if not os.path.exists('report_graphs/bar_doi_count'):
        os.makedirs('report_graphs/bar_doi_count')
    fig.write_image('report_graphs/bar_doi_count/bar_doi_count_combined.png', scale=FIG_SCALE, width=FIG_WIDTH,
                    height=FIG_HEIGHT)
    af.add_existing_file('report_graphs/bar_doi_count/bar_doi_count_combined.png')
    print('... completed')


def create_bar_doi_count_by_oa(af: AnalyticsFunction):
    # input variables:
    # data = 'all_papers' or 'atleast2cit', latter used here
    df = pd.read_csv('tempdata/summary_stats_by_year_atleast2cit.csv')
    print('... start bar_doi_count_by_oa')

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['noa_count'],
                         name='CLOSED', marker_color='gray'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['oa_count'],
                         name='OPEN', marker_color='#E7664C'))
    fig.update_layout(title='Figure: Annual OA versus non-OA DOI counts',
                      xaxis_title="year",
                      yaxis_title="doi_count")
    fig.update_layout(xaxis_type='category')
    if not os.path.exists('report_graphs/bar_doi_count'):
        os.makedirs('report_graphs/bar_doi_count')
    fig.write_image('report_graphs/bar_doi_count/bar_doi_count_by_oa.png', scale=FIG_SCALE, width=FIG_WIDTH,
                    height=FIG_HEIGHT)
    af.add_existing_file('report_graphs/bar_doi_count/bar_doi_count_by_oa.png')
    print('... completed')


def plot_bar_cit_count_by_oa(df, c_loc='mean'):
    # input variables:
    # c_loc = 'mean' or 'median'
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['year'],
                             y=df['noa_cc_' + str(c_loc)],
                             name='CLOSED', line=dict(color='gray')))
    fig.add_trace(go.Scatter(x=df['year'],
                             y=df['oa_cc_' + str(c_loc)],
                             name='OPEN', line=dict(color='#E7664C')))
    fig.add_trace(go.Scatter(x=df['year'],
                             y=df['gold_cc_' + str(c_loc)],
                             name='GOLD', line=dict(color='#FFD700')))
    fig.add_trace(go.Scatter(x=df['year'],
                             y=df['green_cc_' + str(c_loc)],
                             name='GREEN', line=dict(color='#006400')))
    fig.update_layout(title='Figure: The ' + str(c_loc) + ' citation count per OA category',
                      xaxis_title="year",
                      yaxis_title=str(c_loc) + " citation count")
    fig.update_layout(xaxis_type='category')
    return fig


def create_bar_cit_count_by_oa(af: AnalyticsFunction):
    # create plots for all years, groupings, and diversity metrics
    # data = 'all_papers' or 'atleast2cit'; the latter is used below.
    df_ = pd.read_csv('tempdata/summary_stats_by_year_atleast2cit.csv')

    print('... start bar_cit_count_by_oa')
    for c_loc in C_LOCS:
        fig = plot_bar_cit_count_by_oa(df=df_, c_loc=c_loc)
        if not os.path.exists('report_graphs/bar_cit_count'):
            os.makedirs('report_graphs/bar_cit_count')
        filepath = f'report_graphs/bar_cit_count/bar_cit_count_by_oa_{c_loc}.png'
        fig.write_image(filepath, scale=FIG_SCALE, width=FIG_WIDTH, height=FIG_HEIGHT)
        af.add_existing_file(filepath)
    print('... completed')


def plot_bar_uniq_cit_count(df, group='Countries', c_loc='mean'):
    # input variables:
    # group = Institutions, Countries, Subregions, or Regions or Fields;
    # c_loc = 'mean' or 'median'
    # this only applies to papers with at least 2 citations
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['year'],
                             y=df['noa_' + str(group) + '_uniq_' + str(c_loc)],
                             name='CLOSED', line=dict(color='gray')))
    fig.add_trace(go.Scatter(x=df['year'],
                             y=df['oa_' + str(group) + '_uniq_' + str(c_loc)],
                             name='OPEN', line=dict(color='#E7664C')))
    fig.add_trace(go.Scatter(x=df['year'],
                             y=df['gold_' + str(group) + '_uniq_' + str(c_loc)],
                             name='GOLD', line=dict(color='#FFD700')))
    fig.add_trace(go.Scatter(x=df['year'],
                             y=df['green_' + str(group) + '_uniq_' + str(c_loc)],
                             name='GREEN', line=dict(color='#006400')))
    fig.update_layout(title='Figure: The ' + str(c_loc) + ' number of unique citing ' + str(group),
                      xaxis_title="year",
                      yaxis_title=str(c_loc) + " unique citing " + str(group))
    fig.update_layout(xaxis_type='category')
    return fig


def create_bar_uniq_cit_count(af: AnalyticsFunction):
    # create plots for all years, groupings, and diversity metrics
    # data = 'all_papers' or 'atleast2cit'; the latter is used below.
    df_ = pd.read_csv('tempdata/summary_stats_by_year_atleast2cit.csv')

    print('... start bar_uniq_cit_count')

    for group in GROUPS:
        for c_loc in C_LOCS:
            fig = plot_bar_uniq_cit_count(df=df_, group=group, c_loc=c_loc)
            if not os.path.exists('report_graphs/bar_uniq_cit_count'):
                os.makedirs('report_graphs/bar_uniq_cit_count')
            filepath = f'report_graphs/bar_uniq_cit_count/bar_uniq_cit_count_{group}_{c_loc}.png'
            fig.write_image(filepath, scale=FIG_SCALE, width=FIG_WIDTH, height=FIG_HEIGHT)
            af.add_existing_file(filepath)
    print('... completed')


def plot_line_compare_cit_regions(df, region='Asia'):
    # input variable: region
    # only papers with at least 2 citations are included
    fig = px.line(df, x='year', y='perc_change', color='name',
                  color_discrete_map=COLOR_MAP_REGIONS,
                  category_orders={"name": ORDER_REGIONS})
    fig.update_traces(mode='markers+lines')
    fig.update_layout(legend={"itemsizing": "trace", "itemwidth": 45})
    fig.update_layout(
        title='Figure: % ratios in average citations to papers affiliated to '
              + str(region)
              + '<br><sup>(% ratios are calculated based on citations to OA over non-OA papers)</sup>',
        xaxis_title="Year",
        yaxis_title="% ratios in average citations",
        legend_title_text='Regions')
    return fig


def create_line_compare_cit_regions(af: AnalyticsFunction):
    # create plots for all regions
    data = []
    print('... start plot_line_compare_cit_regions')
    for line in open('tempdata/summary_stats_by_region_atleast2cit.json', 'r'):
        data.append(json.loads(line))
    for region in ORDER_REGIONS:
        data_figure = pd.DataFrame(columns=['name', 'total_oa', 'total_noa', 'perc_change', 'year'])
        for year in YEARS:
            df_oa = [x for x in data if ((x['region'] == region) & (x['year'] == str(year)) & (x['is_oa'] == 'true'))]
            df_noa = [x for x in data if ((x['region'] == region) & (x['year'] == str(year)) & (x['is_oa'] == 'false'))]
            df_oa_doi = int(df_oa[0]['count_doi'])
            df_noa_doi = int(df_noa[0]['count_doi'])
            df_oa = pd.json_normalize(df_oa[0]['CitingRegions_table_all'])
            df_noa = pd.json_normalize(df_noa[0]['CitingRegions_table_all'])
            df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
            df = df.astype({"total_oa": int, "total_noa": int})
            df['perc_change'] = (df['total_oa'] / df_oa_doi) / (df['total_noa'] / df_noa_doi) * 100
            df['year'] = str(year)
            df = pd.DataFrame(df)
            data_figure = pd.concat([data_figure, df])
        fig = plot_line_compare_cit_regions(df=data_figure, region=region)
        if not os.path.exists('report_graphs/line_compare_cit_count_regions'):
            os.makedirs('report_graphs/line_compare_cit_count_regions')
        fig.write_image('report_graphs/line_compare_cit_count_regions/line_compare_cit_count_regions_for_'
                        + region + '.png', scale=FIG_SCALE, width=FIG_WIDTH, height=FIG_HEIGHT)
        af.add_existing_file('report_graphs/line_compare_cit_count_regions/line_compare_cit_count_regions_for_'
                             + region + '.png')
    print('... completed')


def plot_line_compare_cit_subregions(df, subregion='Sub-Saharan Africa'):
    # input variable: subregion
    # only papers with at least 2 citations are included
    fig = px.line(df, x='year', y='perc_change', color='name', line_dash='name',
                  color_discrete_map=COLOR_MAP_SUBREGIONS,
                  line_dash_map=DASH_MAP_SUBREGIONS,
                  category_orders={"name": ORDER_SUBREGIONS})
    fig.update_traces(mode='markers+lines')
    fig.update_layout(legend={"itemsizing": "trace", "itemwidth": 45})
    fig.update_layout(
        title='Figure: % ratios in average citations to papers affiliated to '
              + str(subregion)
              + '<br><sup>(% ratios are calculated based on citations to OA over non-OA papers)</sup>',
        xaxis_title="Year",
        yaxis_title="% ratios in average citations",
        legend_title_text='Subregions')
    return fig


def create_line_compare_cit_subregions(af: AnalyticsFunction):
    # create plots for all subregions
    data = []
    for line in open('tempdata/summary_stats_by_subregion_atleast2cit.json', 'r'):
        data.append(json.loads(line))
    print('... start plot_line_compare_cit_subregions')
    for subregion in ORDER_SUBREGIONS:
        data_figure = pd.DataFrame(columns=['name', 'total_oa', 'total_noa', 'perc_change', 'year'])
        for year in YEARS:
            df_oa = [x for x in data if
                     ((x['subregion'] == subregion) & (x['year'] == str(year)) & (x['is_oa'] == 'true'))]
            df_noa = [x for x in data if
                      ((x['subregion'] == subregion) & (x['year'] == str(year)) & (x['is_oa'] == 'false'))]
            if (len(df_oa) > 0) & (len(df_noa) > 0):
                df_oa_doi = int(df_oa[0]['count_doi'])
                df_noa_doi = int(df_noa[0]['count_doi'])
                df_oa = pd.json_normalize(df_oa[0]['CitingSubregions_table_all'])
                df_noa = pd.json_normalize(df_noa[0]['CitingSubregions_table_all'])
                df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
                df = df.astype({"total_oa": int, "total_noa": int})
                df['perc_change'] = (df['total_oa'] / df_oa_doi) / (df['total_noa'] / df_noa_doi) * 100
                df['year'] = str(year)
                df = pd.DataFrame(df)
                data_figure = pd.concat([data_figure, df])
        fig = plot_line_compare_cit_subregions(df=data_figure, subregion=subregion)
        if not os.path.exists('report_graphs/line_compare_cit_count_subregions'):
            os.makedirs('report_graphs/line_compare_cit_count_subregions')
        fig.write_image('report_graphs/line_compare_cit_count_subregions/line_compare_cit_count_subregions_for_'
                        + subregion + '.png', scale=FIG_SCALE, width=FIG_WIDTH, height=FIG_HEIGHT)
        af.add_existing_file('report_graphs/line_compare_cit_count_subregions/line_compare_cit_count_subregions_for_'
                             + subregion + '.png')
    print('... completed')


def plot_bar_compare_cit_regions(df, region='Asia', year=2019):
    # input variable: region
    # only papers with at least 2 citations are included
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['name'], y=df['perc_change'], marker_color='royalblue'))
    fig.update_layout(title='Figure: % change in total citations to OA/non-OA paper affiliated to ' +
                            str(region) + ' for ' + str(year),
                      xaxis_title="region",
                      yaxis_title="% change in total citations")
    fig.update_layout(xaxis_type='category')
    fig.update_xaxes(categoryorder='category ascending')
    return fig


def create_bar_compare_cit_regions(af: AnalyticsFunction):
    # create plots for all regions
    data = []
    for line in open('tempdata/summary_stats_by_region_atleast2cit.json', 'r'):
        data.append(json.loads(line))
    print('... start plot_bar_compare_cit_regions')
    for region in ORDER_REGIONS:
        for year in YEARS:
            df_oa = [x for x in data if ((x['region'] == region) & (x['year'] == str(year)) & (x['is_oa'] == 'true'))]
            df_noa = [x for x in data if ((x['region'] == region) & (x['year'] == str(year)) & (x['is_oa'] == 'false'))]
            df_oa = pd.json_normalize(df_oa[0]['CitingRegions_table_all'])
            df_noa = pd.json_normalize(df_noa[0]['CitingRegions_table_all'])
            df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
            df = df.astype({"total_oa": int, "total_noa": int})
            df['perc_change'] = (df['total_oa'] - df['total_noa']) / df['total_noa'] * 100
            fig = plot_bar_compare_cit_regions(df, region=region, year=year)
            if not os.path.exists('report_graphs/bar_compare_cit_regions'):
                os.makedirs('report_graphs/bar_compare_cit_regions')
            fig.write_image('report_graphs/bar_compare_cit_regions/bar_compare_cit_regions_for_'
                            + region + '_' + str(year) + '.png', scale=FIG_SCALE, width=FIG_WIDTH, height=FIG_HEIGHT)
            af.add_existing_file(
                'report_graphs/bar_compare_cit_regions/bar_compare_cit_regions_for_'
                + region + '_' + str(year) + '.png')
    print('... completed')


def plot_bar_compare_cit_subregions(df, subregion='Sub-Saharan Africa', year=2019):
    # input variable: subregion
    # only papers with at least 2 citations are included
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['name'], y=df['perc_change'], marker_color='royalblue'))
    fig.update_layout(title='Figure: % change in total citations to OA/non-OA paper affiliated to ' +
                            str(subregion) + ' for ' + str(year),
                      xaxis_title="subregion",
                      yaxis_title="% change in total citations")
    fig.update_layout(xaxis_type='category')
    fig.update_xaxes(categoryorder='category ascending')
    return fig


def create_bar_compare_cit_subregions(af: AnalyticsFunction):
    # create plots for all regions
    data = []
    for line in open('tempdata/summary_stats_by_subregion_atleast2cit.json', 'r'):
        data.append(json.loads(line))
    print('... start plot_bar_compare_cit_subregions')
    for subregion in ORDER_SUBREGIONS:
        for year in YEARS:
            df_oa = [x for x in data if
                     ((x['subregion'] == subregion) & (x['year'] == str(year)) & (x['is_oa'] == 'true'))]
            df_noa = [x for x in data if
                      ((x['subregion'] == subregion) & (x['year'] == str(year)) & (x['is_oa'] == 'false'))]
            if (len(df_oa) > 0) & (len(df_noa) > 0):
                df_oa = pd.json_normalize(df_oa[0]['CitingSubregions_table_all'])
                df_noa = pd.json_normalize(df_noa[0]['CitingSubregions_table_all'])
                df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
                df = df.astype({"total_oa": int, "total_noa": int})
                df['perc_change'] = (df['total_oa'] - df['total_noa']) / df['total_noa'] * 100
                fig = plot_bar_compare_cit_subregions(df, subregion=subregion, year=year)
                if not os.path.exists('report_graphs/bar_compare_cit_subregions'):
                    os.makedirs('report_graphs/bar_compare_cit_subregions')
                fig.write_image('report_graphs/bar_compare_cit_subregions/bar_compare_cit_subregions_for_'
                                + subregion + '_' + str(year) + '.png', scale=FIG_SCALE, width=FIG_WIDTH,
                                height=FIG_HEIGHT)
                af.add_existing_file(
                    'report_graphs/bar_compare_cit_subregions/bar_compare_cit_subregions_for_'
                    + subregion + '_' + str(year) + '.png')
    print('... completed')


def create_figure2a(af: AnalyticsFunction):
    # create plot for panel A of figure 1 of main text
    df = pd.read_csv('tempdata/summary_stats_by_year_atleast2cit.csv')
    print('... start figure2a')
    fig = make_subplots(rows=1, cols=1, y_title="Shannon score")
    fig.add_trace(go.Scatter(x=df['year'], y=df['noa_Institutions_Shannon_median'],
                             name='CLOSED', marker_color='gray'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['year'], y=df['oa_Institutions_Shannon_median'],
                             name='OPEN', marker_color='#E7664C'), row=1, col=1)
    fig.update_xaxes(tickangle=270)
    fig.update_layout(title='Fig. 2A: Median Shannon scores (Institutions)')
    fig.update_layout(xaxis_type='category')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="right",
        x=1
    ))
    if not os.path.exists('report_graphs/figure2'):
        os.makedirs('report_graphs/figure2')
    fig.write_image('report_graphs/figure2/figure2a.png', scale=FIG_SCALE, width=500, height=320)
    af.add_existing_file('report_graphs/figure2/figure2a.png')
    print('... completed')


def create_figure2b(af: AnalyticsFunction):
    # create plot for panel B of figure 1 of main text
    df = pd.read_csv('tempdata/summary_stats_by_year_atleast2cit.csv')
    print('... start figure2b')
    fig = make_subplots(rows=4, cols=1, subplot_titles=("Countries", "Subregions", "Regions", "Fields"),
                        shared_xaxes=True, vertical_spacing=0.04, y_title="Shannon score")

    fig.add_trace(go.Scatter(x=df['year'], y=df['noa_Countries_Shannon_mean'],
                             name='CLOSED', marker_color='gray', showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['year'], y=df['oa_Countries_Shannon_mean'],
                             name='OPEN', marker_color='#E7664C', showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['year'], y=df['gold_Countries_Shannon_mean'],
                             name='GOLD', marker_color='#FFD700', showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['year'], y=df['green_Countries_Shannon_mean'],
                             name='GREEN', marker_color='#006400', showlegend=False), row=1, col=1)

    fig.add_trace(go.Scatter(x=df['year'], y=df['noa_Subregions_Shannon_mean'],
                             name='CLOSED', marker_color='gray', showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=df['year'], y=df['oa_Subregions_Shannon_mean'],
                             name='OPEN', marker_color='#E7664C', showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=df['year'], y=df['gold_Subregions_Shannon_mean'],
                             name='GOLD', marker_color='#FFD700', showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=df['year'], y=df['green_Subregions_Shannon_mean'],
                             name='GREEN', marker_color='#006400', showlegend=False), row=2, col=1)

    fig.add_trace(go.Scatter(x=df['year'], y=df['noa_Regions_Shannon_mean'],
                             name='CLOSED', marker_color='gray', showlegend=False), row=3, col=1)
    fig.add_trace(go.Scatter(x=df['year'], y=df['oa_Regions_Shannon_mean'],
                             name='OPEN', marker_color='#E7664C', showlegend=False), row=3, col=1)
    fig.add_trace(go.Scatter(x=df['year'], y=df['gold_Regions_Shannon_mean'],
                             name='GOLD', marker_color='#FFD700', showlegend=False), row=3, col=1)
    fig.add_trace(go.Scatter(x=df['year'], y=df['green_Regions_Shannon_mean'],
                             name='GREEN', marker_color='#006400', showlegend=False), row=3, col=1)

    fig.add_trace(go.Scatter(x=df['year'], y=df['noa_Fields_Shannon_mean'],
                             name='CLOSED', marker_color='gray'), row=4, col=1)
    fig.add_trace(go.Scatter(x=df['year'], y=df['oa_Fields_Shannon_mean'],
                             name='OPEN', marker_color='#E7664C'), row=4, col=1)
    fig.add_trace(go.Scatter(x=df['year'], y=df['gold_Fields_Shannon_mean'],
                             name='GOLD', marker_color='#FFD700'), row=4, col=1)
    fig.add_trace(go.Scatter(x=df['year'], y=df['green_Fields_Shannon_mean'],
                             name='GREEN', marker_color='#006400'), row=4, col=1)

    fig.update_xaxes(tickangle=270)
    fig.update_layout(title='Fig. 2B: Mean Shannon scores')
    fig.update_layout(xaxis_type='category')
    fig.update_layout(xaxis4=dict(tickvals=YEARS))
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.029,
        xanchor="right",
        x=1
    ))
    if not os.path.exists('report_graphs/figure2'):
        os.makedirs('report_graphs/figure2')
    fig.write_image('report_graphs/figure2/figure2b.png', scale=FIG_SCALE, width=500, height=700)
    af.add_existing_file('report_graphs/figure2/figure2b.png')
    print('... completed')


def create_figure2c(af: AnalyticsFunction):
    # create plot for panel C of figure 2 of main text
    print('... start figure2c')

    df = pd.read_csv('tempdata/samples_by_oa_2019.csv')
    df.fillna(value=False, inplace=True)
    method = "Shannon"
    group_labels = ["CLOSED", "OPEN"]
    fig = make_subplots(rows=5, cols=1, subplot_titles=GROUPS, vertical_spacing=0.05,
                        y_title="Probability density / Frequency", x_title=method + " score")

    for subplot_count in list(range(len(GROUPS))):
        x1 = df['Citing' + str(GROUPS[subplot_count]) + '_' +
                str(method)].loc[df['Citing' + str(GROUPS[subplot_count]) + '_' + str(method)] > 0].loc[df.s_noa]
        x1 = x1.astype(float)
        x2 = df['Citing' + str(GROUPS[subplot_count]) + '_' +
                str(method)].loc[df['Citing' + str(GROUPS[subplot_count]) + '_' + str(method)] > 0].loc[df.s_oa]
        x2 = x2.astype(float)
        hist_data = [x1, x2]
        bin1 = max(x1)/50
        bin2 = max(x2)/50
        if subplot_count == len(GROUPS)-1:
            print_legend = True
        else:
            print_legend = False
        fig_sub = ff.create_distplot(hist_data, group_labels, show_hist=True, bin_size=[bin1, bin2], show_rug=False)
        fig.add_trace(go.Histogram(fig_sub['data'][0], marker_color='gray', opacity=.3, showlegend=False),
                      row=subplot_count+1, col=1)
        fig.add_trace(go.Histogram(fig_sub['data'][1], marker_color='#E7664C', opacity=.3, showlegend=False),
                      row=subplot_count+1, col=1)
        fig.add_trace(go.Scatter(fig_sub['data'][2], line=dict(color='gray', width=2), showlegend=print_legend),
                      row=subplot_count+1, col=1)
        fig.add_trace(go.Scatter(fig_sub['data'][3], line=dict(color='#E7664C', width=2), showlegend=print_legend),
                      row=subplot_count+1, col=1)

    fig.update_layout(barmode='overlay')
    fig.update_layout(title='Fig. 2C: KDE on ' + method + ' scores based on samples')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    if not os.path.exists('report_graphs/figure2'):
        os.makedirs('report_graphs/figure2')
    fig.write_image('report_graphs/figure2/figure2c.png', scale=FIG_SCALE, width=500, height=1020)
    af.add_existing_file('report_graphs/figure2/figure2c.png')
    print('... completed')


def create_figure3a(af: AnalyticsFunction):
    # create plots for selected subregions
    # specify which subregions to show
    subregions_compare = ['Northern Europe', 'Sub-Saharan Africa', 'Eastern Asia']
    data = []
    for line in open('tempdata/summary_stats_by_subregion_atleast2cit.json', 'r'):
        data.append(json.loads(line))
    print('... start figure3a')
    # create fig space with 3 subplots
    fig = make_subplots(rows=3, cols=1, subplot_titles=["Citations to " + subregions_compare[0],
                                                        "Citations to " + subregions_compare[1],
                                                        "Citations to " + subregions_compare[2]],
                        vertical_spacing=0.1, y_title="% change in total citations",
                        shared_xaxes=True)
    # bar plot for subregion 1
    df_oa = [x for x in data if
             ((x['subregion'] == subregions_compare[0]) & (x['year'] == '2019') & (x['is_oa'] == 'true'))]
    df_noa = [x for x in data if
              ((x['subregion'] == subregions_compare[0]) & (x['year'] == '2019') & (x['is_oa'] == 'false'))]
    if (len(df_oa) > 0) & (len(df_noa) > 0):
        df_oa = pd.json_normalize(df_oa[0]['CitingSubregions_table_all'])
        df_noa = pd.json_normalize(df_noa[0]['CitingSubregions_table_all'])
        df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
        df = df.astype({"total_oa": int, "total_noa": int})
        df['perc_change'] = (df['total_oa'] - df['total_noa']) / df['total_noa'] * 100
        df = df[df.name.isin(subregions_compare)]
        fig.add_trace(go.Bar(x=df['name'], y=df['perc_change'], marker_color='royalblue', showlegend=False), row=1,
                      col=1)
    # bar plot for subregion 2
    df_oa = [x for x in data if
             ((x['subregion'] == subregions_compare[1]) & (x['year'] == '2019') & (x['is_oa'] == 'true'))]
    df_noa = [x for x in data if
              ((x['subregion'] == subregions_compare[1]) & (x['year'] == '2019') & (x['is_oa'] == 'false'))]
    if (len(df_oa) > 0) & (len(df_noa) > 0):
        df_oa = pd.json_normalize(df_oa[0]['CitingSubregions_table_all'])
        df_noa = pd.json_normalize(df_noa[0]['CitingSubregions_table_all'])
        df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
        df = df.astype({"total_oa": int, "total_noa": int})
        df['perc_change'] = (df['total_oa'] - df['total_noa']) / df['total_noa'] * 100
        df = df[df.name.isin(subregions_compare)]
        fig.add_trace(go.Bar(x=df['name'], y=df['perc_change'], marker_color='royalblue', showlegend=False), row=2,
                      col=1)
    # bar plot for subregion 3
    df_oa = [x for x in data if
             ((x['subregion'] == subregions_compare[2]) & (x['year'] == '2019') & (x['is_oa'] == 'true'))]
    df_noa = [x for x in data if
              ((x['subregion'] == subregions_compare[2]) & (x['year'] == '2019') & (x['is_oa'] == 'false'))]
    if (len(df_oa) > 0) & (len(df_noa) > 0):
        df_oa = pd.json_normalize(df_oa[0]['CitingSubregions_table_all'])
        df_noa = pd.json_normalize(df_noa[0]['CitingSubregions_table_all'])
        df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
        df = df.astype({"total_oa": int, "total_noa": int})
        df['perc_change'] = (df['total_oa'] - df['total_noa']) / df['total_noa'] * 100
        df = df[df.name.isin(subregions_compare)]
        fig.add_trace(go.Bar(x=df['name'], y=df['perc_change'], marker_color='royalblue', showlegend=False), row=3,
                      col=1)
    fig.update_layout(xaxis_type='category')
    fig.update_xaxes(categoryorder='category ascending')
    fig.update_layout(title='Fig. 3A: % change in citations for 2019')
    if not os.path.exists('report_graphs/figure3'):
        os.makedirs('report_graphs/figure3')
    fig.write_image('report_graphs/figure3/figure3a.png', scale=FIG_SCALE, width=370, height=700)
    af.add_existing_file('report_graphs/figure3/figure3a.png')
    print('... completed')


def create_figure3b(af: AnalyticsFunction):
    # create plots for selected subregions
    # specify subregions to show
    subregions_compare = ['Northern Europe', 'Sub-Saharan Africa', 'Eastern Asia']
    data = []
    for line in open('tempdata/summary_stats_by_subregion_atleast2cit.json', 'r'):
        data.append(json.loads(line))
    print('... start figure3b')
    fig = make_subplots(rows=3, cols=1, subplot_titles=subregions_compare,
                        vertical_spacing=0.08, y_title="% ratios in average citations")
    # data and plot for subregion 1
    data_figure = pd.DataFrame(columns=['name', 'total_oa', 'total_noa', 'perc_change', 'year'])
    for year in YEARS:
        df_oa = [x for x in data if
                 ((x['subregion'] == subregions_compare[0]) & (x['year'] == str(year)) & (x['is_oa'] == 'true'))]
        df_noa = [x for x in data if
                  ((x['subregion'] == subregions_compare[0]) & (x['year'] == str(year)) & (x['is_oa'] == 'false'))]
        if (len(df_oa) > 0) & (len(df_noa) > 0):
            df_oa_doi = int(df_oa[0]['count_doi'])
            df_noa_doi = int(df_noa[0]['count_doi'])
            df_oa = pd.json_normalize(df_oa[0]['CitingSubregions_table_all'])
            df_noa = pd.json_normalize(df_noa[0]['CitingSubregions_table_all'])
            df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
            df = df.astype({"total_oa": int, "total_noa": int})
            df['perc_change'] = (df['total_oa'] / df_oa_doi) / (df['total_noa'] / df_noa_doi) * 100
            df['year'] = str(year)
            df = pd.DataFrame(df)
            data_figure = pd.concat([data_figure, df])
    data_figure1 = data_figure[data_figure.name == subregions_compare[0]]
    fig.add_trace(go.Scatter(x=data_figure1['year'], y=data_figure1['perc_change'],
                             name=subregions_compare[0], marker_color=COLOR_MAP_SUBREGIONS[subregions_compare[0]]),
                  row=1, col=1)
    data_figure1 = data_figure[data_figure.name == subregions_compare[1]]
    fig.add_trace(go.Scatter(x=data_figure1['year'], y=data_figure1['perc_change'],
                             name=subregions_compare[1], marker_color=COLOR_MAP_SUBREGIONS[subregions_compare[1]]),
                  row=1, col=1)
    data_figure1 = data_figure[data_figure.name == subregions_compare[2]]
    fig.add_trace(go.Scatter(x=data_figure1['year'], y=data_figure1['perc_change'],
                             name=subregions_compare[2], marker_color=COLOR_MAP_SUBREGIONS[subregions_compare[2]]),
                  row=1, col=1)
    # data and plot for subregion 2
    data_figure = pd.DataFrame(columns=['name', 'total_oa', 'total_noa', 'perc_change', 'year'])
    for year in YEARS:
        df_oa = [x for x in data if
                 ((x['subregion'] == subregions_compare[1]) & (x['year'] == str(year)) & (x['is_oa'] == 'true'))]
        df_noa = [x for x in data if
                  ((x['subregion'] == subregions_compare[1]) & (x['year'] == str(year)) & (x['is_oa'] == 'false'))]
        if (len(df_oa) > 0) & (len(df_noa) > 0):
            df_oa_doi = int(df_oa[0]['count_doi'])
            df_noa_doi = int(df_noa[0]['count_doi'])
            df_oa = pd.json_normalize(df_oa[0]['CitingSubregions_table_all'])
            df_noa = pd.json_normalize(df_noa[0]['CitingSubregions_table_all'])
            df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
            df = df.astype({"total_oa": int, "total_noa": int})
            df['perc_change'] = (df['total_oa'] / df_oa_doi) / (df['total_noa'] / df_noa_doi) * 100
            df['year'] = str(year)
            df = pd.DataFrame(df)
            data_figure = pd.concat([data_figure, df])
    data_figure1 = data_figure[data_figure.name == subregions_compare[0]]
    fig.add_trace(go.Scatter(x=data_figure1['year'], y=data_figure1['perc_change'],
                             name=subregions_compare[0], marker_color=COLOR_MAP_SUBREGIONS[subregions_compare[0]],
                             showlegend=False),
                  row=2, col=1)
    data_figure1 = data_figure[data_figure.name == subregions_compare[1]]
    fig.add_trace(go.Scatter(x=data_figure1['year'], y=data_figure1['perc_change'],
                             name=subregions_compare[1], marker_color=COLOR_MAP_SUBREGIONS[subregions_compare[1]],
                             showlegend=False),
                  row=2, col=1)
    data_figure1 = data_figure[data_figure.name == subregions_compare[2]]
    fig.add_trace(go.Scatter(x=data_figure1['year'], y=data_figure1['perc_change'],
                             name=subregions_compare[2], marker_color=COLOR_MAP_SUBREGIONS[subregions_compare[2]],
                             showlegend=False),
                  row=2, col=1)
    # data and plot for subregion 3
    data_figure = pd.DataFrame(columns=['name', 'total_oa', 'total_noa', 'perc_change', 'year'])
    for year in YEARS:
        df_oa = [x for x in data if
                 ((x['subregion'] == subregions_compare[2]) & (x['year'] == str(year)) & (x['is_oa'] == 'true'))]
        df_noa = [x for x in data if
                  ((x['subregion'] == subregions_compare[2]) & (x['year'] == str(year)) & (x['is_oa'] == 'false'))]
        if (len(df_oa) > 0) & (len(df_noa) > 0):
            df_oa_doi = int(df_oa[0]['count_doi'])
            df_noa_doi = int(df_noa[0]['count_doi'])
            df_oa = pd.json_normalize(df_oa[0]['CitingSubregions_table_all'])
            df_noa = pd.json_normalize(df_noa[0]['CitingSubregions_table_all'])
            df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
            df = df.astype({"total_oa": int, "total_noa": int})
            df['perc_change'] = (df['total_oa'] / df_oa_doi) / (df['total_noa'] / df_noa_doi) * 100
            df['year'] = str(year)
            df = pd.DataFrame(df)
            data_figure = pd.concat([data_figure, df])
    data_figure1 = data_figure[data_figure.name == subregions_compare[0]]
    fig.add_trace(go.Scatter(x=data_figure1['year'], y=data_figure1['perc_change'],
                             name=subregions_compare[0], marker_color=COLOR_MAP_SUBREGIONS[subregions_compare[0]],
                             showlegend=False),
                  row=3, col=1)
    data_figure1 = data_figure[data_figure.name == subregions_compare[1]]
    fig.add_trace(go.Scatter(x=data_figure1['year'], y=data_figure1['perc_change'],
                             name=subregions_compare[1], marker_color=COLOR_MAP_SUBREGIONS[subregions_compare[1]],
                             showlegend=False),
                  row=3, col=1)
    data_figure1 = data_figure[data_figure.name == subregions_compare[2]]
    fig.add_trace(go.Scatter(x=data_figure1['year'], y=data_figure1['perc_change'],
                             name=subregions_compare[2], marker_color=COLOR_MAP_SUBREGIONS[subregions_compare[2]],
                             showlegend=False),
                  row=3, col=1)

    fig.update_traces(mode='markers+lines')
    fig.update_layout(legend={"itemsizing": "trace", "itemwidth": 45})
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.029,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        title='Fig. 3B: % ratios in average citations for all years ')
    if not os.path.exists('report_graphs/figure3'):
        os.makedirs('report_graphs/figure3')
    fig.write_image('report_graphs/figure3/figure3b.png', scale=FIG_SCALE, width=630, height=700)
    af.add_existing_file('report_graphs/figure3/figure3b.png')
    print('... completed')


def plot_line_div_by_field(df, field='Art', method='GiniSim', group='Countries', c_loc='median'):
    # input variables method is either GiniSim or Shannon, group is one of Institutions, Countries, Subregions,
    # or Regions or Fields
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['year'],
                             y=df['noa_Citing' + str(group) + '_' + str(method) + '_' + c_loc],
                             name='CLOSED', line=dict(color='gray')))
    fig.add_trace(go.Scatter(x=df['year'],
                             y=df['oa_Citing' + str(group) + '_' + str(method) + '_' + c_loc],
                             name='OPEN', line=dict(color='#E7664C')))
    fig.add_trace(go.Scatter(x=df['year'],
                             y=df['gold_Citing' + str(group) + '_' + str(method) + '_' + c_loc],
                             name='GOLD', line=dict(color='#FFD700')))
    fig.add_trace(go.Scatter(x=df['year'],
                             y=df['green_Citing' + str(group) + '_' + str(method) + '_' + c_loc],
                             name='GREEN', line=dict(color='#006400')))
    fig.update_layout(title='Figure: Comparing ' + c_loc + ' ' + str(method) + ' on citing ' + str(group) +
                            ' for ' + field,
                      xaxis_title="year",
                      yaxis_title=str(method) + " index")
    fig.update_layout(xaxis_type='category')
    return fig


def create_line_div_by_field(af: AnalyticsFunction):
    # create plots for all years, groupings, and diversity metrics
    # Fields exclude due to small numbers
    print('... start line_div_by_field')
    df_ = pd.read_csv('tempdata/cit_div_by_field.csv')
    fields = df_['field'].unique()
    for field in fields:
        for group in GROUPS:
            for metric in METRICS:
                for c_loc in C_LOCS:
                    fig = plot_line_div_by_field(df=df_[df_["field"] == field], field=field, method=metric, group=group, c_loc=c_loc)
                    if not os.path.exists('report_graphs/line_div_by_field'):
                        os.makedirs('report_graphs/line_div_by_field')
                    filepath = f'report_graphs/line_div_by_field/line_div_by_field_{field}_{group}_{metric}_{c_loc}.png'
                    fig.write_image(filepath, scale=FIG_SCALE, width=FIG_WIDTH, height=FIG_HEIGHT)
                    af.add_existing_file(filepath)
    print('... completed')


def plot_kde_dist_on_cit_div(df, bin1, bin2, method, group, year):
    # plot kde graphs for selected data range
    # input variable: data, labels, bin sizes
    oa_labels = ["CLOSED", "OPEN"]
    oa_colors = ["gray", "#E7664C"]
    fig = ff.create_distplot(df, oa_labels, show_hist=True, bin_size=[bin1, bin2], show_rug=False, colors=oa_colors)
    fig.update_layout(barmode='overlay')
    fig.update_layout(title='Figure: KDE of ' + method + ' scores on citing ' + group + ' for ' + str(year))
    return fig


def create_kde_dist_on_cit_div(af: AnalyticsFunction):
    # create kde plots for citation diversity comparing oa categories
    print('... start kde_dist_on_cit_div')

    for year in YEARS:
        df = pd.read_csv('tempdata/samples_by_oa_'+str(year)+'.csv')
        df.fillna(value=False, inplace=True)
        for group in GROUPS:
            for metric in METRICS:
                x1 = df['Citing' + str(group) + '_' + str(metric)].loc[df.s_noa]
                x1 = x1.astype(float)
                x2 = df['Citing' + str(group) + '_' + str(metric)].loc[df.s_oa]
                x2 = x2.astype(float)
                hist_data = [x1, x2]
                bin1 = max(x1)/50
                bin2 = max(x2)/50
                fig = plot_kde_dist_on_cit_div(df=hist_data, bin1=bin1, bin2=bin2, method=metric, group=group,
                                               year=year)
                if not os.path.exists('report_graphs/kde_dist_on_cit_div'):
                    os.makedirs('report_graphs/kde_dist_on_cit_div')
                filepath = f'report_graphs/kde_dist_on_cit_div/kde_dist_on_cit_div_{metric}_{group}_{year}.png'
                fig.write_image(filepath, scale=FIG_SCALE, width=FIG_WIDTH, height=FIG_HEIGHT)
                af.add_existing_file(filepath)
    print('... completed')






if __name__ == '__main__':
    process_sql_templates_to_queries(af='mock', rerun=True)