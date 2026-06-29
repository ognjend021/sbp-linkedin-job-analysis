## Kako kategorija veličine kompanije utiče na uspešnost oglasa, posmatrano kroz prosečan broj pregleda, prosečan broj prijava i stopu konverzije prijava u odnosu na broj pregleda?
```js
db.job_postings.aggregate([
  {
    $match: {
      "metrics.views": { $gt: 0 },
      "metrics.applies": { $ne: null },
      company_id: { $ne: null }
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
  {
    $unwind: "$company"
  },
  {
    $match: {
      "company.company_size": { $ne: null }
    }
  },
  {
    $project: {
      company_size: "$company.company_size",
      views: "$metrics.views",
      applies: "$metrics.applies",
      conversion_rate: {
        $divide: ["$metrics.applies", "$metrics.views"]
      }
    }
  },
  {
    $group: {
      _id: "$company_size",
      total_jobs: { $sum: 1 },
      avg_views: { $avg: "$views" },
      avg_applies: { $avg: "$applies" },
      avg_conversion_rate: { $avg: "$conversion_rate" }
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
## Rezultat upita
Polje company_size predstavlja kategoriju veličine kompanije preuzetu iz originalnog LinkedIn dataseta. Vrednosti su označene kategorijama od 1 do 7, pri čemu veći broj predstavlja veću kategoriju kompanije. Poznato je da kategorija 1 ima u proseku 50 zaposlenih, kategorija 2 ima u proseku 125 zaposlenih , kategorija 3: 341, kategorija 4: 789, kategorija 5: 1808, kategorija 6: 4767, kategorija 7: 23426
```js
[
  {
    total_jobs: 2717,
    company_size: 1,
    avg_views: 68.368,
    avg_applies: 13.277,
    avg_conversion_rate: 0.188
  },
  {
    total_jobs: 3597,
    company_size: 2,
    avg_views: 59.698,
    avg_applies: 12.89,
    avg_conversion_rate: 0.194
  },
  {
    total_jobs: 2413,
    company_size: 3,
    avg_views: 61.246,
    avg_applies: 11.649,
    avg_conversion_rate: 0.181
  },
  {
    total_jobs: 2000,
    company_size: 4,
    avg_views: 54.913,
    avg_applies: 11.35,
    avg_conversion_rate: 0.184
  },
  {
    total_jobs: 4126,
    company_size: 5,
    avg_views: 50.517,
    avg_applies: 9.951,
    avg_conversion_rate: 0.173
  },
  {
    total_jobs: 1548,
    company_size: 6,
    avg_views: 52.152,
    avg_applies: 7.891,
    avg_conversion_rate: 0.158
  },
  {
    total_jobs: 4970,
    company_size: 7,
    avg_views: 44.16,
    avg_applies: 6.805,
    avg_conversion_rate: 0.151
  }
]
```