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

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Optional, Callable, Union

from google.cloud import bigquery

from observatory.reports import report_utils
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


def calculate_citation_diversity(af: AnalyticsFunction,
                                 rerun: bool = False,
                                 verbose: bool = True):
    """
    Run global_citations_query.sql to generate article level citation diversity data
    """

    query = load_sql_to_string('global_citation_query.sql',
                               parameters=dict(
                                   first_year=years[0],
                                   last_year=years[-1],
                                   doi_table=DOI_TABLE,
                                   mag_references_table=MAG_REFERENCES_TABLE
                               ),
                               directory="report_data_processing/sql")

    if not report_utils.bigquery_rerun(af, rerun, verbose):
        print(f"""Query is:            
            {query}

            """)
        print(f'Destination Table: {MAG_REFERENCES_TABLE}')
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
        query = load_sql_to_string('cit_div_vs_cit_count.sql',
                                   parameters=dict(year=year),
                                   directory='report_data_processing/sql')


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
                         x=df['cit_group'].loc[df.is_oa], name='OA'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_' + str(method)].loc[~df.is_oa],
                         x=df['cit_group'].loc[~df.is_oa], name='not OA'))
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
    for year in years:
        df_ = pd.read_csv('tempdata/samples_by_cit_group_and_oa_' + str(year) + '.csv', dtype={'cit_group': str})
        df_['cit_group'] = pd.Categorical(df_['cit_group'], ["2", "3", "4", "5-6", "7-9", "10-11", "12-14",
                                                             "15-16", "17-19", "20-23", "24-29", "30-42",
                                                             "43-59", ">=60"])
        df_ = df_.sort_values('cit_group')
        for group in groups:
            for metric in metrics:
                fig = plot_boxplot_div_by_cit_group(df=df_, method=metric, group=group, year=year)
                if not os.path.exists('report_graphs/box_div_by_cit_group'):
                    os.makedirs('report_graphs/box_div_by_cit_group')
                fig.write_image('report_graphs/box_div_by_cit_group/box_div_by_cit_group_'
                                + metric + '_' + group + '_' + str(year) + '.png', scale=scale, width=width,
                                height=height)
                af.add_existing_file('report_graphs/box_div_by_cit_group/box_div_by_cit_group_'
                                     + metric + '_' + group + '_' + str(year) + '.png')


def plot_boxplot_div_by_oa_group(df, method='GiniSim', group='Countries', year=2019):
    # input variables method is either GiniSim or Shannon, group is one of Institutions, Countries, Subregions,
    # or Regions or Fields
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_' + str(method)].loc[df.s_noa], name='not OA',
                         marker_color='indianred'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_' + str(method)].loc[df.s_oa], name='OA',
                         marker_color='royalblue'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_' + str(method)].loc[df.s_gold], name='gold OA',
                         marker_color='darkgoldenrod'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_' + str(method)].loc[df.s_green], name='green OA',
                         marker_color='darkgreen'))
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
    for year in years:
        df_ = pd.read_csv('tempdata/samples_by_oa_' + str(year) + '.csv')
        df_.fillna(value=False, inplace=True)
        for group in groups:
            for metric in metrics:
                fig = plot_boxplot_div_by_oa_group(df=df_, method=metric, group=group, year=year)
                if not os.path.exists('report_graphs/box_div_by_oa_group'):
                    os.makedirs('report_graphs/box_div_by_oa_group')
                fig.write_image('report_graphs/box_div_by_oa_group/box_div_by_oa_group_'
                                + metric + '_' + group + '_' + str(year) + '.png', scale=scale, width=width,
                                height=height)
                af.add_existing_file('report_graphs/box_div_by_oa_group/box_div_by_oa_group_'
                                     + metric + '_' + group + '_' + str(year) + '.png')


def plot_boxplot_uniq_cit_by_cit_group(df, group='Countries', year=2019):
    # input variable group is one of Institutions, Countries, Subregions,
    # or Regions or Fields

    # print(df[df['is_oa'] == True][['CitingCountries_Shannon']])
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_count_uniq'].loc[df.is_oa],
                         x=df['cit_group'].loc[df.is_oa], name='OA'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_count_uniq'].loc[~df.is_oa],
                         x=df['cit_group'].loc[~df.is_oa], name='not OA'))
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
    for year in years:
        df_ = pd.read_csv('tempdata/samples_by_cit_group_and_oa_' + str(year) + '.csv', dtype={'cit_group': str})
        df_['cit_group'] = pd.Categorical(df_['cit_group'], ["2", "3", "4", "5-6", "7-9", "10-11", "12-14",
                                                             "15-16", "17-19", "20-23", "24-29", "30-42",
                                                             "43-59", ">=60"])
        df_ = df_.sort_values('cit_group')
        for group in groups:
            fig = plot_boxplot_uniq_cit_by_cit_group(df=df_, group=group, year=year)
            if not os.path.exists('report_graphs/box_uniq_cit_by_cit_group'):
                os.makedirs('report_graphs/box_uniq_cit_by_cit_group')
            fig.write_image('report_graphs/box_uniq_cit_by_cit_group/box_uniq_cit_by_cit_group_'
                            + group + '_' + str(year) + '.png', scale=scale, width=width, height=height)
            af.add_existing_file('report_graphs/box_uniq_cit_by_cit_group/box_uniq_cit_by_cit_group_'
                                 + group + '_' + str(year) + '.png')


