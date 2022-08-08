import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import json
import numpy as np

# year = 2019


def generate_boxplot_div_by_cit_group(method='GiniSim', group='Countries', year=2019):
    # input variables method is either GiniSim or Shannon, group is one of Institutions, Countries, Subregions,
    # or Regions or Fields
    df = pd.read_csv('tempdata/samples_by_cit_group_and_oa_' + str(year) + '.csv', dtype = {'cit_group': str})
    df['cit_group'] = pd.Categorical(df['cit_group'], ["2", "3", "4", "5-6", "7-9", "10-11", "12-14",
                                                        "15-16", "17-19", "20-23", "24-29", "30-42",
                                                        "43-59", ">=60"])
    df = df.sort_values('cit_group')
    # print(df[df['is_oa'] == True][['CitingCountries_Shannon']])
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['Citing'+str(group)+'_'+str(method)].loc[df.is_oa],
                         x=df['cit_group'].loc[df.is_oa], name='OA'))
    fig.add_trace(go.Box(y=df['Citing'+str(group)+'_'+str(method)].loc[~df.is_oa],
                         x=df['cit_group'].loc[~df.is_oa], name='not OA'))
    fig.update_layout(title='Figure: Box plots of '+str(method)+' index on citing '+str(group)
                            +' by citation groups for '+ str(year) +
                            '<br><sup>(A total of 56000 papers. '
                            'Each group consists of a sample 2000 OA papers and 2000 non-OA papers)</sup>',
                      xaxis_title="Groups by citation count",
                      yaxis_title=str(method)+" index",
                      boxmode='group')
    fig.show()


def generate_boxplot_div_by_oa_group(method='GiniSim', group='Countries', year=2019):
    # input variables method is either GiniSim or Shannon, group is one of Institutions, Countries, Subregions,
    # or Regions or Fields
    df = pd.read_csv('tempdata/samples_by_oa_' + str(year) + '.csv')
    df.fillna(value=False, inplace=True)
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_' + str(method)].loc[df.s_noa], name='not OA',
                         marker_color='indianred'))
    fig.add_trace(go.Box(y=df['Citing'+str(group)+ '_' + str(method)].loc[df.s_oa], name='OA',
                         marker_color='royalblue'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_' + str(method)].loc[df.s_gold], name='gold OA',
                         marker_color='darkgoldenrod'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_' + str(method)].loc[df.s_green], name='green OA',
                         marker_color='darkgreen'))
    fig.update_layout(title='Figure: Box plots of '+str(method)+' index on citing '+str(group)+' by OA status for '
                            + str(year) +
                            '<br><sup>(samples of 10000 non-OA, 10000 OA, '
                            '10000 gold and 10000 green papers.)</sup>',
                      xaxis_title="OA status",
                      yaxis_title=str(method)+" index")
    fig.show()


def generate_boxplot_uniq_cit_by_cit_group(group='Countries', year=2019):
    # input variable group is one of Institutions, Countries, Subregions,
    # or Regions or Fields
    df = pd.read_csv('tempdata/samples_by_cit_group_and_oa_' + str(year) + '.csv', dtype={'cit_group': str})
    df['cit_group'] = pd.Categorical(df['cit_group'], ["2", "3", "4", "5-6", "7-9", "10-11", "12-14",
                                                       "15-16", "17-19", "20-23", "24-29", "30-42",
                                                       "43-59", ">=60"])
    df = df.sort_values('cit_group')
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
                      yaxis_title="number of unique citing "+str(group),
                      boxmode='group')
    fig.show()

def generate_boxplot_uniq_cit_by_oa_group(group='Countries', year=2019):
    # input variable group is one of Institutions, Countries, Subregions,
    # or Regions or Fields
    df = pd.read_csv('tempdata/samples_by_oa_' + str(year) + '.csv')
    df.fillna(value=False, inplace=True)
    fig = go.Figure()
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_count_uniq'].loc[df.s_noa], name='not OA',
                         marker_color='indianred'))
    fig.add_trace(go.Box(y=df['Citing'+str(group)+ '_count_uniq'].loc[df.s_oa], name='OA',
                         marker_color='royalblue'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_count_uniq'].loc[df.s_gold], name='gold OA',
                         marker_color='darkgoldenrod'))
    fig.add_trace(go.Box(y=df['Citing' + str(group) + '_count_uniq'].loc[df.s_green], name='green OA',
                         marker_color='darkgreen'))
    fig.update_layout(title='Figure: Box plots of number of unique citing '+str(group)+' by OA status for '
                            + str(year) +
                            '<br><sup>(samples of 10000 non-OA, 10000 OA, '
                            '10000 gold and 10000 green papers.)</sup>',
                      xaxis_title="OA status",
                      yaxis_title="number of unique citing "+str(group))
    fig.show()


def generate_cit_div_vs_cit_count(method='GiniSim', group='Countries', year=2019):
    # input variables method is either GiniSim or Shannon, group is one of Institutions, Countries, Subregions,
    # or Regions or Fields
    df = pd.read_csv('tempdata/cit_div_vs_cit_count_' + str(year) + '.csv')
    df = df.sort_values('CitationCount')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['CitationCount'],
                             y=df['Citing'+str(group)+'_'+str(method)+'_perc0'],
                             name='min', line=dict(color='firebrick', dash='dot')))
    fig.add_trace(go.Scatter(x=df['CitationCount'],
                             y=df['Citing'+str(group)+'_'+str(method)+'_perc25'],
                             name='1stQ', line=dict(color='firebrick')))
    fig.add_trace(go.Scatter(x=df['CitationCount'],
                             y=df['Citing'+str(group)+'_'+str(method)+'_perc75'],
                             name='3rdQ', line=dict(color='royalblue')))
    fig.add_trace(go.Scatter(x=df['CitationCount'],
                             y=df['Citing'+str(group)+'_'+str(method)+'_perc100'],
                             name='max', line=dict(color='royalblue', dash='dot')))
    fig.add_trace(go.Scatter(x=df['CitationCount'],
                             y=df['Citing'+str(group)+'_'+str(method)+'_perc50'],
                             name='median', line=dict(color='black', width=3)))
    fig.update_layout(title='Figure: Citation count versus '+str(method)+' index of citing '+str(group)+' for '
                            +str(year),
                      xaxis_title="Citation count",
                      yaxis_title=str(method)+" index")
    fig.update_layout(xaxis_type='category')
    fig.show()


