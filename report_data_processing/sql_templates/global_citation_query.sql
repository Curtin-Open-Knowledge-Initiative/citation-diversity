/*
## Summary

Creates the main DOI level citation diversity table to be deployed to BigQuery

## Description

## Contacts
karl.huang@curtin.edu.au

## Requires
table bigquery://{doi_table}
table bigquery://{mag_references_table}

## Creates
table bigquery://{citation_diversity_table}

*/

#function for creating frequency table from a list of names
CREATE TEMP FUNCTION GetNamesAndCounts(elements ARRAY<STRING>) AS (
  ARRAY(
    SELECT AS STRUCT elem AS name, COUNT(*) AS count
    FROM UNNEST(elements) AS elem
    GROUP BY elem
    ORDER BY count
  )
);

WITH 
    #collect all article id for global outputs
    cited_id AS (
        SELECT
            DISTINCT(mag.PaperId)
        FROM `{doi_table}`
    ),
    #collect articles' ids in MAG that cite articles from above
    citing_id AS (
        SELECT
            pr.PaperId AS PaperId,
            ARRAY_AGG(cited_id.PaperId) AS CitedId
        FROM `{mag_references_table}` AS pr
            JOIN cited_id on pr.PaperReferenceId = cited_id.PaperId 
        GROUP BY 
            pr.PaperId
    ),
    #create a list of citing articles with relevant metadata
    citing_articles AS (
        SELECT 
            doi,
            crossref.title,
            crossref.published_year,
            crossref.type,
            crossref.container_title,
            unpaywall.is_oa,
            unpaywall.gold,
            unpaywall.green,
            unpaywall.green_only,
            mag.PaperId,
            mag.PaperTitle,
            mag.CitationCount,
            mag.fields,
            events.events,
            # grids,
            # (SELECT COUNT(X) FROM UNNEST(grids) AS X) as grids_count,
            affiliations.institutions,
            affiliations.countries,
            affiliations.subregions,
            affiliations.regions,
            affiliations.authors,
            CitedId
        FROM citing_id
            LEFT JOIN `{doi_table}` ON PaperId = mag.PaperId
    ),
    #group citing institutions to cited articles
    CitingInstitutions AS (
        SELECT Cited AS PaperId, ARRAY_AGG(institution.name IGNORE NULLS) AS CitingInstitutions_name, COUNT(DISTINCT(institution.name)) AS CitingInstitutions_count_uniq,
               COUNT(institution.name) AS CitingInstitutions_count_all
        FROM citing_articles AS X, UNNEST(CitedId) AS Cited, UNNEST(institutions) AS institution
        GROUP BY Cited
    ),
    #group citing countries to cited articles
    CitingCountries AS (
        SELECT Cited AS PaperId, ARRAY_AGG(country.name IGNORE NULLS) AS CitingCountries_name, COUNT(DISTINCT(country.name)) AS CitingCountries_count_uniq,
               COUNT(country.name) AS CitingCountries_count_all
        FROM citing_articles AS X, UNNEST(CitedId) AS Cited, UNNEST(countries) AS country
        GROUP BY Cited
    ),
    #group citing subregions to cited articles
    CitingSubregions AS (
        SELECT Cited AS PaperId, ARRAY_AGG(subregion.name IGNORE NULLS) AS CitingSubregions_name, COUNT(DISTINCT(subregion.name)) AS CitingSubregions_count_uniq,
               COUNT(subregion.name) AS CitingSubregions_count_all
        FROM citing_articles AS X, UNNEST(CitedId) AS Cited, UNNEST(subregions) AS subregion
        GROUP BY Cited
    ),
    #group citing regions to cited articles
    CitingRegions AS (
        SELECT Cited AS PaperId, ARRAY_AGG(region.name IGNORE NULLS) AS CitingRegions_name, COUNT(DISTINCT(region.name)) AS CitingRegions_count_uniq,
               COUNT(region.name) AS CitingRegions_count_all
        FROM citing_articles AS X, UNNEST(CitedId) AS Cited, UNNEST(regions) AS region
        GROUP BY Cited
    ),
    #group citing fields to cited articles
    CitingFields AS (
        SELECT Cited AS PaperId, ARRAY_AGG(field.DisplayName IGNORE NULLS) AS CitingFields_name, COUNT(DISTINCT(field.DisplayName)) AS CitingFields_count_uniq,
               COUNT(field.DisplayName) AS CitingFields_count_all
        FROM citing_articles AS X, UNNEST(CitedId) AS Cited, UNNEST(fields.level_0) AS field
        GROUP BY Cited
    ),
    #create list of cited articles with citing entities info
    cited_articles AS (
        SELECT 
            doi,
            crossref.published_year as year,
            crossref.type as doctype,
            unpaywall.is_oa as is_oa,
            unpaywall.gold as gold,
            unpaywall.green as green,
            unpaywall.green_only as green_only,
            unpaywall.hybrid as hybrid,
            unpaywall.bronze as bronze,
            mag.PaperId AS PaperId,
            mag.CitationCount as CitationCount,
            mag.fields.level_0 as fields,
            C1.CitingInstitutions_count_all AS CitingInstitutions_count_all,
            C1.CitingInstitutions_count_uniq AS CitingInstitutions_count_uniq,
            C1.CitingInstitutions_name AS CitingInstitutions_name,
            GetNamesAndCounts(C1.CitingInstitutions_name) AS CitingInstitutions_table,
            C2.CitingCountries_count_all AS CitingCountries_count_all,
            C2.CitingCountries_count_uniq AS CitingCountries_count_uniq,
            C2.CitingCountries_name AS CitingCountries_name,
            GetNamesAndCounts(C2.CitingCountries_name) AS CitingCountries_table,
            C3.CitingSubregions_count_all AS CitingSubregions_count_all,
            C3.CitingSubregions_count_uniq AS CitingSubregions_count_uniq,
            C3.CitingSubregions_name AS CitingSubregions_name,
            GetNamesAndCounts(C3.CitingSubregions_name) AS CitingSubregions_table,
            C4.CitingRegions_count_all AS CitingRegions_count_all,
            C4.CitingRegions_count_uniq AS CitingRegions_count_uniq,
            C4.CitingRegions_name AS CitingRegions_name,
            GetNamesAndCounts(C4.CitingRegions_name) AS CitingRegions_table,
            C5.CitingFields_count_all AS CitingFields_count_all,
            C5.CitingFields_count_uniq AS CitingFields_count_uniq,
            C5.CitingFields_name AS CitingFields_name,
            GetNamesAndCounts(C5.CitingFields_name) AS CitingFields_table,
            affiliations.institutions,
            affiliations.countries,
            affiliations.subregions,
            affiliations.regions,
        FROM `{doi_table}` AS outputs
            LEFT JOIN CitingInstitutions AS C1 ON outputs.mag.PaperId = C1.PaperId  
            LEFT JOIN CitingCountries AS C2 ON outputs.mag.PaperId = C2.PaperId  
            LEFT JOIN CitingSubregions AS C3 ON outputs.mag.PaperId = C3.PaperId 
            LEFT JOIN CitingRegions AS C4 ON outputs.mag.PaperId = C4.PaperId 
            LEFT JOIN CitingFields AS C5 ON outputs.mag.PaperId = C5.PaperId 
    )
