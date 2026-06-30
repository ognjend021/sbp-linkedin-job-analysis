## (optimizovano) Kako broj zaposlenih u kompaniji utiče na visinu ponuđene plate i uspešnost oglasa?

```js
db.job_postings_v2.aggregate([
  {
    $match: {
      "company.employee_count": { $gt: 0 },
      "salary.normalized_salary": { $ne: null },
      "metrics.views": { $gt: 0 },
      "metrics.applies": { $ne: null }
    }
  },
  {
    $bucket: {
      groupBy: "$company.employee_count",
      boundaries: [1, 50, 200, 1000, 5000, 10000, 50000, 1000000],
      output: {
        total_jobs: { $sum: 1 },
        companies_set: { $addToSet: "$company_id" },
        avg_salary: { $avg: "$salary.normalized_salary" },
        avg_views: { $avg: "$metrics.views" },
        avg_applies: { $avg: "$metrics.applies" },
        avg_conversion_rate: { $avg: "$metrics.conversion_rate" }
      }
    }
  },
  {
    $project: {
      _id: 0,
      employee_bucket: {
        $switch: {
          branches: [
            { case: { $eq: ["$_id", 1] }, then: "1-49" },
            { case: { $eq: ["$_id", 50] }, then: "50-199" },
            { case: { $eq: ["$_id", 200] }, then: "200-999" },
            { case: { $eq: ["$_id", 1000] }, then: "1,000-4,999" },
            { case: { $eq: ["$_id", 5000] }, then: "5,000-9,999" },
            { case: { $eq: ["$_id", 10000] }, then: "10,000-49,999" },
            { case: { $eq: ["$_id", 50000] }, then: "50,000+" }
          ],
          default: "other"
        }
      },
      total_jobs: 1,
      unique_companies: { $size: "$companies_set" },
      avg_salary: { $round: ["$avg_salary", 3] },
      avg_views: { $round: ["$avg_views", 3] },
      avg_applies: { $round: ["$avg_applies", 3] },
      avg_conversion_rate: { $round: ["$avg_conversion_rate", 3] }
    }
  }
])
```