def generate_year_vs_cit_div(data='atleast2cit', method='GiniSim', group='Countries', c_loc='mean'):
    # input variables:
    # data = 'all_papers' or 'atleast2cit';
    # metric = 'GiniSim' or 'Shannon';
    # group = Institutions, Countries, Subregions, or Regions or Fields;
    # c_loc = 'mean' or 'median'
    df = pd.read_csv('tempdata/summary_stats_by_year_' + str(data) + '.csv')
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['noa_' + str(group) + '_' + str(method) + '_' + str(c_loc)],
                         name='not OA', marker_color='indianred'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['oa_'+str(group)+'_'+str(method)+'_'+str(c_loc)],
                         name='OA', marker_color='royalblue'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['gold_' + str(group) + '_' + str(method) + '_' + str(c_loc)],
                         name='gold OA', marker_color='darkgoldenrod'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['green_' + str(group) + '_' + str(method) + '_' + str(c_loc)],
                         name='green OA', marker_color='darkgreen'))
    fig.update_layout(title='Figure: The '+ str(c_loc) + ' ' + str(method)+' index of citing '+str(group)+' ',
                      xaxis_title="year",
                      yaxis_title=str(method)+" index")
    fig.update_layout(xaxis_type='category')
    fig.show()


def generate_year_vs_doi_count_combined(data='atleast2cit'):
    # input variables:
    # data = 'all_papers' or 'atleast2cit'
    df = pd.read_csv('tempdata/summary_stats_by_year_' + str(data) + '.csv')
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['doi_count'],
                         name='doi count', marker_color='grey'))
    fig.update_layout(title='Figure: Annual DOI counts',
                      xaxis_title="year",
                      yaxis_title="doi count")
    fig.update_layout(xaxis_type='category')
    fig.show()


def generate_year_vs_doi_count(data='atleast2cit'):
    # input variables:
    # data = 'all_papers' or 'atleast2cit'
    df = pd.read_csv('tempdata/summary_stats_by_year_' + str(data) + '.csv')
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
    fig.show()


def generate_year_vs_cit_count(data='atleast2cit', c_loc='mean'):
    # input variables:
    # data = 'all_papers' or 'atleast2cit';
    # c_loc = 'mean' or 'median'
    df = pd.read_csv('tempdata/summary_stats_by_year_' + str(data) + '.csv')
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['noa_cc_'+ str(c_loc)],
                         name='not OA', marker_color='indianred'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['oa_cc_'+str(c_loc)],
                         name='OA', marker_color='royalblue'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['gold_cc_'+ str(c_loc)],
                         name='gold OA', marker_color='darkgoldenrod'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['green_cc_'+ str(c_loc)],
                         name='green OA', marker_color='darkgreen'))
    fig.update_layout(title='Figure: The ' + str(c_loc) + ' citation count per OA type',
                      xaxis_title="year",
                      yaxis_title=str(c_loc)+" citation count")
    fig.update_layout(xaxis_type='category')
    fig.show()


def generate_year_vs_citing_entities(group='Countries', c_loc='mean'):
    # input variables:
    # group = Institutions, Countries, Subregions, or Regions or Fields;
    # c_loc = 'mean' or 'median'
    # this only applies to papers with at least 2 citations
    df = pd.read_csv('tempdata/summary_stats_by_year_atleast2cit.csv')
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['noa_' + str(group) + '_uniq_' + str(c_loc)],
                         name='not OA', marker_color='indianred'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['oa_'+str(group)+'_uniq_'+str(c_loc)],
                         name='OA', marker_color='royalblue'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['gold_' + str(group) + '_uniq_' + str(c_loc)],
                         name='gold OA', marker_color='darkgoldenrod'))
    fig.add_trace(go.Bar(x=df['year'],
                         y=df['green_' + str(group) + '_uniq_' + str(c_loc)],
                         name='green OA', marker_color='darkgreen'))
    fig.update_layout(title='Figure: The '+ str(c_loc) + ' number of unique citing '+str(group),
                      xaxis_title="year",
                      yaxis_title=str(c_loc)+" unique citing "+str(group))
    fig.update_layout(xaxis_type='category')
    fig.show()


def generate_region_vs_citations(region='Asia', year='2021'):
    data = []
    for line in open('tempdata/summary_stats_by_region_atleast2cit.json', 'r'):
        data.append(json.loads(line))
    df_oa = [x for x in data if ((x['region'] == region) & (x['year'] == year) & (x['is_oa'] == 'true'))]
    df_noa = [x for x in data if ((x['region'] == region) & (x['year'] == year) & (x['is_oa'] == 'false'))]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[x['name'] for x in df_oa[0]['CitingRegions_table_all']],
                         y=[int(x['total']) for x in df_oa[0]['CitingRegions_table_all']],
                         name='OA', marker_color='royalblue'))
    fig.add_trace(go.Bar(x=[x['name'] for x in df_noa[0]['CitingRegions_table_all']],
                         y=[int(x['total']) for x in df_noa[0]['CitingRegions_table_all']],
                         name='not OA', marker_color='indianred'))
    fig.update_layout(title='Figure: Number of institutional citations to papers affiliated to ' + str(region) + ' for ' + str(year),
                      xaxis_title="region",
                      yaxis_title="citation count")
    fig.update_layout(xaxis_type='category')
    fig.update_xaxes(categoryorder='category ascending')
    fig.show()