SELECT
  *,
  #calculate the Gini-Simpson index for various different groupings
  (SELECT 1 - SUM(POW(X.count/CitingInstitutions_count_all,2)) FROM UNNEST(CitingInstitutions_table) AS X) as CitingInstitutions_GiniSim,
  (SELECT 1 - SUM(POW(X.count/CitingCountries_count_all,2)) FROM UNNEST(CitingCountries_table) AS X) as CitingCountries_GiniSim,
  (SELECT 1 - SUM(POW(X.count/CitingSubregions_count_all,2)) FROM UNNEST(CitingSubregions_table) AS X) as CitingSubregions_GiniSim,
  (SELECT 1 - SUM(POW(X.count/CitingRegions_count_all,2)) FROM UNNEST(CitingRegions_table) AS X) as CitingRegions_GiniSim,
  (SELECT 1 - SUM(POW(X.count/CitingFields_count_all,2)) FROM UNNEST(CitingFields_table) AS X) as CitingFields_GiniSim,
  #calculate the Shannon (entropy) index for various different groupings
  (SELECT -SUM((X.count/CitingInstitutions_count_all)*LN(X.count/CitingInstitutions_count_all)) FROM UNNEST(CitingInstitutions_table) AS X) as CitingInstitutions_Shannon,
  (SELECT -SUM((X.count/CitingCountries_count_all)*LN(X.count/CitingCountries_count_all)) FROM UNNEST(CitingCountries_table) AS X) as CitingCountries_Shannon,
  (SELECT -SUM((X.count/CitingSubregions_count_all)*LN(X.count/CitingSubregions_count_all)) FROM UNNEST(CitingSubregions_table) AS X) as CitingSubregions_Shannon,
  (SELECT -SUM((X.count/CitingRegions_count_all)*LN(X.count/CitingRegions_count_all)) FROM UNNEST(CitingRegions_table) AS X) as CitingRegions_Shannon,
  (SELECT -SUM((X.count/CitingFields_count_all)*LN(X.count/CitingFields_count_all)) FROM UNNEST(CitingFields_table) AS X) as CitingFields_Shannon
FROM cited_articles
WHERE 
  (PaperId IS NOT NULL) AND (year >= {first_year}) AND (year <= {last_year})
