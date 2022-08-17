/*
## Summary
Generates annual citation counts between regions

## Description
Creates a table that lists for each cited region and publication year:
- DOI counts for OA and non-OA outputs;
- Number of citations from all citing region to OA papers affiliated to the cited region;
- Number of citations from all citing region to non-OA papers affiliated to the cited region.

## Contacts
karl.huang@curtin.edu.au

## Requires
table bigquery://{citation_diversity_table}

## Creates
file summary_stats_by_region_atleast2cit.csv

*/

WITH
  datatemp1 AS (
    SELECT
      region.name AS region_cited,
      year,
      is_oa,
      ARRAY_CONCAT_AGG(CitingRegions_table) AS CitingRegions_table_temp,
      COUNT(doi) AS count_doi
    FROM `{citation_diversity_table}`, UNNEST(regions) AS region
    WHERE (CitationCount >= 2) AND (region.name IS NOT NULL) AND (year IS NOT NULL) AND (is_oa IS NOT NULL)
    GROUP BY region.name, year, is_oa
  ),
  datatemp2 AS (
    SELECT
      * EXCEPT(CitingRegions_table_temp),
    ARRAY(SELECT AS STRUCT name, SUM(count) AS total FROM UNNEST(CitingRegions_table_temp) AS X GROUP BY name) AS CitingRegions_table_all
  FROM datatemp1
  )
SELECT
  region_cited,
  year,
  is_oa,
  count_doi,
  X.name AS region_citing,
  X.total AS region_citing_count
FROM datatemp2, UNNEST(CitingRegions_table_all) AS X
