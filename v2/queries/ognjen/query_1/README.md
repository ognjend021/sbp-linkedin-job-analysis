## (optimizovano) Da li različiti tipovi rada (Full-time, Part-time, Contract…) ostvaruju različitu efikasnost oglasa, posmatrano kroz prosečan broj pregleda, prosečan broj prijava i stopu konverzije prijava u odnosu na preglede?
```js
db.job_postings_v2.aggregate([
  {
    $match: {
      work_type: { $ne: "" },
      "metrics.views": { $gt: 0 },
      "metrics.applies": { $ne: null }
    }
  },
  {
    $group: {
      _id: "$work_type",
      total_jobs: { $sum: 1 },
      avg_views: { $avg: "$metrics.views" },
      avg_applies: { $avg: "$metrics.applies" },
      avg_conversion_rate: { $avg: "$metrics.conversion_rate" }
    }
  },
  {
    $project: {
      _id: 0,
      work_type: "$_id",
      total_jobs: 1,
      avg_views: { $round: ["$avg_views", 3] },
      avg_applies: { $round: ["$avg_applies", 3] },
      avg_conversion_rate: { $round: ["$avg_conversion_rate", 3] }
    }
  },
  {
    $sort: {
      avg_conversion_rate: -1
    }
  }
])
```