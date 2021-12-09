import pandas as pd
import plotly.graph_objects as go
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


if __name__ == "__main__":
    # generate_boxplot_div_by_cit_group(method='Shannon', group='Subregions', year=2015)
    # generate_cit_div_vs_cit_count(method='Shannon', group='Subregions', year=2011)
    # generate_boxplot_div_by_oa_group(method='Shannon', group='Countries', year=2019)
    # generate_boxplot_uniq_cit_by_cit_group(group='Countries', year=2018)
    generate_boxplot_uniq_cit_by_oa_group(group='Subregions', year=2012)