def generate_subregion_vs_citations(subregion='Latin America and the Caribbean', year='2019'):
    data = []
    for line in open('tempdata/summary_stats_by_subregion_atleast2cit.json', 'r'):
        data.append(json.loads(line))
    df_oa = [x for x in data if ((x['subregion'] == subregion) & (x['year'] == year) & (x['is_oa'] == 'true'))]
    df_noa = [x for x in data if ((x['subregion'] == subregion) & (x['year'] == year) & (x['is_oa'] == 'false'))]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[x['name'] for x in df_oa[0]['CitingSubregions_table_all']],
                         y=[int(x['total']) for x in df_oa[0]['CitingSubregions_table_all']],
                         name='OA', marker_color='royalblue'))
    fig.add_trace(go.Bar(x=[x['name'] for x in df_noa[0]['CitingSubregions_table_all']],
                         y=[int(x['total']) for x in df_noa[0]['CitingSubregions_table_all']],
                         name='not OA', marker_color='indianred'))
    fig.update_layout(title='Figure: Number of institutional citations to papers affiliated to ' + str(subregion) + ' for ' + str(year),
                      xaxis_title="subregion",
                      yaxis_title="citation count")
    fig.update_layout(xaxis_type='category')
    fig.update_xaxes(categoryorder='category ascending')
    fig.show()

def generate_region_vs_citations_perc_change(region='Asia', year='2019'):
    data = []
    for line in open('tempdata/summary_stats_by_region_atleast2cit.json', 'r'):
        data.append(json.loads(line))
    df_oa = [x for x in data if ((x['region'] == region) & (x['year'] == year) & (x['is_oa'] == 'true'))]
    df_noa = [x for x in data if ((x['region'] == region) & (x['year'] == year) & (x['is_oa'] == 'false'))]
    df_oa = pd.json_normalize(df_oa[0]['CitingRegions_table_all'])
    df_noa = pd.json_normalize(df_noa[0]['CitingRegions_table_all'])
    df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
    df = df.astype({"total_oa": int, "total_noa": int})
    df['perc_change'] = (df['total_oa'] - df['total_noa'])/df['total_noa']*100
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['name'],
                         y=df['perc_change'],
                         marker_color='royalblue'))
    fig.update_layout(
        title='Figure: Percentage change in citations to OA/non-OA paper affiliated to '
              + str(region) + ' for ' + str(year),
        xaxis_title="region",
        yaxis_title="percent change")
    fig.update_layout(xaxis_type='category')
    fig.update_xaxes(categoryorder='category ascending')
    fig.show()

def generate_subregion_vs_citations_perc_change(subregion='Latin America and the Caribbean', year='2019'):
    data = []
    for line in open('tempdata/summary_stats_by_subregion_atleast2cit.json', 'r'):
        data.append(json.loads(line))
    df_oa = [x for x in data if ((x['subregion'] == subregion) & (x['year'] == year) & (x['is_oa'] == 'true'))]
    df_noa = [x for x in data if ((x['subregion'] == subregion) & (x['year'] == year) & (x['is_oa'] == 'false'))]
    df_oa = pd.json_normalize(df_oa[0]['CitingSubregions_table_all'])
    df_noa = pd.json_normalize(df_noa[0]['CitingSubregions_table_all'])
    df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
    df = df.astype({"total_oa": int, "total_noa": int})
    df['perc_change'] = (df['total_oa'] - df['total_noa'])/df['total_noa']*100
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['name'],
                         y=df['perc_change'],
                         marker_color='royalblue'))
    fig.update_layout(
        title='Figure: Percentage change in citations to OA/non-OA paper affiliated to '
              + str(subregion) + ' for ' + str(year),
        xaxis_title="subregion",
        yaxis_title="percent change")
    fig.update_layout(xaxis_type='category')
    fig.update_xaxes(categoryorder='category ascending')
    fig.show()


def generate_region_vs_citations_perc_change_over_time(region='Europe', year_start='2010', year_end='2019'):
    data = []
    color_map_regions={
        "Asia": 'orange',
        "Europe": 'limegreen',
        "Americas": 'brown',
        "Oceania": 'red',
        "Africa": 'magenta'
    }
    order_regions=["Asia", "Europe", "Americas ", "Oceania", "Africa"]
    for line in open('tempdata/summary_stats_by_region_atleast2cit.json', 'r'):
        data.append(json.loads(line))
    fig = go.Figure()
    data_figure = pd.DataFrame(columns=['name', 'total_oa', 'total_noa', 'perc_change', 'year'])
    for year in range(int(year_start), int(year_end)+1):
        df_oa = [x for x in data if ((x['region'] == region) & (x['year'] == str(year)) & (x['is_oa'] == 'true'))]
        df_noa = [x for x in data if ((x['region'] == region) & (x['year'] == str(year)) & (x['is_oa'] == 'false'))]
        df_oa = pd.json_normalize(df_oa[0]['CitingRegions_table_all'])
        df_noa = pd.json_normalize(df_noa[0]['CitingRegions_table_all'])
        df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
        df = df.astype({"total_oa": int, "total_noa": int})
        df['perc_change'] = (df['total_oa'] - df['total_noa'])/df['total_noa']*100
        df['year'] = str(year)
        df = pd.DataFrame(df)
        data_figure = pd.concat([data_figure, df])
    fig = px.line(data_figure, x='year', y='perc_change', color='name',
                  color_discrete_map=color_map_regions,
                  category_orders={"name": order_regions})
    fig.update_layout(legend={"itemsizing": "trace", "itemwidth": 45})
    fig.update_layout(
        title='Figure: Percentage difference in citations to OA over non-OA papers affiliated to '
              + str(region) + ' from ' + str(year_start) + ' to ' + str(year_end)
              + '<br><sup>(Percentage differences are relative to non-OA papers)</sup>',
        xaxis_title="Year",
        yaxis_title="Percent difference",
        legend_title_text='Regions')
    fig.show()


