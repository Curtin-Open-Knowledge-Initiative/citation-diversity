DECLARE y INT64 DEFAULT 2010;

WITH
  sample_oa AS (
      (SELECT
        doi,
        TRUE AS s_oa
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE CitationCount>=2 AND year=y AND is_oa=TRUE )
      ORDER BY FARM_FINGERPRINT(CONCAT(doi,'1'))
      LIMIT 10000)
  ),
  sample_noa AS (
      (SELECT
        doi,
        TRUE AS s_noa,
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE CitationCount>=2 AND year=y AND is_oa=FALSE )
      ORDER BY FARM_FINGERPRINT(CONCAT(doi,'2'))
      LIMIT 10000)
  ),
  sample_gold AS (
      (SELECT
        doi,
        TRUE AS s_gold,
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE CitationCount>=2 AND year=y AND gold=TRUE )
      ORDER BY FARM_FINGERPRINT(CONCAT(doi,'3'))
      LIMIT 10000)
  ),
  sample_green AS (
      (SELECT
        doi,
        TRUE AS s_green,
      FROM (SELECT * FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` WHERE CitationCount>=2 AND year=y AND green=TRUE )
      ORDER BY FARM_FINGERPRINT(CONCAT(doi,'4'))
      LIMIT 10000)
  )
SELECT
  doi,
  year,
  s_oa,
  s_noa,
  s_gold,
  s_green,
  CitationCount,
  CitingInstitutions_count_uniq,
  CitingCountries_count_uniq,
  CitingSubregions_count_uniq,
  CitingRegions_count_uniq,
  CitingFields_count_uniq,
  CitingInstitutions_GiniSim,
  CitingCountries_GiniSim,
  CitingSubregions_GiniSim,
  CitingRegions_GiniSim,
  CitingFields_GiniSim,
  CitingInstitutions_Shannon,
  CitingCountries_Shannon,
  CitingSubregions_Shannon,
  CitingRegions_Shannon,
  CitingFields_Shannon
FROM (sample_oa FULL JOIN sample_noa USING(doi)
                FULL JOIN sample_gold USING (doi)
                FULL JOIN sample_green USING(doi))
  LEFT JOIN `coki-scratch-space.citation_diversity_analysis.citation_diversity_global` USING(doi)

