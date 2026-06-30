## (optimizovano) Koje industrije zahtevaju najraznovrsniji skup veština i koje su njihove tri najzastupljenije veštine?

```js
db.industry_skill_stats_v2.find().sort({
  distinct_skill_count: -1,
  avg_skills_per_job: -1,
  total_jobs: -1
})
```