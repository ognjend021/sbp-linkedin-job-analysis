## Kako kategorija veličine kompanije utiče na uspešnost oglasa, posmatrano kroz prosečan broj pregleda, prosečan broj prijava i stopu konverzije prijava u odnosu na broj pregleda?
```js
db.job_metadata.aggregate([
  { $unwind: "$industries" },
  {
    $match: {
      "industries.industry_name": { $ne: "" }
    }
  },
  { $unwind: "$skills" },
  {
    $match: {
      "skills.skill_name": { $ne: "" }
    }
  },
  {
    $facet: {
      industry_stats: [
        {
          $group: {
            _id: "$industries.industry_name",
            job_ids: { $addToSet: "$job_id" },
            distinct_skills: { $addToSet: "$skills.skill_name" },
            total_skill_mentions: { $sum: 1 }
          }
        },
        {
          $project: {
            _id: 0,
            industry: "$_id",
            total_jobs: { $size: "$job_ids" },
            distinct_skill_count: { $size: "$distinct_skills" },
            avg_skills_per_job: {
              $round: [
                {
                  $divide: [
                    "$total_skill_mentions",
                    { $size: "$job_ids" }
                  ]
                },
                3
              ]
            }
          }
        },
        {
          $match: {
            total_jobs: { $gte: 100 }
          }
        },
        {
          $sort: {
            distinct_skill_count: -1,
            avg_skills_per_job: -1,
            total_jobs: -1
          }
        },
        { $limit: 10 }
      ],

      top_skills: [
        {
          $group: {
            _id: {
              industry: "$industries.industry_name",
              skill: "$skills.skill_name"
            },
            skill_count: { $sum: 1 }
          }
        },
        {
          $setWindowFields: {
            partitionBy: "$_id.industry",
            sortBy: { skill_count: -1 },
            output: {
              rank: { $rank: {} }
            }
          }
        },
        {
          $match: {
            rank: { $lte: 3 }
          }
        },
        {
          $project: {
            _id: 0,
            industry: "$_id.industry",
            rank: 1,
            skill: "$_id.skill",
            skill_count: 1
          }
        },
        {
          $group: {
            _id: "$industry",
            top_skills: {
              $push: {
                rank: "$rank",
                skill: "$skill",
                skill_count: "$skill_count"
              }
            }
          }
        },
        {
          $project: {
            _id: 0,
            industry: "$_id",
            top_skills: 1
          }
        }
      ]
    }
  },
  { $unwind: "$industry_stats" },
  {
    $project: {
      _id: 0,
      industry: "$industry_stats.industry",
      total_jobs: "$industry_stats.total_jobs",
      distinct_skill_count: "$industry_stats.distinct_skill_count",
      avg_skills_per_job: "$industry_stats.avg_skills_per_job",
      top_skills: {
        $let: {
          vars: {
            matched: {
              $first: {
                $filter: {
                  input: "$top_skills",
                  as: "ts",
                  cond: {
                    $eq: ["$$ts.industry", "$industry_stats.industry"]
                  }
                }
              }
            }
          },
          in: "$$matched.top_skills"
        }
      }
    }
  },
  {
    $sort: {
      distinct_skill_count: -1,
      avg_skills_per_job: -1,
      total_jobs: -1
    }
  }
])
```
## Rezultat upita
```js
[
  {
    industry: 'Advertising Services',
    total_jobs: 1801,
    distinct_skill_count: 35,
    avg_skills_per_job: 2.261,
    top_skills: [
      { rank: 1, skill: 'Marketing', skill_count: 844 },
      { rank: 2, skill: 'Sales', skill_count: 560 },
      { rank: 3, skill: 'Customer Service', skill_count: 454 }
    ]
  },
  {
    industry: 'Biotechnology Research',
    total_jobs: 1943,
    distinct_skill_count: 35,
    avg_skills_per_job: 2.045,
    top_skills: [
      { rank: 1, skill: 'Research', skill_count: 411 },
      { rank: 2, skill: 'Information Technology', skill_count: 355 },
      { rank: 3, skill: 'Sales', skill_count: 322 }
    ]
  },
  {
    industry: 'Retail Apparel and Fashion',
    total_jobs: 1321,
    distinct_skill_count: 35,
    avg_skills_per_job: 1.958,
    top_skills: [
      { rank: 1, skill: 'Sales', skill_count: 802 },
      { rank: 2, skill: 'Business Development', skill_count: 643 },
      { rank: 3, skill: 'Management', skill_count: 160 }
    ]
  },
  {
    industry: 'Consumer Services',
    total_jobs: 814,
    distinct_skill_count: 35,
    avg_skills_per_job: 1.957,
    top_skills: [
      { rank: 1, skill: 'Sales', skill_count: 235 },
      { rank: 2, skill: 'Management', skill_count: 211 },
      { rank: 3, skill: 'Manufacturing', skill_count: 151 }
    ]
  },
  {
    industry: 'Pharmaceutical Manufacturing',
    total_jobs: 2397,
    distinct_skill_count: 35,
    avg_skills_per_job: 1.94,
    top_skills: [
      { rank: 1, skill: 'Information Technology', skill_count: 408 },
      { rank: 2, skill: 'Sales', skill_count: 359 },
      { rank: 3, skill: 'Research', skill_count: 355 }
    ]
  },
  {
    industry: 'Motor Vehicle Manufacturing',
    total_jobs: 1919,
    distinct_skill_count: 35,
    avg_skills_per_job: 1.921,
    top_skills: [
      { rank: 1, skill: 'Manufacturing', skill_count: 631 },
      { rank: 2, skill: 'Management', skill_count: 522 },
      { rank: 3, skill: 'Sales', skill_count: 466 }
    ]
  },
  {
    industry: 'Software Development',
    total_jobs: 4779,
    distinct_skill_count: 35,
    avg_skills_per_job: 1.894,
    top_skills: [
      { rank: 1, skill: 'Information Technology', skill_count: 2145 },
      { rank: 2, skill: 'Engineering', skill_count: 1394 },
      { rank: 3, skill: 'Sales', skill_count: 930 }
    ]
  },
  {
    industry: 'Manufacturing',
    total_jobs: 3545,
    distinct_skill_count: 35,
    avg_skills_per_job: 1.894,
    top_skills: [
      { rank: 1, skill: 'Manufacturing', skill_count: 970 },
      { rank: 2, skill: 'Sales', skill_count: 848 },
      { rank: 3, skill: 'Management', skill_count: 741 }
    ]
  },
  {
    industry: 'Food and Beverage Services',
    total_jobs: 1842,
    distinct_skill_count: 35,
    avg_skills_per_job: 1.894,
    top_skills: [
      { rank: 1, skill: 'Management', skill_count: 781 },
      { rank: 2, skill: 'Manufacturing', skill_count: 707 },
      { rank: 3, skill: 'Sales', skill_count: 428 }
    ]
  },
  {
    industry: 'Construction',
    total_jobs: 3271,
    distinct_skill_count: 35,
    avg_skills_per_job: 1.871,
    top_skills: [
      { rank: 1, skill: 'Management', skill_count: 1077 },
      { rank: 2, skill: 'Manufacturing', skill_count: 872 },
      { rank: 3, skill: 'Project Management', skill_count: 621 }
    ]
  }
]
```