def generate_subregion_vs_citations_perc_change_over_time(subregion='Latin America and the Caribbean', year_start='2010', year_end='2019'):
    data = []
    color_map_subregions={
        "Eastern Asia": 'orange',
        "Southern Asia": 'orange',
        "Western Asia": 'orange',
        "South-eastern Asia": 'orange',
        "Central Asia": 'orange',
        "Southern Europe": 'limegreen',
        "Eastern Europe": 'limegreen',
        "Western Europe": 'limegreen',
        "Northern Europe": 'limegreen',
        "Latin America and the Caribbean": 'brown',
        "Northern America": 'dodgerblue',
        "Australia and New Zealand": 'red',
        "Melanesia": 'red',
        "Polynesia": 'red',
        "Micronesia": 'red',
        "Northern Africa": 'magenta',
        "Sub-Saharan Africa": 'magenta'
    }
    dash_map_subregions = {
        "Eastern Asia": 'solid',
        "Southern Asia": 'longdash',
        "Western Asia": 'dash',
        "South-eastern Asia": 'dashdot',
        "Central Asia": 'dot',
        "Southern Europe": 'solid',
        "Eastern Europe": 'dash',
        "Western Europe": 'dashdot',
        "Northern Europe": 'dot',
        "Latin America and the Caribbean": 'solid',
        "Northern America": 'solid',
        "Australia and New Zealand": 'solid',
        "Melanesia": 'dash',
        "Polynesia": 'dashdot',
        "Micronesia": 'dot',
        "Northern Africa": 'solid',
        "Sub-Saharan Africa": 'dash'
    }
    order_subregions=["Eastern Asia", "Southern Asia", "Western Asia", "South-eastern Asia", "Central Asia",
                      "Southern Europe", "Eastern Europe", "Western Europe", "Northern Europe",
                      "Latin America and the Caribbean", "Northern America", "Australia and New Zealand", "Melanesia",
                      "Polynesia", "Micronesia", "Northern Africa", "Sub-Saharan Africa"]
    for line in open('tempdata/summary_stats_by_subregion_atleast2cit.json', 'r'):
        data.append(json.loads(line))
    fig = go.Figure()
    data_figure = pd.DataFrame(columns=['name', 'total_oa', 'total_noa', 'perc_change', 'year'])
    for year in range(int(year_start), int(year_end)+1):
        df_oa = [x for x in data if ((x['subregion'] == subregion) & (x['year'] == str(year)) & (x['is_oa'] == 'true'))]
        df_noa = [x for x in data if ((x['subregion'] == subregion) & (x['year'] == str(year)) & (x['is_oa'] == 'false'))]
        if (len(df_oa) > 0) & (len(df_noa) > 0):
            df_oa = pd.json_normalize(df_oa[0]['CitingSubregions_table_all'])
            df_noa = pd.json_normalize(df_noa[0]['CitingSubregions_table_all'])
            df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
            df = df.astype({"total_oa": int, "total_noa": int})
            df['perc_change'] = (df['total_oa'] - df['total_noa'])/df['total_noa']*100
            df['year'] = str(year)
            df = pd.DataFrame(df)
            data_figure = pd.concat([data_figure, df])
    fig = px.line(data_figure, x='year', y='perc_change', color='name', line_dash='name',
                  color_discrete_map=color_map_subregions,
                  line_dash_map=dash_map_subregions,
                  category_orders={"name": order_subregions})
    fig.update_layout(legend={"itemsizing": "trace", "itemwidth": 45})
    fig.update_layout(
        title='Figure: Percentage difference in citations to OA over non-OA papers affiliated to '
              + str(subregion) + ' from ' + str(year_start) + ' to ' + str(year_end)
              + '<br><sup>(Percentage differences are relative to non-OA papers)</sup>',
        xaxis_title="Year",
        yaxis_title="Percentage difference",
        legend_title_text='Subregions')
    fig.show()


def generate_line_year_vs_cit_div():
    # input variables:
    # data = 'all_papers' or 'atleast2cit';
    # metric = 'GiniSim' or 'Shannon';
    # group = Institutions, Countries, Subregions, or Regions or Fields;
    # c_loc = 'mean' or 'median'
    df = pd.read_csv('tempdata/summary_stats_by_year_atleast2cit.csv')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['year'], y=df['noa_Institutions_GiniSim_median'],
                         name='CLOSED', marker_color='gray'))
    fig.add_trace(go.Scatter(x=df['year'], y=df['oa_Institutions_GiniSim_median'],
                         name='OPEN', marker_color='#E7664C'))
    fig.update_layout(xaxis_title="year",
                      yaxis_title="Gini-Simpson score")
    fig.update_layout(xaxis_type='category')
    fig.show()


