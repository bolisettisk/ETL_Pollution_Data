select site.SiteID, site.Location, `Mean_PM2.5`, `Mean_VPM2.5`
from (
select SiteID, avg(`PM2.5`) as `Mean_PM2.5`, avg(`VPM2.5`) as `Mean_VPM2.5`
from Reading
where year(Date) = 2019 and Time between addtime("08:00:00", "-00:15:00") and addtime("08:00:00", "00:15:00")
group by SiteID) as `Mean-with-nulls`, site
where ((`Mean_PM2.5`is not null) or (`Mean_VPM2.5` is not null)) and `Mean-with-nulls`.siteid = site.SiteID;




