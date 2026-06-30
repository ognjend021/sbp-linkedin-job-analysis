## Da li različiti tipovi rada (Full-time, Part-time, Contract…) ostvaruju različitu efikasnost oglasa, posmatrano kroz prosečan broj pregleda, prosečan broj prijava i stopu konverzije prijava u odnosu na preglede?
```js
db.job_postings.aggregate([
  {
    $match: {
      work_type: { $ne: "" },
      "metrics.views": { $gt: 0 },
      "metrics.applies": { $ne: null }
    }
  },
  {
    $project: {
      work_type: 1,
      views: "$metrics.views",
      applies: "$metrics.applies",
      conversion_rate: {
        $divide: ["$metrics.applies", "$metrics.views"]
      }
    }
  },
  {
    $group: {
      _id: "$work_type",
      total_jobs: { $sum: 1 },
      avg_views: { $avg: "$views" },
      avg_applies: { $avg: "$applies" },
      avg_conversion_rate: { $avg: "$conversion_rate" }
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
## Rezultat upita
```js
[
  {
    total_jobs: 364,
    work_type: 'INTERNSHIP',
    avg_views: 53.047,
    avg_applies: 12.753,
    avg_conversion_rate: 0.204
  },
  {
    total_jobs: 4622,
    work_type: 'CONTRACT',
    avg_views: 70.32,
    avg_applies: 17.705,
    avg_conversion_rate: 0.191
  },
  {
    total_jobs: 56,
    work_type: 'OTHER',
    avg_views: 56.661,
    avg_applies: 13.661,
    avg_conversion_rate: 0.18
  },
  {
    total_jobs: 674,
    work_type: 'PART_TIME',
    avg_views: 55.702,
    avg_applies: 9.004,
    avg_conversion_rate: 0.175
  },
  {
    total_jobs: 134,
    work_type: 'TEMPORARY',
    avg_views: 59.858,
    avg_applies: 12.366,
    avg_conversion_rate: 0.172
  },
  {
    total_jobs: 17438,
    work_type: 'FULL_TIME',
    avg_views: 51.658,
    avg_applies: 8.706,
    avg_conversion_rate: 0.172
  },
  {
    total_jobs: 31,
    work_type: 'VOLUNTEER',
    avg_views: 52.613,
    avg_applies: 7.097,
    avg_conversion_rate: 0.12
  }
]
```