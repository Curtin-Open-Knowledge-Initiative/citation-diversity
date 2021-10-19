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
from report_data_processing.sql import *

# Insert applicable graphs once created
# from report_graphs import (
#     Alluvial, OverallCoverage, BarLine, ValueAddBar, ValueAddByCrossrefType, ValueAddByCrossrefTypeHorizontal,
#     PlotlyTable
# )

# Replace with applicable project name
PROJECT_ID = 'coki-scratch-space'
TEMPDIR = Path('tempdir')


def get_data(af: AnalyticsFunction):
    """
    Create main citation diversity table and save as new table in BigQuery
    """

    print("Generating the Citation Diversity Table")
    with bigquery.Client() as client:
        job_config = bigquery.QueryJobConfig(destination="coki-scratch-space.karl.citation_diversity",
                                             create_disposition="CREATE_IF_NEEDED",
                                             write_disposition="WRITE_TRUNCATE")

        # Start the query, passing in the extra configuration.
        query_job = client.query(global_citation_query, job_config=job_config)  # Make an API request.
        query_job.result()  # Wait for the job to complete.

    print("...completed")

def pull_data(af:AnalyticsFunction):
    """
    Pull data down for analysis
    """

    print("Pulling data from Bigquery")
    data = pd.read_gbq(query=global_citation_query)
    data.to_csv(TEMPDIR / 'file.csv')
    af.add_existing_file(TEMPDIR / 'file.csv')
    print('...completed')
