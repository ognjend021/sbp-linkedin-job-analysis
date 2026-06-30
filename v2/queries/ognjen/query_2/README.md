## (optimizovano) Koje veštine se najčešće pojavljuju u najuspešnijim oglasima, pri čemu se uspešnost meri stopom konverzije prijava u odnosu na broj pregleda, uz najmanje 100 pregleda oglasa?
```js
db.job_postings_v2.aggregate([
  {
    $match: {
      "metrics.views": { $gte: 100 },
      "metrics.conversion_rate": { $gte: 0.30 }
    }
  },
  {
    $unwind: "$skills"
  },
  {
    $group: {
      _id: "$skills.skill_name",
      count: { $sum: 1 },
      avg_conversion_rate: { $avg: "$metrics.conversion_rate" }
    }
  },
  {
    $project: {
      _id: 0,
      skill_name: "$_id",
      count: 1,
      avg_conversion_rate: { $round: ["$avg_conversion_rate", 3] }
    }
  },
  {
    $sort: {
      count: -1,
      avg_conversion_rate: -1
    }
  },
  { $limit: 20 }
])
```