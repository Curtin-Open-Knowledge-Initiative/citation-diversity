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

from observatory.reports import report_utils
from precipy.analytics_function import AnalyticsFunction
from report_data_processing.sql import (
    hello_world
)
# Insert applicable graphs once created
# from report_graphs import (
#     Alluvial, OverallCoverage, BarLine, ValueAddBar, ValueAddByCrossrefType, ValueAddByCrossrefTypeHorizontal,
#     PlotlyTable
# )

# Replace with applicable project name
PROJECT_ID = 'coki-curtin-research-qualities'

def get_data(af: AnalyticsFunction):
    hello_world_query = pd.read_gbq(query=hello_world,
                                 project_id=PROJECT_ID)

    hello_world_query.to_csv('hello_world.csv')
    af.add_existing_file('hello_world.csv')
    # issue with af not removing files in current working directory
    os.remove('hello_world.csv')
