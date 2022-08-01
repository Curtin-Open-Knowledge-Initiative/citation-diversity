# COKI CURTIN RESEARCH QUALITITES REPORT
#
# Copyright 2021 ######
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

# Utility functions
# from pathlib import Path

# which groupings to run
groups = ['Institutions', 'Countries', 'Subregions', 'Regions', 'Fields']

# which citation diversity metric to run
metrics = ['GiniSim', 'Shannon']

# which data year to run, i.e., 2010 to 2019
years = list(range(2010, 2021))

# measures of central location
c_locs = ['mean', 'median']

# Table Locations
PROJECT_ID = 'coki-citation-diversity'
DOI_TABLE = 'academic-observatory.observatory.doi20220730'
MAG_REFERENCES_TABLE = 'academic-observatory.mag.PaperReferences20211206'
CITATION_DIVERSITY_TABLE = 'coki-scratch-space.karl.citation_diversity_global'

# plotly figure sizes
scale=1
width=1000
height=600