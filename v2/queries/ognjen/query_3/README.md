## (optimizovano) Kako kategorija veličine kompanije utiče na uspešnost oglasa, posmatrano kroz prosečan broj pregleda, prosečan broj prijava i stopu konverzije prijava u odnosu na broj pregleda?

```js
db.job_postings_v2.aggregate([
  {
    $match: {
      "metrics.views": { $gt: 0 },
      "metrics.applies": { $ne: null },
      "company.company_size": { $ne: null }
    }
  },
  {
    $group: {
      _id: "$company.company_size",
      total_jobs: { $sum: 1 },
      avg_views: { $avg: "$metrics.views" },
      avg_applies: { $avg: "$metrics.applies" },
      avg_conversion_rate: { $avg: "$metrics.conversion_rate" }
    }
  },
  {
    $project: {
      _id: 0,
      company_size: "$_id",
      total_jobs: 1,
      avg_views: { $round: ["$avg_views", 3] },
      avg_applies: { $round: ["$avg_applies", 3] },
      avg_conversion_rate: { $round: ["$avg_conversion_rate", 3] }
    }
  },
  {
    $sort: {
      company_size: 1
    }
  }
])
```