SELECT
  $__timeEpoch(EventProcessedUtcTime),
  temperature
FROM
  experimental
WHERE
  $__timeFilter(EventProcessedUtcTime)
ORDER BY
  EventProcessedUtcTime ASC