def create_figure2c():
    # create plots for all years, groupings, and diversity metrics
    print('... start figure2c')
    df = pd.read_csv('tempdata/samples_by_oa_2019.csv')
    df.fillna(value=False, inplace=True)
    # df = df[df['CitationCount'] >= 10]
    method = "Shannon"
    groups = ['Institutions', 'Countries', 'Subregions', 'Regions', 'Fields']
    group_labels = ["CLOSED", "OPEN"]
    fig = make_subplots(rows=5, cols=2, column_widths=[0.9, 0.1],
                        subplot_titles=[val for val in groups for _ in (0, 1)],
                        vertical_spacing=0.06,
                        horizontal_spacing=0.1,
                        y_title="Probability density / Frequency", x_title=method + " index score")

    x1 = df['Citing' + str(groups[0]) + '_' + str(method)].loc[df['Citing' + str(groups[0]) + '_' + str(method)]>0].loc[df.s_noa]
    x1 = x1.astype(float)
    x2 = df['Citing' + str(groups[0]) + '_' + str(method)].loc[df['Citing' + str(groups[0]) + '_' + str(method)]>0].loc[df.s_oa]
    x2 = x2.astype(float)
    hist_data = [x1, x2]
    fig_sub = ff.create_distplot(hist_data, group_labels, show_hist=True, bin_size=[0.13, 0.13], show_rug=False)
    fig.add_trace(go.Histogram(fig_sub['data'][0], marker_color='gray', opacity=.3, showlegend=False),
                  row=1, col=1)
    fig.add_trace(go.Histogram(fig_sub['data'][1], marker_color='#E7664C', opacity=.3, showlegend=False),
                  row=1, col=1)
    fig.add_trace(go.Scatter(fig_sub['data'][2], line=dict(color='gray', width=2), showlegend=False),
                  row=1, col=1)
    fig.add_trace(go.Scatter(fig_sub['data'][3], line=dict(color='#E7664C', width=2), showlegend=False),
                  row=1, col=1)

    x1 = df['Citing' + str(groups[0]) + '_' + str(method)].loc[df['Citing' + str(groups[0]) + '_' + str(method)] == 0].loc[
        df.s_noa]
    x1 = x1.astype(float)
    x2 = df['Citing' + str(groups[0]) + '_' + str(method)].loc[df['Citing' + str(groups[0]) + '_' + str(method)] == 0].loc[
        df.s_oa]
    x2 = x2.astype(float)
    fig.add_trace(go.Histogram(x=x1, marker_color='gray', opacity=.3, showlegend=False),
                  row=1, col=2)
    fig.add_trace(go.Histogram(x=x2, marker_color='#E7664C', opacity=.3, showlegend=False),
                  row=1, col=2)

    x1 = df['Citing' + str(groups[1]) + '_' + str(method)].loc[df['Citing' + str(groups[1]) + '_' + str(method)]>0].loc[df.s_noa]
    x1 = x1.astype(float)
    x2 = df['Citing' + str(groups[1]) + '_' + str(method)].loc[df['Citing' + str(groups[1]) + '_' + str(method)]>0].loc[df.s_oa]
    x2 = x2.astype(float)
    hist_data = [x1, x2]
    fig_sub = ff.create_distplot(hist_data, group_labels, show_hist=True, bin_size=[0.08, 0.08], show_rug=False)
    fig.add_trace(go.Histogram(fig_sub['data'][0], marker_color='gray', opacity=.3, showlegend=False),
                  row=2, col=1)
    fig.add_trace(go.Histogram(fig_sub['data'][1], marker_color='#E7664C', opacity=.3, showlegend=False),
                  row=2, col=1)
    fig.add_trace(go.Scatter(fig_sub['data'][2], line=dict(color='gray', width=2), showlegend=False),
                  row=2, col=1)
    fig.add_trace(go.Scatter(fig_sub['data'][3], line=dict(color='#E7664C', width=2), showlegend=False),
                  row=2, col=1)

    x1 = df['Citing' + str(groups[1]) + '_' + str(method)].loc[df['Citing' + str(groups[1])
                                                                  + '_' + str(method)] == 0].loc[df.s_noa]
    x1 = x1.astype(float)
    x2 = df['Citing' + str(groups[1]) + '_' + str(method)].loc[df['Citing' + str(groups[1])
                                                                  + '_' + str(method)] == 0].loc[df.s_oa]
    x2 = x2.astype(float)
    fig.add_trace(go.Histogram(x=x1, marker_color='gray', opacity=.3, showlegend=False),
                  row=2, col=2)
    fig.add_trace(go.Histogram(x=x2, marker_color='#E7664C', opacity=.3, showlegend=False),
                  row=2, col=2)

    x1 = df['Citing' + str(groups[2]) + '_' + str(method)].loc[df['Citing' + str(groups[2]) + '_' + str(method)]>0].loc[df.s_noa]
    x1 = x1.astype(float)
    x2 = df['Citing' + str(groups[2]) + '_' + str(method)].loc[df['Citing' + str(groups[2]) + '_' + str(method)]>0].loc[df.s_oa]
    x2 = x2.astype(float)
    hist_data = [x1, x2]
    fig_sub = ff.create_distplot(hist_data, group_labels, show_hist=True, bin_size=[0.05, 0.05], show_rug=False)
    fig.add_trace(go.Histogram(fig_sub['data'][0], marker_color='gray', opacity=.3, showlegend=False),
                  row=3, col=1)
    fig.add_trace(go.Histogram(fig_sub['data'][1], marker_color='#E7664C', opacity=.3, showlegend=False),
                  row=3, col=1)
    fig.add_trace(go.Scatter(fig_sub['data'][2], line=dict(color='gray', width=2), showlegend=False),
                  row=3, col=1)
    fig.add_trace(go.Scatter(fig_sub['data'][3], line=dict(color='#E7664C', width=2), showlegend=False),
                  row=3, col=1)

    x1 = df['Citing' + str(groups[2]) + '_' + str(method)].loc[df['Citing' + str(groups[2])
                                                                  + '_' + str(method)] == 0].loc[df.s_noa]
    x1 = x1.astype(float)
    x2 = df['Citing' + str(groups[2]) + '_' + str(method)].loc[df['Citing' + str(groups[2])
                                                                  + '_' + str(method)] == 0].loc[df.s_oa]
    x2 = x2.astype(float)
    fig.add_trace(go.Histogram(x=x1, marker_color='gray', opacity=.3, showlegend=False),
                  row=3, col=2)
    fig.add_trace(go.Histogram(x=x2, marker_color='#E7664C', opacity=.3, showlegend=False),
                  row=3, col=2)

    x1 = df['Citing' + str(groups[3]) + '_' + str(method)].loc[df['Citing' + str(groups[3]) + '_' + str(method)]>0].loc[df.s_noa]
    x1 = x1.astype(float)
    x2 = df['Citing' + str(groups[3]) + '_' + str(method)].loc[df['Citing' + str(groups[3]) + '_' + str(method)]>0].loc[df.s_oa]
    x2 = x2.astype(float)
    hist_data = [x1, x2]
    fig_sub = ff.create_distplot(hist_data, group_labels, show_hist=True, bin_size=[0.04, 0.04], show_rug=False)
    fig.add_trace(go.Histogram(fig_sub['data'][0], marker_color='gray', opacity=.3, showlegend=False),
                  row=4, col=1)
    fig.add_trace(go.Histogram(fig_sub['data'][1], marker_color='#E7664C', opacity=.3, showlegend=False),
                  row=4, col=1)
    fig.add_trace(go.Scatter(fig_sub['data'][2], line=dict(color='gray', width=2), showlegend=False),
                  row=4, col=1)
    fig.add_trace(go.Scatter(fig_sub['data'][3], line=dict(color='#E7664C', width=2), showlegend=False),
                  row=4, col=1)

    x1 = df['Citing' + str(groups[3]) + '_' + str(method)].loc[df['Citing' + str(groups[3])
                                                                  + '_' + str(method)] == 0].loc[df.s_noa]
    x1 = x1.astype(float)
    x2 = df['Citing' + str(groups[3]) + '_' + str(method)].loc[df['Citing' + str(groups[3])
                                                                  + '_' + str(method)] == 0].loc[df.s_oa]
    x2 = x2.astype(float)
    fig.add_trace(go.Histogram(x=x1, marker_color='gray', opacity=.3, showlegend=False),
                  row=4, col=2)
    fig.add_trace(go.Histogram(x=x2, marker_color='#E7664C', opacity=.3, showlegend=False),
                  row=4, col=2)

    x1 = df['Citing' + str(groups[4]) + '_' + str(method)].loc[df['Citing' + str(groups[4]) + '_' + str(method)]>0].loc[df.s_noa]
    x1 = x1.astype(float)
    x2 = df['Citing' + str(groups[4]) + '_' + str(method)].loc[df['Citing' + str(groups[4]) + '_' + str(method)]>0].loc[df.s_oa]
    x2 = x2.astype(float)
    hist_data = [x1, x2]
    fig_sub = ff.create_distplot(hist_data, group_labels, show_hist=True, bin_size=[0.05, 0.05], show_rug=False)
    fig.add_trace(go.Histogram(fig_sub['data'][0], marker_color='gray', opacity=.3, showlegend=False),
                  row=5, col=1)
    fig.add_trace(go.Histogram(fig_sub['data'][1], marker_color='#E7664C', opacity=.3, showlegend=False),
                  row=5, col=1)
    fig.add_trace(go.Scatter(fig_sub['data'][2], line=dict(color='gray', width=2), showlegend=True), row=5, col=1)
    fig.add_trace(go.Scatter(fig_sub['data'][3], line=dict(color='#E7664C', width=2), showlegend=True), row=5, col=1)

    x1 = df['Citing' + str(groups[4]) + '_' + str(method)].loc[df['Citing' + str(groups[4])
                                                                  + '_' + str(method)] == 0].loc[df.s_noa]
    x1 = x1.astype(float)
    x2 = df['Citing' + str(groups[4]) + '_' + str(method)].loc[df['Citing' + str(groups[4])
                                                                  + '_' + str(method)] == 0].loc[df.s_oa]
    x2 = x2.astype(float)
    fig.add_trace(go.Histogram(x=x1, marker_color='gray', opacity=.3, showlegend=False),
                  row=5, col=2)
    fig.add_trace(go.Histogram(x=x2, marker_color='#E7664C', opacity=.3, showlegend=False),
                  row=5, col=2)

    # fig.update_yaxes(type="log")
    # fig.update_layout(barmode='overlay')
    fig.update_layout(title='Fig. 2C: KDE on ' + method + ' scores' +
                            '<br><sup>(samples of 10000 non-OA and 10000 OA papers in each case)</sup>')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.show()
    print('... completed')


