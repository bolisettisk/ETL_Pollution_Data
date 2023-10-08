SELECT `Date`, `Time`, `Time Offset`,site.SiteID, site.Location, NOx
FROM site, (SELECT * FROM reading
WHERE YEAR(Date) = 2019
ORDER BY NOx DESC
LIMIT 1) AS reading_19
WHERE site.siteid = reading_19.siteid;