def plot_boxplot_uniq_cit_by_oa_group(df, group='Countries', year=2019):
    # input variable group is one of Institutions, Countries, Subregions,
    # or Regions or Fields
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_count_uniq'].loc[df.s_noa], name='not OA',
                         marker_color='indianred'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_count_uniq'].loc[df.s_oa], name='OA',
                         marker_color='royalblue'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_count_uniq'].loc[df.s_gold], name='gold OA',
                         marker_color='darkgoldenrod'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_count_uniq'].loc[df.s_green], name='green OA',
                         marker_color='darkgreen'))
    fig.update_layout(title='Figure: Box plots of number of unique citing ' + str(group) + ' by OA status for '
                            + str(year) +
                            '<br><sup>(samples of 10000 non-OA, 10000 OA, '
                            '10000 gold and 10000 green papers.)</sup>',
                      xaxis_title="OA status",
                      yaxis_title="number of unique citing " + str(group))
    return fig


def create_boxplot_uniq_cit_by_oa_group(af: AnalyticsFunction):
    # create plots for all years, groupings, and diversity metrics
    for year in years:
        df_ = pd.read_csv('tempdata/samples_by_oa_' + str(year) + '.csv')
        df_.fillna(value=False, inplace=True)
        for group in groups:
            fig = plot_boxplot_uniq_cit_by_oa_group(df=df_, group=group, year=year)
            if not os.path.exists('report_graphs/box_uniq_cit_by_oa_group'):
                os.makedirs('report_graphs/box_uniq_cit_by_oa_group')
            fig.write_image('report_graphs/box_uniq_cit_by_oa_group/box_uniq_cit_by_oa_group_'
                            + group + '_' + str(year) + '.png', scale=scale, width=width, height=height)
            af.add_existing_file('report_graphs/box_uniq_cit_by_oa_group/box_uniq_cit_by_oa_group_'
                                 + group + '_' + str(year) + '.png')


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
    groups_ = groups
    groups_.remove('Fields')
    for year in years:
        df_ = pd.read_csv('tempdata/cit_div_vs_cit_count_' + str(year) + '.csv')
        df_ = df_.sort_values('CitationCount')
        for group in groups_:
            for metric in metrics:
                fig = plot_line_div_vs_cit_count(df=df_, method=metric, group=group, year=year)
                if not os.path.exists('report_graphs/line_div_vs_cit_count'):
                    os.makedirs('report_graphs/line_div_vs_cit_count')
                fig.write_image('report_graphs/line_div_vs_cit_count/line_div_vs_cit_count_'
                                + metric + '_' + group + '_' + str(year) + '.png', scale=scale, width=width,
                                height=height)
                af.add_existing_file('report_graphs/line_div_vs_cit_count/line_div_vs_cit_count_'
                                     + metric + '_' + group + '_' + str(year) + '.png')


def plot_bar_div_vs_year(df, method='GiniSim', group='Countries', c_loc='mean'):
    # input variables:
    # metric = 'GiniSim' or 'Shannon';
    # group = Institutions, Countries, Subregions, or Regions or Fields;
    # c_loc = 'mean' or 'median'
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['noa_' + str(group) + '_' + str(method) + '_' + str(c_loc)],
                         name='not OA', marker_color='indianred'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['oa_' + str(group) + '_' + str(method) + '_' + str(c_loc)],
                         name='OA', marker_color='royalblue'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['gold_' + str(group) + '_' + str(method) + '_' + str(c_loc)],
                         name='gold OA', marker_color='darkgoldenrod'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['green_' + str(group) + '_' + str(method) + '_' + str(c_loc)],
                         name='green OA', marker_color='darkgreen'))
    fig.update_layout(title='Figure: The ' + str(c_loc) + ' ' + str(method) + ' index of citing ' + str(group) + ' ',
                      xaxis_title="year",
                      yaxis_title=str(method) + " index")
    fig.update_layout(xaxis_type='category')
    return fig


def create_bar_div_vs_year(af: AnalyticsFunction):
    # create plots for all years, groupings, and diversity metrics
    # data = 'all_papers' or 'atleast2cit'; the latter is used below.
    df_ = pd.read_csv('tempdata/summary_stats_by_year_atleast2cit.csv')
    for metric in metrics:
        for group in groups:
            for c_loc in c_locs:
                fig = plot_bar_div_vs_year(df=df_, method=metric, group=group, c_loc=c_loc)
                if not os.path.exists('report_graphs/bar_div_vs_year'):
                    os.makedirs('report_graphs/bar_div_vs_year')
                fig.write_image('report_graphs/bar_div_vs_year/bar_div_vs_year_'
                                + metric + '_' + group + '_' + c_loc + '.png', scale=scale, width=width, height=height)
                af.add_existing_file('report_graphs/bar_div_vs_year/bar_div_vs_year_'
                                     + metric + '_' + group + '_' + c_loc + '.png')