def create_figure2c_test():
    print('... start figure2c_test')
    df = pd.read_csv('tempdata/samples_by_oa_2019.csv')
    df.fillna(value=False, inplace=True)
    df = df[df['CitationCount'] >= 20]
    method = "Shannon"
    groups = ['Institutions', 'Countries', 'Subregions', 'Regions', 'Fields']
    group_labels = ["CLOSED", "OPEN"]
    fig = make_subplots(rows=5, cols=1, subplot_titles=groups,
                        y_title="Probability density", x_title=method + " index score")

    x1 = df['Citing' + str(groups[2]) + '_' + str(method)].loc[df.s_noa]
    x1 = x1.astype(float)
    x2 = df['Citing' + str(groups[2]) + '_' + str(method)].loc[df.s_oa]
    x2 = x2.astype(float)
    hist_data = [x1, x2]
    fig_sub = ff.create_distplot(hist_data, group_labels, colors=['gray', '#E7664C'], bin_size=[0.05, 0.05], show_rug=False)
    fig_sub.show()
    print('... completed')


def create_figure3a_test():
    # create plots for selected subregions
    # specify which subregions to show
    subregions_compare = ['Northern Europe', 'Sub-Saharan Africa', 'Eastern Asia']
    data = []
    for line in open('tempdata/summary_stats_by_subregion_atleast2cit.json', 'r'):
        data.append(json.loads(line))
    print('... start figure3a')
    # create fig space with 3 subplots
    fig = make_subplots(rows=3, cols=1, subplot_titles=subregions_compare,
                        vertical_spacing=0.1, y_title="% change in total citations", x_title="Citing subregions")
    # bar plot for subregion 1
    df_oa = [x for x in data if ((x['subregion'] == subregions_compare[0]) & (x['year'] == '2019') & (x['is_oa'] == 'true'))]
    df_noa = [x for x in data if ((x['subregion'] == subregions_compare[0]) & (x['year'] == '2019') & (x['is_oa'] == 'false'))]
    if (len(df_oa) > 0) & (len(df_noa) > 0):
        df_oa = pd.json_normalize(df_oa[0]['CitingSubregions_table_all'])
        df_noa = pd.json_normalize(df_noa[0]['CitingSubregions_table_all'])
        df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
        df = df.astype({"total_oa": int, "total_noa": int})
        df['perc_change'] = (df['total_oa'] - df['total_noa']) / df['total_noa'] * 100
        df = df[df.name.isin(subregions_compare)]
        fig.add_trace(go.Bar(x=df['name'], y=df['perc_change'], marker_color='royalblue', showlegend=False), row=1, col=1)
    # bar plot for subregion 2
    df_oa = [x for x in data if ((x['subregion'] == subregions_compare[1]) & (x['year'] == '2019') & (x['is_oa'] == 'true'))]
    df_noa = [x for x in data if ((x['subregion'] == subregions_compare[1]) & (x['year'] == '2019') & (x['is_oa'] == 'false'))]
    if (len(df_oa) > 0) & (len(df_noa) > 0):
        df_oa = pd.json_normalize(df_oa[0]['CitingSubregions_table_all'])
        df_noa = pd.json_normalize(df_noa[0]['CitingSubregions_table_all'])
        df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
        df = df.astype({"total_oa": int, "total_noa": int})
        df['perc_change'] = (df['total_oa'] - df['total_noa']) / df['total_noa'] * 100
        df = df[df.name.isin(subregions_compare)]
        fig.add_trace(go.Bar(x=df['name'], y=df['perc_change'], marker_color='royalblue', showlegend=False), row=2, col=1)
    # bar plot for subregion 3
    df_oa = [x for x in data if ((x['subregion'] == subregions_compare[2]) & (x['year'] == '2019') & (x['is_oa'] == 'true'))]
    df_noa = [x for x in data if ((x['subregion'] == subregions_compare[2]) & (x['year'] == '2019') & (x['is_oa'] == 'false'))]
    if (len(df_oa) > 0) & (len(df_noa) > 0):
        df_oa = pd.json_normalize(df_oa[0]['CitingSubregions_table_all'])
        df_noa = pd.json_normalize(df_noa[0]['CitingSubregions_table_all'])
        df = df_oa.merge(df_noa, on=['name'], suffixes=('_oa', '_noa'))
        df = df.astype({"total_oa": int, "total_noa": int})
        df['perc_change'] = (df['total_oa'] - df['total_noa']) / df['total_noa'] * 100
        df = df[df.name.isin(subregions_compare)]
        fig.add_trace(go.Bar(x=df['name'], y=df['perc_change'], marker_color='royalblue', showlegend=False), row=3, col=1)
    fig.update_layout(xaxis_type='category')
    fig.update_xaxes(categoryorder='category ascending')
    fig.update_layout(title='Fig. 3A: % change in total citations from selected subregions')
    fig.show()
    print('... completed')


