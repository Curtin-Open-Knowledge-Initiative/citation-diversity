#This includes only papers that are cited at least twice
WITH
  DataTemp1 AS(
    SELECT *
    FROM `coki-scratch-space.citation_diversity_analysis.citation_diversity_global`
    WHERE year>=2010 AND year<=2019 AND is_oa IS NOT NULL AND CitationCount>=2
  ),
  DataTemp2 AS(
    SELECT
      doi,
      #median number of citations for each oa type and year
      PERCENTILE_CONT(CitationCount,0.5) OVER(PARTITION BY year, is_oa) AS oa_cc_median,
      PERCENTILE_CONT(CitationCount,0.5) OVER(PARTITION BY year, gold) AS gold_cc_median,
      PERCENTILE_CONT(CitationCount,0.5) OVER(PARTITION BY year, green) AS green_cc_median,
      PERCENTILE_CONT(CitationCount,0.5) OVER(PARTITION BY year, green_only) AS green_only_cc_median,
      PERCENTILE_CONT(CitationCount,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_cc_median,
      PERCENTILE_CONT(CitationCount,0.5) OVER(PARTITION BY year, bronze) AS bronze_cc_median,
      #median uniq counts of citing groups and diversity measures for oa papers
      PERCENTILE_CONT(CitingInstitutions_count_uniq,0.5) OVER(PARTITION BY year, is_oa) AS oa_Institutions_uniq_median,
      PERCENTILE_CONT(CitingCountries_count_uniq,0.5) OVER(PARTITION BY year, is_oa) AS oa_Countries_uniq_median,
      PERCENTILE_CONT(CitingSubregions_count_uniq,0.5) OVER(PARTITION BY year, is_oa) AS oa_Subregions_uniq_median,
      PERCENTILE_CONT(CitingRegions_count_uniq,0.5) OVER(PARTITION BY year, is_oa) AS oa_Regions_uniq_median,
      PERCENTILE_CONT(CitingFields_count_uniq,0.5) OVER(PARTITION BY year, is_oa) AS oa_Fields_uniq_median,
      PERCENTILE_CONT(CitingInstitutions_GiniSim,0.5) OVER(PARTITION BY year, is_oa) AS oa_Institutions_GiniSim_median,
      PERCENTILE_CONT(CitingCountries_GiniSim,0.5) OVER(PARTITION BY year, is_oa) AS oa_Countries_GiniSim_median,
      PERCENTILE_CONT(CitingSubregions_GiniSim,0.5) OVER(PARTITION BY year, is_oa) AS oa_Subregions_GiniSim_median,
      PERCENTILE_CONT(CitingRegions_GiniSim,0.5) OVER(PARTITION BY year, is_oa) AS oa_Regions_GiniSim_median,
      PERCENTILE_CONT(CitingFields_GiniSim,0.5) OVER(PARTITION BY year, is_oa) AS oa_Fields_GiniSim_median,
      PERCENTILE_CONT(CitingInstitutions_Shannon,0.5) OVER(PARTITION BY year, is_oa) AS oa_Institutions_Shannon_median,
      PERCENTILE_CONT(CitingCountries_Shannon,0.5) OVER(PARTITION BY year, is_oa) AS oa_Countries_Shannon_median,
      PERCENTILE_CONT(CitingSubregions_Shannon,0.5) OVER(PARTITION BY year, is_oa) AS oa_Subregions_Shannon_median,
      PERCENTILE_CONT(CitingRegions_Shannon,0.5) OVER(PARTITION BY year, is_oa) AS oa_Regions_Shannon_median,
      PERCENTILE_CONT(CitingFields_Shannon,0.5) OVER(PARTITION BY year, is_oa) AS oa_Fields_Shannon_median
    FROM DataTemp1
  ),
  DataTemp3 AS(
    SELECT
      doi,
      #median uniq counts of citing groups and diversity measures for gold papers
      PERCENTILE_CONT(CitingInstitutions_count_uniq,0.5) OVER(PARTITION BY year, gold) AS gold_Institutions_uniq_median,
      PERCENTILE_CONT(CitingCountries_count_uniq,0.5) OVER(PARTITION BY year, gold) AS gold_Countries_uniq_median,
      PERCENTILE_CONT(CitingSubregions_count_uniq,0.5) OVER(PARTITION BY year, gold) AS gold_Subregions_uniq_median,
      PERCENTILE_CONT(CitingRegions_count_uniq,0.5) OVER(PARTITION BY year, gold) AS gold_Regions_uniq_median,
      PERCENTILE_CONT(CitingFields_count_uniq,0.5) OVER(PARTITION BY year, gold) AS gold_Fields_uniq_median,
      PERCENTILE_CONT(CitingInstitutions_GiniSim,0.5) OVER(PARTITION BY year, gold) AS gold_Institutions_GiniSim_median,
      PERCENTILE_CONT(CitingCountries_GiniSim,0.5) OVER(PARTITION BY year, gold) AS gold_Countries_GiniSim_median,
      PERCENTILE_CONT(CitingSubregions_GiniSim,0.5) OVER(PARTITION BY year, gold) AS gold_Subregions_GiniSim_median,
      PERCENTILE_CONT(CitingRegions_GiniSim,0.5) OVER(PARTITION BY year, gold) AS gold_Regions_GiniSim_median,
      PERCENTILE_CONT(CitingFields_GiniSim,0.5) OVER(PARTITION BY year, gold) AS gold_Fields_GiniSim_median,
      PERCENTILE_CONT(CitingInstitutions_Shannon,0.5) OVER(PARTITION BY year, gold) AS gold_Institutions_Shannon_median,
      PERCENTILE_CONT(CitingCountries_Shannon,0.5) OVER(PARTITION BY year, gold) AS gold_Countries_Shannon_median,
      PERCENTILE_CONT(CitingSubregions_Shannon,0.5) OVER(PARTITION BY year, gold) AS gold_Subregions_Shannon_median,
      PERCENTILE_CONT(CitingRegions_Shannon,0.5) OVER(PARTITION BY year, gold) AS gold_Regions_Shannon_median,
      PERCENTILE_CONT(CitingFields_Shannon,0.5) OVER(PARTITION BY year, gold) AS gold_Fields_Shannon_median,
      #median uniq counts of citing groups and diversity measures for green papers
      PERCENTILE_CONT(CitingInstitutions_count_uniq,0.5) OVER(PARTITION BY year, green) AS green_Institutions_uniq_median,
      PERCENTILE_CONT(CitingCountries_count_uniq,0.5) OVER(PARTITION BY year, green) AS green_Countries_uniq_median,
      PERCENTILE_CONT(CitingSubregions_count_uniq,0.5) OVER(PARTITION BY year, green) AS green_Subregions_uniq_median,
      PERCENTILE_CONT(CitingRegions_count_uniq,0.5) OVER(PARTITION BY year, green) AS green_Regions_uniq_median,
      PERCENTILE_CONT(CitingFields_count_uniq,0.5) OVER(PARTITION BY year, green) AS green_Fields_uniq_median,
      PERCENTILE_CONT(CitingInstitutions_GiniSim,0.5) OVER(PARTITION BY year, green) AS green_Institutions_GiniSim_median,
      PERCENTILE_CONT(CitingCountries_GiniSim,0.5) OVER(PARTITION BY year, green) AS green_Countries_GiniSim_median,
      PERCENTILE_CONT(CitingSubregions_GiniSim,0.5) OVER(PARTITION BY year, green) AS green_Subregions_GiniSim_median,
      PERCENTILE_CONT(CitingRegions_GiniSim,0.5) OVER(PARTITION BY year, green) AS green_Regions_GiniSim_median,
      PERCENTILE_CONT(CitingFields_GiniSim,0.5) OVER(PARTITION BY year, green) AS green_Fields_GiniSim_median,
      PERCENTILE_CONT(CitingInstitutions_Shannon,0.5) OVER(PARTITION BY year, green) AS green_Institutions_Shannon_median,
      PERCENTILE_CONT(CitingCountries_Shannon,0.5) OVER(PARTITION BY year, green) AS green_Countries_Shannon_median,
      PERCENTILE_CONT(CitingSubregions_Shannon,0.5) OVER(PARTITION BY year, green) AS green_Subregions_Shannon_median,
      PERCENTILE_CONT(CitingRegions_Shannon,0.5) OVER(PARTITION BY year, green) AS green_Regions_Shannon_median,
      PERCENTILE_CONT(CitingFields_Shannon,0.5) OVER(PARTITION BY year, green) AS green_Fields_Shannon_median,
    FROM DataTemp1
  ),
  DataTemp4 AS(
    SELECT
      doi,
      #median uniq counts of citing groups and diversity measures for green only papers
      PERCENTILE_CONT(CitingInstitutions_count_uniq,0.5) OVER(PARTITION BY year, green_only) AS green_only_Institutions_uniq_median,
      PERCENTILE_CONT(CitingCountries_count_uniq,0.5) OVER(PARTITION BY year, green_only) AS green_only_Countries_uniq_median,
      PERCENTILE_CONT(CitingSubregions_count_uniq,0.5) OVER(PARTITION BY year, green_only) AS green_only_Subregions_uniq_median,
      PERCENTILE_CONT(CitingRegions_count_uniq,0.5) OVER(PARTITION BY year, green_only) AS green_only_Regions_uniq_median,
      PERCENTILE_CONT(CitingFields_count_uniq,0.5) OVER(PARTITION BY year, green_only) AS green_only_Fields_uniq_median,
      PERCENTILE_CONT(CitingInstitutions_GiniSim,0.5) OVER(PARTITION BY year, green_only) AS green_only_Institutions_GiniSim_median,
      PERCENTILE_CONT(CitingCountries_GiniSim,0.5) OVER(PARTITION BY year, green_only) AS green_only_Countries_GiniSim_median,
      PERCENTILE_CONT(CitingSubregions_GiniSim,0.5) OVER(PARTITION BY year, green_only) AS green_only_Subregions_GiniSim_median,
      PERCENTILE_CONT(CitingRegions_GiniSim,0.5) OVER(PARTITION BY year, green_only) AS green_only_Regions_GiniSim_median,
      PERCENTILE_CONT(CitingFields_GiniSim,0.5) OVER(PARTITION BY year, green_only) AS green_only_Fields_GiniSim_median,
      PERCENTILE_CONT(CitingInstitutions_Shannon,0.5) OVER(PARTITION BY year, green_only) AS green_only_Institutions_Shannon_median,
      PERCENTILE_CONT(CitingCountries_Shannon,0.5) OVER(PARTITION BY year, green_only) AS green_only_Countries_Shannon_median,
      PERCENTILE_CONT(CitingSubregions_Shannon,0.5) OVER(PARTITION BY year, green_only) AS green_only_Subregions_Shannon_median,
      PERCENTILE_CONT(CitingRegions_Shannon,0.5) OVER(PARTITION BY year, green_only) AS green_only_Regions_Shannon_median,
      PERCENTILE_CONT(CitingFields_Shannon,0.5) OVER(PARTITION BY year, green_only) AS green_only_Fields_Shannon_median,
      #median uniq counts of citing groups and diversity measures for hybrid papers
      PERCENTILE_CONT(CitingInstitutions_count_uniq,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_Institutions_uniq_median,
      PERCENTILE_CONT(CitingCountries_count_uniq,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_Countries_uniq_median,
      PERCENTILE_CONT(CitingSubregions_count_uniq,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_Subregions_uniq_median,
      PERCENTILE_CONT(CitingRegions_count_uniq,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_Regions_uniq_median,
      PERCENTILE_CONT(CitingFields_count_uniq,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_Fields_uniq_median,
      PERCENTILE_CONT(CitingInstitutions_GiniSim,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_Institutions_GiniSim_median,
      PERCENTILE_CONT(CitingCountries_GiniSim,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_Countries_GiniSim_median,
      PERCENTILE_CONT(CitingSubregions_GiniSim,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_Subregions_GiniSim_median,
      PERCENTILE_CONT(CitingRegions_GiniSim,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_Regions_GiniSim_median,
      PERCENTILE_CONT(CitingFields_GiniSim,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_Fields_GiniSim_median,
      PERCENTILE_CONT(CitingInstitutions_Shannon,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_Institutions_Shannon_median,
      PERCENTILE_CONT(CitingCountries_Shannon,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_Countries_Shannon_median,
      PERCENTILE_CONT(CitingSubregions_Shannon,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_Subregions_Shannon_median,
      PERCENTILE_CONT(CitingRegions_Shannon,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_Regions_Shannon_median,
      PERCENTILE_CONT(CitingFields_Shannon,0.5) OVER(PARTITION BY year, hybrid) AS hybrid_Fields_Shannon_median
    FROM DataTemp1
  ),
  DataTemp5 AS(
    SELECT
      doi,
      #median uniq counts of citing groups and diversity measures for bronze papers
      PERCENTILE_CONT(CitingInstitutions_count_uniq,0.5) OVER(PARTITION BY year, bronze) AS bronze_Institutions_uniq_median,
      PERCENTILE_CONT(CitingCountries_count_uniq,0.5) OVER(PARTITION BY year, bronze) AS bronze_Countries_uniq_median,
      PERCENTILE_CONT(CitingSubregions_count_uniq,0.5) OVER(PARTITION BY year, bronze) AS bronze_Subregions_uniq_median,
      PERCENTILE_CONT(CitingRegions_count_uniq,0.5) OVER(PARTITION BY year, bronze) AS bronze_Regions_uniq_median,
      PERCENTILE_CONT(CitingFields_count_uniq,0.5) OVER(PARTITION BY year, bronze) AS bronze_Fields_uniq_median,
      PERCENTILE_CONT(CitingInstitutions_GiniSim,0.5) OVER(PARTITION BY year, bronze) AS bronze_Institutions_GiniSim_median,
      PERCENTILE_CONT(CitingCountries_GiniSim,0.5) OVER(PARTITION BY year, bronze) AS bronze_Countries_GiniSim_median,
      PERCENTILE_CONT(CitingSubregions_GiniSim,0.5) OVER(PARTITION BY year, bronze) AS bronze_Subregions_GiniSim_median,
      PERCENTILE_CONT(CitingRegions_GiniSim,0.5) OVER(PARTITION BY year, bronze) AS bronze_Regions_GiniSim_median,
      PERCENTILE_CONT(CitingFields_GiniSim,0.5) OVER(PARTITION BY year, bronze) AS bronze_Fields_GiniSim_median,
      PERCENTILE_CONT(CitingInstitutions_Shannon,0.5) OVER(PARTITION BY year, bronze) AS bronze_Institutions_Shannon_median,
      PERCENTILE_CONT(CitingCountries_Shannon,0.5) OVER(PARTITION BY year, bronze) AS bronze_Countries_Shannon_median,
      PERCENTILE_CONT(CitingSubregions_Shannon,0.5) OVER(PARTITION BY year, bronze) AS bronze_Subregions_Shannon_median,
      PERCENTILE_CONT(CitingRegions_Shannon,0.5) OVER(PARTITION BY year, bronze) AS bronze_Regions_Shannon_median,
      PERCENTILE_CONT(CitingFields_Shannon,0.5) OVER(PARTITION BY year, bronze) AS bronze_Fields_Shannon_median
    FROM DataTemp1
  ),
  DataTempAll AS(
    SELECT *
    FROM DataTemp1
      JOIN DataTemp2 USING(doi)
      JOIN DataTemp3 USING(doi)
      JOIN DataTemp4 USING(doi)
      JOIN DataTemp5 USING(doi)
  )
SELECT
  year,
  #count of dois for each oa type
  COUNT(doi) as doi_count,
  COUNT(IF(is_oa=TRUE, doi, NULL)) as oa_count,
  COUNT(IF(is_oa=FALSE, doi, NULL)) as noa_count,
  COUNT(IF(gold=TRUE, doi, NULL)) as gold_count,
  COUNT(IF(green=TRUE, doi, NULL)) as green_count,
  COUNT(IF(green_only=TRUE, doi, NULL)) as green_only_count,
  COUNT(IF(hybrid=TRUE, doi, NULL)) as hybrid_count,
  COUNT(IF(bronze=TRUE, doi, NULL)) as bronze_count,
  #mean and median citation count for each oa type
  AVG(IF(is_oa=TRUE , CitationCount, NULL)) as oa_cc_mean,
  ANY_VALUE(IF(is_oa=TRUE,oa_cc_median,NULL)) as oa_cc_median,
  AVG(IF(is_oa=FALSE, CitationCount, NULL)) as noa_cc_mean,
  ANY_VALUE(IF(is_oa=FALSE,oa_cc_median,NULL)) as noa_cc_median,
  AVG(IF(gold=TRUE , CitationCount, NULL)) as gold_cc_mean,
  ANY_VALUE(IF(gold=TRUE,gold_cc_median,NULL)) as gold_cc_median,
  AVG(IF(green=TRUE , CitationCount, NULL)) as green_cc_mean,
  ANY_VALUE(IF(green=TRUE,green_cc_median,NULL)) as green_cc_median,
  AVG(IF(green_only=TRUE , CitationCount, NULL)) as green_only_cc_mean,
  ANY_VALUE(IF(green_only=TRUE,green_only_cc_median,NULL)) as green_only_cc_median,
  AVG(IF(hybrid=TRUE , CitationCount, NULL)) as hybrid_cc_mean,
  ANY_VALUE(IF(hybrid=TRUE,hybrid_cc_median,NULL)) as hybrid_cc_median,
  AVG(IF(bronze=TRUE , CitationCount, NULL)) as bronze_cc_mean,
  ANY_VALUE(IF(bronze=TRUE,bronze_cc_median,NULL)) as bronze_cc_median,
  #mean and median unique citing groups and diversity measures for oa
  AVG(IF(is_oa=TRUE, CitingInstitutions_count_uniq, NULL)) as oa_Institutions_uniq_mean,
  ANY_VALUE(IF(is_oa=TRUE, oa_Institutions_uniq_median, NULL)) as oa_Institutions_uniq_median,
  AVG(IF(is_oa=TRUE, CitingCountries_count_uniq, NULL)) as oa_Countries_uniq_mean,
  ANY_VALUE(IF(is_oa=TRUE, oa_Countries_uniq_median, NULL)) as oa_Countries_uniq_median,
  AVG(IF(is_oa=TRUE, CitingSubregions_count_uniq, NULL)) as oa_Subregions_uniq_mean,
  ANY_VALUE(IF(is_oa=TRUE, oa_Subregions_uniq_median, NULL)) as oa_Subregions_uniq_median,
  AVG(IF(is_oa=TRUE, CitingRegions_count_uniq, NULL)) as oa_Regions_uniq_mean,
  ANY_VALUE(IF(is_oa=TRUE, oa_Regions_uniq_median, NULL)) as oa_Regions_uniq_median,
  AVG(IF(is_oa=TRUE, CitingFields_count_uniq, NULL)) as oa_Fields_uniq_mean,
  ANY_VALUE(IF(is_oa=TRUE, oa_Fields_uniq_median, NULL)) as oa_Fields_uniq_median,
  AVG(IF(is_oa=TRUE, CitingInstitutions_GiniSim, NULL)) as oa_Institutions_GiniSim_mean,
  ANY_VALUE(IF(is_oa=TRUE, oa_Institutions_GiniSim_median, NULL)) as oa_Institutions_GiniSim_median,
  AVG(IF(is_oa=TRUE, CitingCountries_GiniSim, NULL)) as oa_Countries_GiniSim_mean,
  ANY_VALUE(IF(is_oa=TRUE, oa_Countries_GiniSim_median, NULL)) as oa_Countries_GiniSim_median,
  AVG(IF(is_oa=TRUE, CitingSubregions_GiniSim, NULL)) as oa_Subregions_GiniSim_mean,
  ANY_VALUE(IF(is_oa=TRUE, oa_Subregions_GiniSim_median, NULL)) as oa_Subregions_GiniSim_median,
  AVG(IF(is_oa=TRUE, CitingRegions_GiniSim, NULL)) as oa_Regions_GiniSim_mean,
  ANY_VALUE(IF(is_oa=TRUE, oa_Regions_GiniSim_median, NULL)) as oa_Regions_GiniSim_median,
  AVG(IF(is_oa=TRUE, CitingFields_GiniSim, NULL)) as oa_Fields_GiniSim_mean,
  ANY_VALUE(IF(is_oa=TRUE, oa_Fields_GiniSim_median, NULL)) as oa_Fields_GiniSim_median,
  AVG(IF(is_oa=TRUE, CitingInstitutions_Shannon, NULL)) as oa_Institutions_Shannon_mean,
  ANY_VALUE(IF(is_oa=TRUE, oa_Institutions_Shannon_median, NULL)) as oa_Institutions_Shannon_median,
  AVG(IF(is_oa=TRUE, CitingCountries_Shannon, NULL)) as oa_Countries_Shannon_mean,
  ANY_VALUE(IF(is_oa=TRUE, oa_Countries_Shannon_median, NULL)) as oa_Countries_Shannon_median,
  AVG(IF(is_oa=TRUE, CitingSubregions_Shannon, NULL)) as oa_Subregions_Shannon_mean,
  ANY_VALUE(IF(is_oa=TRUE, oa_Subregions_Shannon_median, NULL)) as oa_Subregions_Shannon_median,
  AVG(IF(is_oa=TRUE, CitingRegions_Shannon, NULL)) as oa_Regions_Shannon_mean,
  ANY_VALUE(IF(is_oa=TRUE, oa_Regions_Shannon_median, NULL)) as oa_Regions_Shannon_median,
  AVG(IF(is_oa=TRUE, CitingFields_Shannon, NULL)) as oa_Fields_Shannon_mean,
  ANY_VALUE(IF(is_oa=TRUE, oa_Fields_Shannon_median, NULL)) as oa_Fields_Shannon_median,
  #mean and median unique citing groups and diversity measures for non-oa
  AVG(IF(is_oa=FALSE, CitingInstitutions_count_uniq, NULL)) as noa_Institutions_uniq_mean,
  ANY_VALUE(IF(is_oa=FALSE, oa_Institutions_uniq_median, NULL)) as noa_Institutions_uniq_median,
  AVG(IF(is_oa=FALSE, CitingCountries_count_uniq, NULL)) as noa_Countries_uniq_mean,
  ANY_VALUE(IF(is_oa=FALSE, oa_Countries_uniq_median, NULL)) as noa_Countries_uniq_median,
  AVG(IF(is_oa=FALSE, CitingSubregions_count_uniq, NULL)) as noa_Subregions_uniq_mean,
  ANY_VALUE(IF(is_oa=FALSE, oa_Subregions_uniq_median, NULL)) as noa_Subregions_uniq_median,
  AVG(IF(is_oa=FALSE, CitingRegions_count_uniq, NULL)) as noa_Regions_uniq_mean,
  ANY_VALUE(IF(is_oa=FALSE, oa_Regions_uniq_median, NULL)) as noa_Regions_uniq_median,
  AVG(IF(is_oa=FALSE, CitingFields_count_uniq, NULL)) as noa_Fields_uniq_mean,
  ANY_VALUE(IF(is_oa=FALSE, oa_Fields_uniq_median, NULL)) as noa_Fields_uniq_median,
  AVG(IF(is_oa=FALSE, CitingInstitutions_GiniSim, NULL)) as noa_Institutions_GiniSim_mean,
  ANY_VALUE(IF(is_oa=FALSE, oa_Institutions_GiniSim_median, NULL)) as noa_Institutions_GiniSim_median,
  AVG(IF(is_oa=FALSE, CitingCountries_GiniSim, NULL)) as noa_Countries_GiniSim_mean,
  ANY_VALUE(IF(is_oa=FALSE, oa_Countries_GiniSim_median, NULL)) as noa_Countries_GiniSim_median,
  AVG(IF(is_oa=FALSE, CitingSubregions_GiniSim, NULL)) as noa_Subregions_GiniSim_mean,
  ANY_VALUE(IF(is_oa=FALSE, oa_Subregions_GiniSim_median, NULL)) as noa_Subregions_GiniSim_median,
  AVG(IF(is_oa=FALSE, CitingRegions_GiniSim, NULL)) as noa_Regions_GiniSim_mean,
  ANY_VALUE(IF(is_oa=FALSE, oa_Regions_GiniSim_median, NULL)) as noa_Regions_GiniSim_median,
  AVG(IF(is_oa=FALSE, CitingFields_GiniSim, NULL)) as noa_Fields_GiniSim_mean,
  ANY_VALUE(IF(is_oa=FALSE, oa_Fields_GiniSim_median, NULL)) as noa_Fields_GiniSim_median,
  AVG(IF(is_oa=FALSE, CitingInstitutions_Shannon, NULL)) as noa_Institutions_Shannon_mean,
  ANY_VALUE(IF(is_oa=FALSE, oa_Institutions_Shannon_median, NULL)) as noa_Institutions_Shannon_median,
  AVG(IF(is_oa=FALSE, CitingCountries_Shannon, NULL)) as noa_Countries_Shannon_mean,
  ANY_VALUE(IF(is_oa=FALSE, oa_Countries_Shannon_median, NULL)) as noa_Countries_Shannon_median,
  AVG(IF(is_oa=FALSE, CitingSubregions_Shannon, NULL)) as noa_Subregions_Shannon_mean,
  ANY_VALUE(IF(is_oa=FALSE, oa_Subregions_Shannon_median, NULL)) as noa_Subregions_Shannon_median,
  AVG(IF(is_oa=FALSE, CitingRegions_Shannon, NULL)) as noa_Regions_Shannon_mean,
  ANY_VALUE(IF(is_oa=FALSE, oa_Regions_Shannon_median, NULL)) as noa_Regions_Shannon_median,
  AVG(IF(is_oa=FALSE, CitingFields_Shannon, NULL)) as noa_Fields_Shannon_mean,
  ANY_VALUE(IF(is_oa=FALSE, oa_Fields_Shannon_median, NULL)) as noa_Fields_Shannon_median,
  #mean and median unique citing groups and diversity measures for gold
  AVG(IF(gold=TRUE, CitingInstitutions_count_uniq, NULL)) as gold_Institutions_uniq_mean,
  ANY_VALUE(IF(gold=TRUE, gold_Institutions_uniq_median, NULL)) as gold_Institutions_uniq_median,
  AVG(IF(gold=TRUE, CitingCountries_count_uniq, NULL)) as gold_Countries_uniq_mean,
  ANY_VALUE(IF(gold=TRUE, gold_Countries_uniq_median, NULL)) as gold_Countries_uniq_median,
  AVG(IF(gold=TRUE, CitingSubregions_count_uniq, NULL)) as gold_Subregions_uniq_mean,
  ANY_VALUE(IF(gold=TRUE, gold_Subregions_uniq_median, NULL)) as gold_Subregions_uniq_median,
  AVG(IF(gold=TRUE, CitingRegions_count_uniq, NULL)) as gold_Regions_uniq_mean,
  ANY_VALUE(IF(gold=TRUE, gold_Regions_uniq_median, NULL)) as gold_Regions_uniq_median,
  AVG(IF(gold=TRUE, CitingFields_count_uniq, NULL)) as gold_Fields_uniq_mean,
  ANY_VALUE(IF(gold=TRUE, gold_Fields_uniq_median, NULL)) as gold_Fields_uniq_median,
  AVG(IF(gold=TRUE, CitingInstitutions_GiniSim, NULL)) as gold_Institutions_GiniSim_mean,
  ANY_VALUE(IF(gold=TRUE, gold_Institutions_GiniSim_median, NULL)) as gold_Institutions_GiniSim_median,
  AVG(IF(gold=TRUE, CitingCountries_GiniSim, NULL)) as gold_Countries_GiniSim_mean,
  ANY_VALUE(IF(gold=TRUE, gold_Countries_GiniSim_median, NULL)) as gold_Countries_GiniSim_median,
  AVG(IF(gold=TRUE, CitingSubregions_GiniSim, NULL)) as gold_Subregions_GiniSim_mean,
  ANY_VALUE(IF(gold=TRUE, gold_Subregions_GiniSim_median, NULL)) as gold_Subregions_GiniSim_median,
  AVG(IF(gold=TRUE, CitingRegions_GiniSim, NULL)) as gold_Regions_GiniSim_mean,
  ANY_VALUE(IF(gold=TRUE, gold_Regions_GiniSim_median, NULL)) as gold_Regions_GiniSim_median,
  AVG(IF(gold=TRUE, CitingFields_GiniSim, NULL)) as gold_Fields_GiniSim_mean,
  ANY_VALUE(IF(gold=TRUE, gold_Fields_GiniSim_median, NULL)) as gold_Fields_GiniSim_median,
  AVG(IF(gold=TRUE, CitingInstitutions_Shannon, NULL)) as gold_Institutions_Shannon_mean,
  ANY_VALUE(IF(gold=TRUE, gold_Institutions_Shannon_median, NULL)) as gold_Institutions_Shannon_median,
  AVG(IF(gold=TRUE, CitingCountries_Shannon, NULL)) as gold_Countries_Shannon_mean,
  ANY_VALUE(IF(gold=TRUE, gold_Countries_Shannon_median, NULL)) as gold_Countries_Shannon_median,
  AVG(IF(gold=TRUE, CitingSubregions_Shannon, NULL)) as gold_Subregions_Shannon_mean,
  ANY_VALUE(IF(gold=TRUE, gold_Subregions_Shannon_median, NULL)) as gold_Subregions_Shannon_median,
  AVG(IF(gold=TRUE, CitingRegions_Shannon, NULL)) as gold_Regions_Shannon_mean,
  ANY_VALUE(IF(gold=TRUE, gold_Regions_Shannon_median, NULL)) as gold_Regions_Shannon_median,
  AVG(IF(gold=TRUE, CitingFields_Shannon, NULL)) as gold_Fields_Shannon_mean,
  ANY_VALUE(IF(gold=TRUE, gold_Fields_Shannon_median, NULL)) as gold_Fields_Shannon_median,
  #mean and median unique citing groups and diversity measures for green
  AVG(IF(green=TRUE, CitingInstitutions_count_uniq, NULL)) as green_Institutions_uniq_mean,
  ANY_VALUE(IF(green=TRUE, green_Institutions_uniq_median, NULL)) as green_Institutions_uniq_median,
  AVG(IF(green=TRUE, CitingCountries_count_uniq, NULL)) as green_Countries_uniq_mean,
  ANY_VALUE(IF(green=TRUE, green_Countries_uniq_median, NULL)) as green_Countries_uniq_median,
  AVG(IF(green=TRUE, CitingSubregions_count_uniq, NULL)) as green_Subregions_uniq_mean,
  ANY_VALUE(IF(green=TRUE, green_Subregions_uniq_median, NULL)) as green_Subregions_uniq_median,
  AVG(IF(green=TRUE, CitingRegions_count_uniq, NULL)) as green_Regions_uniq_mean,
  ANY_VALUE(IF(green=TRUE, green_Regions_uniq_median, NULL)) as green_Regions_uniq_median,
  AVG(IF(green=TRUE, CitingFields_count_uniq, NULL)) as green_Fields_uniq_mean,
  ANY_VALUE(IF(green=TRUE, green_Fields_uniq_median, NULL)) as green_Fields_uniq_median,
  AVG(IF(green=TRUE, CitingInstitutions_GiniSim, NULL)) as green_Institutions_GiniSim_mean,
  ANY_VALUE(IF(green=TRUE, green_Institutions_GiniSim_median, NULL)) as green_Institutions_GiniSim_median,
  AVG(IF(green=TRUE, CitingCountries_GiniSim, NULL)) as green_Countries_GiniSim_mean,
  ANY_VALUE(IF(green=TRUE, green_Countries_GiniSim_median, NULL)) as green_Countries_GiniSim_median,
  AVG(IF(green=TRUE, CitingSubregions_GiniSim, NULL)) as green_Subregions_GiniSim_mean,
  ANY_VALUE(IF(green=TRUE, green_Subregions_GiniSim_median, NULL)) as green_Subregions_GiniSim_median,
  AVG(IF(green=TRUE, CitingRegions_GiniSim, NULL)) as green_Regions_GiniSim_mean,
  ANY_VALUE(IF(green=TRUE, green_Regions_GiniSim_median, NULL)) as green_Regions_GiniSim_median,
  AVG(IF(green=TRUE, CitingFields_GiniSim, NULL)) as green_Fields_GiniSim_mean,
  ANY_VALUE(IF(green=TRUE, green_Fields_GiniSim_median, NULL)) as green_Fields_GiniSim_median,
  AVG(IF(green=TRUE, CitingInstitutions_Shannon, NULL)) as green_Institutions_Shannon_mean,
  ANY_VALUE(IF(green=TRUE, green_Institutions_Shannon_median, NULL)) as green_Institutions_Shannon_median,
  AVG(IF(green=TRUE, CitingCountries_Shannon, NULL)) as green_Countries_Shannon_mean,
  ANY_VALUE(IF(green=TRUE, green_Countries_Shannon_median, NULL)) as green_Countries_Shannon_median,
  AVG(IF(green=TRUE, CitingSubregions_Shannon, NULL)) as green_Subregions_Shannon_mean,
  ANY_VALUE(IF(green=TRUE, green_Subregions_Shannon_median, NULL)) as green_Subregions_Shannon_median,
  AVG(IF(green=TRUE, CitingRegions_Shannon, NULL)) as green_Regions_Shannon_mean,
  ANY_VALUE(IF(green=TRUE, green_Regions_Shannon_median, NULL)) as green_Regions_Shannon_median,
  AVG(IF(green=TRUE, CitingFields_Shannon, NULL)) as green_Fields_Shannon_mean,
  ANY_VALUE(IF(green=TRUE, green_Fields_Shannon_median, NULL)) as green_Fields_Shannon_median,
  #mean and median unique citing groups and diversity measures for green only
  AVG(IF(green_only=TRUE, CitingInstitutions_count_uniq, NULL)) as green_only_Institutions_uniq_mean,
  ANY_VALUE(IF(green_only=TRUE, green_only_Institutions_uniq_median, NULL)) as green_only_Institutions_uniq_median,
  AVG(IF(green_only=TRUE, CitingCountries_count_uniq, NULL)) as green_only_Countries_uniq_mean,
  ANY_VALUE(IF(green_only=TRUE, green_only_Countries_uniq_median, NULL)) as green_only_Countries_uniq_median,
  AVG(IF(green_only=TRUE, CitingSubregions_count_uniq, NULL)) as green_only_Subregions_uniq_mean,
  ANY_VALUE(IF(green_only=TRUE, green_only_Subregions_uniq_median, NULL)) as green_only_Subregions_uniq_median,
  AVG(IF(green_only=TRUE, CitingRegions_count_uniq, NULL)) as green_only_Regions_uniq_mean,
  ANY_VALUE(IF(green_only=TRUE, green_only_Regions_uniq_median, NULL)) as green_only_Regions_uniq_median,
  AVG(IF(green_only=TRUE, CitingFields_count_uniq, NULL)) as green_only_Fields_uniq_mean,
  ANY_VALUE(IF(green_only=TRUE, green_only_Fields_uniq_median, NULL)) as green_only_Fields_uniq_median,
  AVG(IF(green_only=TRUE, CitingInstitutions_GiniSim, NULL)) as green_only_Institutions_GiniSim_mean,
  ANY_VALUE(IF(green_only=TRUE, green_only_Institutions_GiniSim_median, NULL)) as green_only_Institutions_GiniSim_median,
  AVG(IF(green_only=TRUE, CitingCountries_GiniSim, NULL)) as green_only_Countries_GiniSim_mean,
  ANY_VALUE(IF(green_only=TRUE, green_only_Countries_GiniSim_median, NULL)) as green_only_Countries_GiniSim_median,
  AVG(IF(green_only=TRUE, CitingSubregions_GiniSim, NULL)) as green_only_Subregions_GiniSim_mean,
  ANY_VALUE(IF(green_only=TRUE, green_only_Subregions_GiniSim_median, NULL)) as green_only_Subregions_GiniSim_median,
  AVG(IF(green_only=TRUE, CitingRegions_GiniSim, NULL)) as green_only_Regions_GiniSim_mean,
  ANY_VALUE(IF(green_only=TRUE, green_only_Regions_GiniSim_median, NULL)) as green_only_Regions_GiniSim_median,
  AVG(IF(green_only=TRUE, CitingFields_GiniSim, NULL)) as green_only_Fields_GiniSim_mean,
  ANY_VALUE(IF(green_only=TRUE, green_only_Fields_GiniSim_median, NULL)) as green_only_Fields_GiniSim_median,
  AVG(IF(green_only=TRUE, CitingInstitutions_Shannon, NULL)) as green_only_Institutions_Shannon_mean,
  ANY_VALUE(IF(green_only=TRUE, green_only_Institutions_Shannon_median, NULL)) as green_only_Institutions_Shannon_median,
  AVG(IF(green_only=TRUE, CitingCountries_Shannon, NULL)) as green_only_Countries_Shannon_mean,
  ANY_VALUE(IF(green_only=TRUE, green_only_Countries_Shannon_median, NULL)) as green_only_Countries_Shannon_median,
  AVG(IF(green_only=TRUE, CitingSubregions_Shannon, NULL)) as green_only_Subregions_Shannon_mean,
  ANY_VALUE(IF(green_only=TRUE, green_only_Subregions_Shannon_median, NULL)) as green_only_Subregions_Shannon_median,
  AVG(IF(green_only=TRUE, CitingRegions_Shannon, NULL)) as green_only_Regions_Shannon_mean,
  ANY_VALUE(IF(green_only=TRUE, green_only_Regions_Shannon_median, NULL)) as green_only_Regions_Shannon_median,
  AVG(IF(green_only=TRUE, CitingFields_Shannon, NULL)) as green_only_Fields_Shannon_mean,
  ANY_VALUE(IF(green_only=TRUE, green_only_Fields_Shannon_median, NULL)) as green_only_Fields_Shannon_median,
  #mean and median unique citing groups and diversity measures for hybrid
  AVG(IF(hybrid=TRUE, CitingInstitutions_count_uniq, NULL)) as hybrid_Institutions_uniq_mean,
  ANY_VALUE(IF(hybrid=TRUE, hybrid_Institutions_uniq_median, NULL)) as hybrid_Institutions_uniq_median,
  AVG(IF(hybrid=TRUE, CitingCountries_count_uniq, NULL)) as hybrid_Countries_uniq_mean,
  ANY_VALUE(IF(hybrid=TRUE, hybrid_Countries_uniq_median, NULL)) as hybrid_Countries_uniq_median,
  AVG(IF(hybrid=TRUE, CitingSubregions_count_uniq, NULL)) as hybrid_Subregions_uniq_mean,
  ANY_VALUE(IF(hybrid=TRUE, hybrid_Subregions_uniq_median, NULL)) as hybrid_Subregions_uniq_median,
  AVG(IF(hybrid=TRUE, CitingRegions_count_uniq, NULL)) as hybrid_Regions_uniq_mean,
  ANY_VALUE(IF(hybrid=TRUE, hybrid_Regions_uniq_median, NULL)) as hybrid_Regions_uniq_median,
  AVG(IF(hybrid=TRUE, CitingFields_count_uniq, NULL)) as hybrid_Fields_uniq_mean,
  ANY_VALUE(IF(hybrid=TRUE, hybrid_Fields_uniq_median, NULL)) as hybrid_Fields_uniq_median,
  AVG(IF(hybrid=TRUE, CitingInstitutions_GiniSim, NULL)) as hybrid_Institutions_GiniSim_mean,
  ANY_VALUE(IF(hybrid=TRUE, hybrid_Institutions_GiniSim_median, NULL)) as hybrid_Institutions_GiniSim_median,
  AVG(IF(hybrid=TRUE, CitingCountries_GiniSim, NULL)) as hybrid_Countries_GiniSim_mean,
  ANY_VALUE(IF(hybrid=TRUE, hybrid_Countries_GiniSim_median, NULL)) as hybrid_Countries_GiniSim_median,
  AVG(IF(hybrid=TRUE, CitingSubregions_GiniSim, NULL)) as hybrid_Subregions_GiniSim_mean,
  ANY_VALUE(IF(hybrid=TRUE, hybrid_Subregions_GiniSim_median, NULL)) as hybrid_Subregions_GiniSim_median,
  AVG(IF(hybrid=TRUE, CitingRegions_GiniSim, NULL)) as hybrid_Regions_GiniSim_mean,
  ANY_VALUE(IF(hybrid=TRUE, hybrid_Regions_GiniSim_median, NULL)) as hybrid_Regions_GiniSim_median,
  AVG(IF(hybrid=TRUE, CitingFields_GiniSim, NULL)) as hybrid_Fields_GiniSim_mean,
  ANY_VALUE(IF(hybrid=TRUE, hybrid_Fields_GiniSim_median, NULL)) as hybrid_Fields_GiniSim_median,
  AVG(IF(hybrid=TRUE, CitingInstitutions_Shannon, NULL)) as hybrid_Institutions_Shannon_mean,
  ANY_VALUE(IF(hybrid=TRUE, hybrid_Institutions_Shannon_median, NULL)) as hybrid_Institutions_Shannon_median,
  AVG(IF(hybrid=TRUE, CitingCountries_Shannon, NULL)) as hybrid_Countries_Shannon_mean,
  ANY_VALUE(IF(hybrid=TRUE, hybrid_Countries_Shannon_median, NULL)) as hybrid_Countries_Shannon_median,
  AVG(IF(hybrid=TRUE, CitingSubregions_Shannon, NULL)) as hybrid_Subregions_Shannon_mean,
  ANY_VALUE(IF(hybrid=TRUE, hybrid_Subregions_Shannon_median, NULL)) as hybrid_Subregions_Shannon_median,
  AVG(IF(hybrid=TRUE, CitingRegions_Shannon, NULL)) as hybrid_Regions_Shannon_mean,
  ANY_VALUE(IF(hybrid=TRUE, hybrid_Regions_Shannon_median, NULL)) as hybrid_Regions_Shannon_median,
  AVG(IF(hybrid=TRUE, CitingFields_Shannon, NULL)) as hybrid_Fields_Shannon_mean,
  ANY_VALUE(IF(hybrid=TRUE, hybrid_Fields_Shannon_median, NULL)) as hybrid_Fields_Shannon_median,
  #mean and median unique citing groups and diversity measures for bronze
  AVG(IF(bronze=TRUE, CitingInstitutions_count_uniq, NULL)) as bronze_Institutions_uniq_mean,
  ANY_VALUE(IF(bronze=TRUE, bronze_Institutions_uniq_median, NULL)) as bronze_Institutions_uniq_median,
  AVG(IF(bronze=TRUE, CitingCountries_count_uniq, NULL)) as bronze_Countries_uniq_mean,
  ANY_VALUE(IF(bronze=TRUE, bronze_Countries_uniq_median, NULL)) as bronze_Countries_uniq_median,
  AVG(IF(bronze=TRUE, CitingSubregions_count_uniq, NULL)) as bronze_Subregions_uniq_mean,
  ANY_VALUE(IF(bronze=TRUE, bronze_Subregions_uniq_median, NULL)) as bronze_Subregions_uniq_median,
  AVG(IF(bronze=TRUE, CitingRegions_count_uniq, NULL)) as bronze_Regions_uniq_mean,
  ANY_VALUE(IF(bronze=TRUE, bronze_Regions_uniq_median, NULL)) as bronze_Regions_uniq_median,
  AVG(IF(bronze=TRUE, CitingFields_count_uniq, NULL)) as bronze_Fields_uniq_mean,
  ANY_VALUE(IF(bronze=TRUE, bronze_Fields_uniq_median, NULL)) as bronze_Fields_uniq_median,
  AVG(IF(bronze=TRUE, CitingInstitutions_GiniSim, NULL)) as bronze_Institutions_GiniSim_mean,
  ANY_VALUE(IF(bronze=TRUE, bronze_Institutions_GiniSim_median, NULL)) as bronze_Institutions_GiniSim_median,
  AVG(IF(bronze=TRUE, CitingCountries_GiniSim, NULL)) as bronze_Countries_GiniSim_mean,
  ANY_VALUE(IF(bronze=TRUE, bronze_Countries_GiniSim_median, NULL)) as bronze_Countries_GiniSim_median,
  AVG(IF(bronze=TRUE, CitingSubregions_GiniSim, NULL)) as bronze_Subregions_GiniSim_mean,
  ANY_VALUE(IF(bronze=TRUE, bronze_Subregions_GiniSim_median, NULL)) as bronze_Subregions_GiniSim_median,
  AVG(IF(bronze=TRUE, CitingRegions_GiniSim, NULL)) as bronze_Regions_GiniSim_mean,
  ANY_VALUE(IF(bronze=TRUE, bronze_Regions_GiniSim_median, NULL)) as bronze_Regions_GiniSim_median,
  AVG(IF(bronze=TRUE, CitingFields_GiniSim, NULL)) as bronze_Fields_GiniSim_mean,
  ANY_VALUE(IF(bronze=TRUE, bronze_Fields_GiniSim_median, NULL)) as bronze_Fields_GiniSim_median,
  AVG(IF(bronze=TRUE, CitingInstitutions_Shannon, NULL)) as bronze_Institutions_Shannon_mean,
  ANY_VALUE(IF(bronze=TRUE, bronze_Institutions_Shannon_median, NULL)) as bronze_Institutions_Shannon_median,
  AVG(IF(bronze=TRUE, CitingCountries_Shannon, NULL)) as bronze_Countries_Shannon_mean,
  ANY_VALUE(IF(bronze=TRUE, bronze_Countries_Shannon_median, NULL)) as bronze_Countries_Shannon_median,
  AVG(IF(bronze=TRUE, CitingSubregions_Shannon, NULL)) as bronze_Subregions_Shannon_mean,
  ANY_VALUE(IF(bronze=TRUE, bronze_Subregions_Shannon_median, NULL)) as bronze_Subregions_Shannon_median,
  AVG(IF(bronze=TRUE, CitingRegions_Shannon, NULL)) as bronze_Regions_Shannon_mean,
  ANY_VALUE(IF(bronze=TRUE, bronze_Regions_Shannon_median, NULL)) as bronze_Regions_Shannon_median,
  AVG(IF(bronze=TRUE, CitingFields_Shannon, NULL)) as bronze_Fields_Shannon_mean,
  ANY_VALUE(IF(bronze=TRUE, bronze_Fields_Shannon_median, NULL)) as bronze_Fields_Shannon_median
FROM  DataTempAll
GROUP BY year
ORDER BY year ASC
