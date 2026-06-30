## Skripta za transformaciju kolekcije job_postings u job_postings_v2

Izvor: linkedin_jobs.job_postings + companies + job_metadata
Cilj: denormalizovana analitička kolekcija za HR upite

```js
db = db.getSiblingDB("linkedin_jobs");

db.job_postings.aggregate([
  {
    $lookup: {
      from: "companies",
      localField: "company_id",
      foreignField: "company_id",
      as: "company"
    }
  },
  {
    $unwind: {
      path: "$company",
      preserveNullAndEmptyArrays: true
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
    $unwind: {
      path: "$metadata",
      preserveNullAndEmptyArrays: true
    }
  },
  {
    $project: {
      _id: 0,

      job_id: 1,
      company_id: 1,

      title: 1,
      work_type: 1,
      formatted_work_type: 1,
      formatted_experience_level: 1,
      location: 1,

      company: {
        company_size: "$company.company_size",
        employee_count: "$company.employee_count"
      },

      salary: {
        normalized_salary: "$salary.normalized_salary",
        currency: "$salary.currency",
        pay_period: "$salary.pay_period",
        compensation_type: "$salary.compensation_type"
      },

      metrics: {
        views: "$metrics.views",
        applies: "$metrics.applies",
        conversion_rate: {
          $cond: [
            { $gt: ["$metrics.views", 0] },
            { $divide: ["$metrics.applies", "$metrics.views"] },
            null
          ]
        }
      },

      skills: "$metadata.skills",
      industries: "$metadata.industries",
      benefits: "$metadata.benefits",

      skill_count: {
        $size: {
          $ifNull: ["$metadata.skills", []]
        }
      },

      dates: {
        listed_time: "$dates.listed_time"
      }
    }
  },
  {
    $out: {
      db: "linkedin_jobs_v2",
      coll: "job_postings_v2"
    }
  }
], { allowDiskUse: true });
```
## Skripta za kreiranje V2 kolekcije industry_skill_stats_v2

Izvor: linkedin_jobs.job_metadata
Cilj: precomputed kolekcija za HR4

```js
db = db.getSiblingDB("linkedin_jobs");

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
                { $divide: ["$total_skill_mentions", { $size: "$job_ids" }] },
                3
              ]
            }
          }
        },
        { $match: { total_jobs: { $gte: 100 } } },
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
        { $match: { rank: { $lte: 3 } } },
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
        _id: "$industry_stats.industry",
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
                    $eq: [
                        "$$ts.industry",
                        "$industry_stats.industry"
                    ]
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
  },
  {
    $out: {
      db: "linkedin_jobs_v2",
      coll: "industry_skill_stats_v2"
    }
  }
], { allowDiskUse: true });
```

## Kod za kreiranje index-a za obe kolekcije

Nakon formiranja V2 kolekcija kreirani su indeksi nad atributima koji se najčešće koriste u filtriranju, grupisanju i sortiranju analitičkih upita.

```js
db.job_postings_v2.createIndex({ work_type: 1 });
db.job_postings_v2.createIndex({ "metrics.views": 1 });
db.job_postings_v2.createIndex({ "metrics.conversion_rate": 1 });
db.job_postings_v2.createIndex({ "company.company_size": 1 });
db.job_postings_v2.createIndex({ "company.employee_count": 1 });
db.job_postings_v2.createIndex({ "salary.normalized_salary": 1 });
db.job_postings_v2.createIndex({ "skills.skill_name": 1 });
db.job_postings_v2.createIndex({ "industries.industry_name": 1 });

db.industry_skill_stats_v2.createIndex({ distinct_skill_count: -1 });
db.industry_skill_stats_v2.createIndex({ avg_skills_per_job: -1 });
```