def create_bar_doi_count_combined(af: AnalyticsFunction):
    # input variables:
    # data = 'all_papers' or 'atleast2cit', latter used here
    df = pd.read_csv('tempdata/summary_stats_by_year_atleast2cit.csv')
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
    fig.write_image('report_graphs/bar_doi_count/bar_doi_count_combined.png', scale=scale, width=width, height=height)
    af.add_existing_file('report_graphs/bar_doi_count/bar_doi_count_combined.png')


def create_bar_doi_count_by_oa(af: AnalyticsFunction):
    # input variables:
    # data = 'all_papers' or 'atleast2cit', latter used here
    df = pd.read_csv('tempdata/summary_stats_by_year_atleast2cit.csv')
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['noa_count'],
                         name='not OA', marker_color='indianred'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['oa_count'],
                         name='OA', marker_color='royalblue'))
    fig.update_layout(title='Figure: Annual OA versus non-OA DOI counts',
                      xaxis_title="year",
                      yaxis_title="doi_count")
    fig.update_layout(xaxis_type='category')
    if not os.path.exists('report_graphs/bar_doi_count'):
        os.makedirs('report_graphs/bar_doi_count')
    fig.write_image('report_graphs/bar_doi_count/bar_doi_count_by_oa.png', scale=scale, width=width, height=height)
    af.add_existing_file('report_graphs/bar_doi_count/bar_doi_count_by_oa.png')


def plot_bar_cit_count_by_oa(df, c_loc='mean'):
    # input variables:
    # c_loc = 'mean' or 'median'
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['noa_cc_' + str(c_loc)],
                         name='not OA', marker_color='indianred'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['oa_cc_' + str(c_loc)],
                         name='OA', marker_color='royalblue'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['gold_cc_' + str(c_loc)],
                         name='gold OA', marker_color='darkgoldenrod'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['green_cc_' + str(c_loc)],
                         name='green OA', marker_color='darkgreen'))
    fig.update_layout(title='Figure: The ' + str(c_loc) + ' citation count per OA type',
                      xaxis_title="year",
                      yaxis_title=str(c_loc) + " citation count")
    fig.update_layout(xaxis_type='category')
    return fig


def create_bar_cit_count_by_oa(af: AnalyticsFunction):
    # create plots for all years, groupings, and diversity metrics
    # data = 'all_papers' or 'atleast2cit'; the latter is used below.
    df_ = pd.read_csv('tempdata/summary_stats_by_year_atleast2cit.csv')
    for c_loc in c_locs:
        fig = plot_bar_cit_count_by_oa(df=df_, c_loc=c_loc)
        if not os.path.exists('report_graphs/bar_cit_count'):
            os.makedirs('report_graphs/bar_cit_count')
        fig.write_image('report_graphs/bar_cit_count/bar_cit_count_by_oa_'
                        + c_loc + '.png', scale=scale, width=width, height=height)
        af.add_existing_file('report_graphs/bar_cit_count/bar_cit_count_by_oa_'
                             + c_loc + '.png')


def plot_bar_uniq_cit_count(df, group='Countries', c_loc='mean'):
    # input variables:
    # group = Institutions, Countries, Subregions, or Regions or Fields;
    # c_loc = 'mean' or 'median'
    # this only applies to papers with at least 2 citations
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['noa_' + str(group) + '_uniq_' + str(c_loc)],
                         name='not OA', marker_color='indianred'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['oa_' + str(group) + '_uniq_' + str(c_loc)],
                         name='OA', marker_color='royalblue'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['gold_' + str(group) + '_uniq_' + str(c_loc)],
                         name='gold OA', marker_color='darkgoldenrod'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['green_' + str(group) + '_uniq_' + str(c_loc)],
                         name='green OA', marker_color='darkgreen'))
    fig.update_layout(title='Figure: The ' + str(c_loc) + ' number of unique citing ' + str(group),
                      xaxis_title="year",
                      yaxis_title=str(c_loc) + " unique citing " + str(group))
    fig.update_layout(xaxis_type='category')
    return fig


def create_bar_uniq_cit_count(af: AnalyticsFunction):
    # create plots for all years, groupings, and diversity metrics
    # data = 'all_papers' or 'atleast2cit'; the latter is used below.
    df_ = pd.read_csv('tempdata/summary_stats_by_year_atleast2cit.csv')
    for group in groups:
        for c_loc in c_locs:
            fig = plot_bar_uniq_cit_count(df=df_, group=group, c_loc=c_loc)
            if not os.path.exists('report_graphs/bar_uniq_cit_count'):
                os.makedirs('report_graphs/bar_uniq_cit_count')
            fig.write_image('report_graphs/bar_uniq_cit_count/bar_uniq_cit_count_'
                            + group + '_' + c_loc + '.png', scale=scale, width=width, height=height)
            af.add_existing_file('report_graphs/bar_uniq_cit_count/bar_uniq_cit_count_'
                                 + group + '_' + c_loc + '.png')
