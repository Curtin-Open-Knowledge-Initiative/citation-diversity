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
        FROM `academic-observatory.observatory.doi20211002`
    ),
    #collect articles' ids in MAG that cite articles from above
    citing_id AS (
        SELECT
            pr.PaperId AS PaperId,
            ARRAY_AGG(cited_id.PaperId) AS CitedId
        FROM `academic-observatory.mag.PaperReferences20210329` AS pr
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
            grids,
            (SELECT COUNT(X) FROM UNNEST(grids) AS X) as grids_count,
            affiliations.institutions,
            affiliations.countries,
            affiliations.subregions,
            affiliations.regions,
            affiliations.authors,
            CitedId
        FROM citing_id
            LEFT JOIN `academic-observatory.observatory.doi20210807` ON PaperId = mag.PaperId
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
            unpaywall.is_oa as is_oa,
            unpaywall.gold as gold,
            unpaywall.green as green,
            unpaywall.green_only as green_only,
            mag.PaperId AS PaperId,
            mag.CitationCount as CitationCount,
            C1.CitingCountries_count_all AS CitingCountries_count_all,
            C1.CitingCountries_count_uniq AS CitingCountries_count_uniq,
            C1.CitingCountries_name AS CitingCountries_name,
            GetNamesAndCounts(C1.CitingCountries_name) AS CitingCountries_table,
            C2.CitingSubregions_count_all AS CitingSubregions_count_all,
            C2.CitingSubregions_count_uniq AS CitingSubregions_count_uniq,
            C2.CitingSubregions_name AS CitingSubregions_name,
            GetNamesAndCounts(C2.CitingSubregions_name) AS CitingSubregions_table,
            C3.CitingRegions_count_all AS CitingRegions_count_all,
            C3.CitingRegions_count_uniq AS CitingRegions_count_uniq,
            C3.CitingRegions_name AS CitingRegions_name,
            GetNamesAndCounts(C3.CitingRegions_name) AS CitingRegions_table,
            C4.CitingFields_count_all AS CitingFields_count_all,
            C4.CitingFields_count_uniq AS CitingFields_count_uniq,
            C4.CitingFields_name AS CitingFields_name,
            GetNamesAndCounts(C4.CitingFields_name) AS CitingFields_table,
        FROM `academic-observatory.observatory.doi20211002` AS outputs
            LEFT JOIN CitingCountries AS C1 ON outputs.mag.PaperId = C1.PaperId
            LEFT JOIN CitingSubregions AS C2 ON outputs.mag.PaperId = C2.PaperId
            LEFT JOIN CitingRegions AS C3 ON outputs.mag.PaperId = C3.PaperId
            LEFT JOIN CitingFields AS C4 ON outputs.mag.PaperId = C4.PaperId
    )
SELECT
  *,
  (SELECT 1 - SUM(POW(X.count/CitingCountries_count_all,2)) FROM UNNEST(CitingCountries_table) AS X) as CitingCountries_unalike,
  (SELECT 1 - SUM(POW(X.count/CitingSubregions_count_all,2)) FROM UNNEST(CitingSubregions_table) AS X) as CitingSubregions_unalike,
  (SELECT 1 - SUM(POW(X.count/CitingRegions_count_all,2)) FROM UNNEST(CitingRegions_table) AS X) as CitingRegions_unalike,
  (SELECT 1 - SUM(POW(X.count/CitingFields_count_all,2)) FROM UNNEST(CitingFields_table) AS X) as CitingFields_unalike
FROM cited_articles
