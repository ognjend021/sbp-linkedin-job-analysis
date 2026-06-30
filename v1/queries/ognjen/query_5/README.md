## Kako broj zaposlenih u kompaniji utiče na visinu ponuđene plate i uspešnost oglasa?
```js
db.job_postings.aggregate([
  {
    $match: {
      company_id: { $ne: null },
      "metrics.views": { $gt: 0 },
      "metrics.applies": { $ne: null },
      "salary.normalized_salary": { $ne: null }
    }
  },
  {
    $lookup: {
      from: "companies",
      localField: "company_id",
      foreignField: "company_id",
      as: "company"
    }
  },
  { $unwind: "$company" },
  {
    $match: {
      "company.employee_count": { $ne: null, $gt: 0 }
    }
  },
  {
    $project: {
      company_id: 1,
      employee_count: "$company.employee_count",
      normalized_salary: "$salary.normalized_salary",
      views: "$metrics.views",
      applies: "$metrics.applies",
      conversion_rate: {
        $divide: ["$metrics.applies", "$metrics.views"]
      }
    }
  },
  {
    $bucket: {
      groupBy: "$employee_count",
      boundaries: [1, 50, 200, 1000, 5000, 10000, 50000, 1000000],
      output: {
        total_jobs: { $sum: 1 },
        companies_set: { $addToSet: "$company_id" },
        avg_salary: { $avg: "$normalized_salary" },
        avg_views: { $avg: "$views" },
        avg_applies: { $avg: "$applies" },
        avg_conversion_rate: { $avg: "$conversion_rate" }
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
## Rezultat upita
```js
[
  {
    total_jobs: 1757,
    employee_bucket: '1-49',
    unique_companies: 1325,
    avg_salary: 105401.505,
    avg_views: 67.832,
    avg_applies: 13.568,
    avg_conversion_rate: 0.19
  },
  {
    total_jobs: 1538,
    employee_bucket: '50-199',
    unique_companies: 909,
    avg_salary: 295981.93,
    avg_views: 61.395,
    avg_applies: 12.651,
    avg_conversion_rate: 0.189
  },
  {
    total_jobs: 1626,
    employee_bucket: '200-999',
    unique_companies: 829,
    avg_salary: 171168.846,
    avg_views: 64.518,
    avg_applies: 11.989,
    avg_conversion_rate: 0.18
  },
  {
    total_jobs: 1540,
    employee_bucket: '1,000-4,999',
    unique_companies: 705,
    avg_salary: 247331.737,
    avg_views: 63.569,
    avg_applies: 10.922,
    avg_conversion_rate: 0.174
  },
  {
    total_jobs: 497,
    employee_bucket: '5,000-9,999',
    unique_companies: 223,
    avg_salary: 104435.586,
    avg_views: 64.024,
    avg_applies: 7.871,
    avg_conversion_rate: 0.155
  },
  {
    total_jobs: 1144,
    employee_bucket: '10,000-49,999',
    unique_companies: 316,
    avg_salary: 109318.766,
    avg_views: 55.744,
    avg_applies: 11.435,
    avg_conversion_rate: 0.166
  },
  {
    total_jobs: 527,
    employee_bucket: '50,000+',
    unique_companies: 111,
    avg_salary: 274342.571,
    avg_views: 72.793,
    avg_applies: 8.044,
    avg_conversion_rate: 0.14
  }
]
```