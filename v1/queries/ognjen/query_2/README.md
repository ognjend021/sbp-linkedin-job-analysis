## Koje veštine se najčešće pojavljuju u uspešnim oglasima, pri čemu se uspešnim oglasom smatra oglas sa najmanje 100 pregleda i stopom konverzije prijava u odnosu na preglede od najmanje 30%?

```js
db.job_postings.aggregate([
  {
    $match: {
      "metrics.views": { $gte: 100 },
      "metrics.applies": { $ne: null }
    }
  },
  {
    $project: {
      job_id: 1,
      conversion_rate: {
        $divide: ["$metrics.applies", "$metrics.views"]
      }
    }
  },
  {
    $match: {
      conversion_rate: { $gte: 0.30 }
    }
  },
  {
    $lookup: {
      from: "job_metadata",
      localField: "job_id",
      foreignField: "job_id",
      as: "metadata"
    }
  },
  {
    $unwind: "$metadata"
  },
  {
    $unwind: "$metadata.skills"
  },
  {
    $group: {
      _id: "$metadata.skills.skill_name",
      count: { $sum: 1 },
      avg_conversion_rate: { $avg: "$conversion_rate" }
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
  {
    $limit: 20
  }
])
```
## Rezultat upita
```js
[
  { count: 486, skill_name: 'Information Technology', avg_conversion_rate: 0.401 },
  { count: 206, skill_name: 'Engineering', avg_conversion_rate: 0.401 },
  { count: 73, skill_name: 'Analyst', avg_conversion_rate: 0.403 },
  { count: 53, skill_name: 'Sales', avg_conversion_rate: 0.363 },
  { count: 49, skill_name: 'Marketing', avg_conversion_rate: 0.372 },
  { count: 38, skill_name: 'Administrative', avg_conversion_rate: 0.38 },
  { count: 31, skill_name: 'Human Resources', avg_conversion_rate: 0.389 },
  { count: 29, skill_name: 'Business Development', avg_conversion_rate: 0.362 },
  { count: 28, skill_name: 'Project Management', avg_conversion_rate: 0.384 },
  { count: 28, skill_name: 'Finance', avg_conversion_rate: 0.372 },
  { count: 27, skill_name: 'Other', avg_conversion_rate: 0.402 },
  { count: 27, skill_name: 'Consulting', avg_conversion_rate: 0.37 },
  { count: 21, skill_name: 'Design', avg_conversion_rate: 0.376 },
  { count: 20, skill_name: 'Product Management', avg_conversion_rate: 0.36 },
  { count: 17, skill_name: 'Customer Service', avg_conversion_rate: 0.448 },
  { count: 17, skill_name: 'Writing/Editing', avg_conversion_rate: 0.378 },
  { count: 17, skill_name: 'Accounting/Auditing', avg_conversion_rate: 0.361 },
  { count: 16, skill_name: 'Management', avg_conversion_rate: 0.379 },
  { count: 15, skill_name: 'Art/Creative', avg_conversion_rate: 0.369 },
  { count: 11, skill_name: 'Strategy/Planning', avg_conversion_rate: 0.377}
]

```