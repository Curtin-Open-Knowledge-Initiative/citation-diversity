# MAG Metadata Coverage Report
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
# Authors: Cameron Neylon, Bianca Kramer

# SQL Queries used for interacting with the BigQuery Datasets

# Document Types and Counts

from pathlib import Path
from typing import Union, Optional

from google.cloud import bigquery

from observatory.reports import report_utils

SQL_TEMPLATES_DIRECTORY = Path("report_data_processing/sql_templates")
SQL_PROCESSED_DIRECTORY = Path("report_data_processing/sql_processed")

def load_sql_to_string(filepath: Union[str, Path],
                       parameters: Optional[dict] = None,
                       directory: Optional[Union[str, Path]] = None):
    filepath = Path(filepath)
    if directory:
        filepath = Path(directory) / filepath

    assert ((filepath.suffix == '.sql') or (filepath.suffix == '.jinja2'))

    with open(filepath, 'r') as f:
        sql_string = f.read()

    if parameters:
        sql_string = sql_string.format(**parameters)

    return sql_string

def run_query_to_bq_table(query: str,
                          query_name,
                          destination_table,
                          rerun,
                          verbose):

    if not report_utils.bigquery_rerun(query_name, rerun, verbose):
        print(f"""Query is:            
            {query}

            """)
        print(f'Destination Table: {destination_table}')
        return

    with bigquery.Client() as client:
        job_config = bigquery.QueryJobConfig(destination=destination_table,
                                             create_disposition="CREATE_IF_NEEDED",
                                             write_disposition="WRITE_TRUNCATE")

        # Start the query, passing in the extra configuration.
        query_job = client.query(query, job_config=job_config)  # Make an API request.
        query_job.result()  # Wait for the job to complete.

    print("...completed")