def create_figure3b_test():
    # create plots for selected subregions
    # specify subregions to show
    years = list(range(2010, 2020))

    # color mapping when comparing subregions
    color_map_subregions = {
        "Eastern Asia": 'orange',
        "Southern Asia": 'orange',
        "Western Asia": 'orange',
        "South-eastern Asia": 'orange',
        "Central Asia": 'orange',
        "Southern Europe": 'limegreen',
        "Eastern Europe": 'limegreen',
        "Western Europe": 'limegreen',
        "Northern Europe": 'limegreen',
        "Latin America and the Caribbean": 'brown',
        "Northern America": 'dodgerblue',
        "Australia and New Zealand": 'red',
        "Melanesia": 'red',
        "Polynesia": 'red',
        "Micronesia": 'red',
        "Northern Africa": 'magenta',
        "Sub-Saharan Africa": 'magenta'
    }

    # line type mapping when comparing subregions
    dash_map_subregions = {
        "Eastern Asia": 'solid',
        "Southern Asia": 'longdash',
        "Western Asia": 'dash',
        "South-eastern Asia": 'dashdot',
        "Central Asia": 'dot',
        "Southern Europe": 'solid',
        "Eastern Europe": 'dash',
        "Western Europe": 'dashdot',
        "Northern Europe": 'dot',
        "Latin America and the Caribbean": 'solid',
        "Northern America": 'solid',
        "Australia and New Zealand": 'solid',
        "Melanesia": 'dash',
        "Polynesia": 'dashdot',
        "Micronesia": 'dot',
        "Northern Africa": 'solid',
        "Sub-Saharan Africa": 'dash'
    }

    # display order when comparing subregions
    order_subregions = [
        "Eastern Asia", "Southern Asia", "Western Asia", "South-eastern Asia", "Central Asia",
        "Southern Europe", "Eastern Europe", "Western Europe", "Northern Europe",
        "Latin America and the Caribbean", "Northern America", "Australia and New Zealand", "Melanesia",
        "Polynesia", "Micronesia", "Northern Africa", "Sub-Saharan Africa"
    ]
    subregions_compare = ['Northern Europe', 'Sub-Saharan Africa', 'Eastern Asia']
    data = []
    for line in open('tempdata/summary_stats_by_subregion_atleast2cit.json', 'r'):
        data.append(json.loads(line))
    print('... start figure3b')

    fig = make_subplots(rows=3, cols=1, subplot_titles=subregions_compare,
                        vertical_spacing=0.1, y_title="% ratios in average citations")

    data_figure = pd.DataFrame(columns=['name', 'total_oa', 'total_noa', 'perc_change', 'year'])
    for year in years:
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
                             name=subregions_compare[0], marker_color=color_map_subregions[subregions_compare[0]]),
                  row=1, col=1)
    data_figure1 = data_figure[data_figure.name == subregions_compare[1]]
    fig.add_trace(go.Scatter(x=data_figure1['year'], y=data_figure1['perc_change'],
                             name=subregions_compare[1], marker_color=color_map_subregions[subregions_compare[1]]),
                  row=1, col=1)
    data_figure1 = data_figure[data_figure.name == subregions_compare[2]]
    fig.add_trace(go.Scatter(x=data_figure1['year'], y=data_figure1['perc_change'],
                             name=subregions_compare[2], marker_color=color_map_subregions[subregions_compare[2]]),
                  row=1, col=1)

    data_figure = pd.DataFrame(columns=['name', 'total_oa', 'total_noa', 'perc_change', 'year'])
    for year in years:
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
                             name=subregions_compare[0], marker_color=color_map_subregions[subregions_compare[0]],
                             showlegend=False),
                  row=2, col=1)
    data_figure1 = data_figure[data_figure.name == subregions_compare[1]]
    fig.add_trace(go.Scatter(x=data_figure1['year'], y=data_figure1['perc_change'],
                             name=subregions_compare[1], marker_color=color_map_subregions[subregions_compare[1]],
                             showlegend=False),
                  row=2, col=1)
    data_figure1 = data_figure[data_figure.name == subregions_compare[2]]
    fig.add_trace(go.Scatter(x=data_figure1['year'], y=data_figure1['perc_change'],
                             name=subregions_compare[2], marker_color=color_map_subregions[subregions_compare[2]],
                             showlegend=False),
                  row=2, col=1)

    data_figure = pd.DataFrame(columns=['name', 'total_oa', 'total_noa', 'perc_change', 'year'])
    for year in years:
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
                             name=subregions_compare[0], marker_color=color_map_subregions[subregions_compare[0]],
                             showlegend=False),
                  row=3, col=1)
    data_figure1 = data_figure[data_figure.name == subregions_compare[1]]
    fig.add_trace(go.Scatter(x=data_figure1['year'], y=data_figure1['perc_change'],
                             name=subregions_compare[1], marker_color=color_map_subregions[subregions_compare[1]],
                             showlegend=False),
                  row=3, col=1)
    data_figure1 = data_figure[data_figure.name == subregions_compare[2]]
    fig.add_trace(go.Scatter(x=data_figure1['year'], y=data_figure1['perc_change'],
                             name=subregions_compare[2], marker_color=color_map_subregions[subregions_compare[2]],
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
        title='Figure: % ratios in average citations for all years ')
    fig.show()
    print('... completed')


if __name__ == "__main__":
    # generate_boxplot_div_by_cit_group(method='Shannon', group='Subregions', year=2015)
    # generate_boxplot_div_by_oa_group(method='Shannon', group='Countries', year=2019)
    # generate_boxplot_uniq_cit_by_cit_group(group='Countries', year=2018)
    # generate_boxplot_uniq_cit_by_oa_group(group='Subregions', year=2012)
    # generate_cit_div_vs_cit_count(method='Shannon', group='Fields', year=2011)
    # generate_year_vs_cit_div(data='atleast2cit', method='GiniSim', group='Fields', c_loc='median')
    # generate_year_vs_doi_count_combined(data='all_papers')
    # generate_year_vs_doi_count(data='all_papers')
    # generate_year_vs_cit_count(data='all_papers', c_loc='mean')
    # generate_year_vs_citing_entities(group='Regions', c_loc='mean')

    # generate_region_vs_citations(region='Asia', year='2021')
    # generate_subregion_vs_citations(subregion='Latin America and the Caribbean', year='2019')
    # generate_region_vs_citations_perc_change(region='Europe', year='2019')
    # generate_subregion_vs_citations_perc_change(subregion='Western Europe', year='2019')

    # generate_region_vs_citations_perc_change_over_time(region='Americas', year_start='2010', year_end='2019')
    # generate_subregion_vs_citations_perc_change_over_time(subregion='Micronesia', year_start='2010', year_end='2019')

    # generate_line_year_vs_cit_div()
    create_figure2c()

