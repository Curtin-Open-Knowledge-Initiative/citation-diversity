/*
## Summary
Generates annual citation counts between subregions

## Description
Creates a table that lists for each cited subregion and publication year:
- DOI counts for OA and non-OA outputs;
- Number of citations from all citing subregion to OA papers affiliated to the cited subregion;
- Number of citations from all citing subregion to non-OA papers affiliated to the cited subregion.

## Contacts
karl.huang@curtin.edu.au

## Requires
table bigquery://coki-scratch-space.citation_diversity_analysis.citation_diversity_global

## Creates
file summary_stats_by_subregion_atleast2cit.csv

*/
WITH
  datatemp1 AS (
    SELECT
      subregion.name AS subregion_cited,
      year,
      is_oa,
      ARRAY_CONCAT_AGG(CitingSubregions_table) AS CitingSubregions_table_temp,
      COUNT(doi) AS count_doi
    FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global`, UNNEST(subregions) AS subregion
    WHERE (CitationCount >= 2) AND (subregion.name IS NOT NULL) AND (year IS NOT NULL) AND (is_oa IS NOT NULL)
    GROUP BY subregion.name, year, is_oa
  ),
  datatemp2 AS (
    SELECT
      * EXCEPT(CitingSubregions_table_temp),
    ARRAY(SELECT AS STRUCT name, SUM(count) AS total FROM UNNEST(CitingSubregions_table_temp) AS X GROUP BY name) AS CitingSubregions_table_all
  FROM datatemp1
  )
SELECT
  subregion_cited,
  year,
  is_oa,
  count_doi,
  X.name AS subregion_citing,
  X.total AS subregion_citing_count
FROM datatemp2, UNNEST(CitingSubregions_table_all) AS X
