# V1 logička šema baze podataka

V1 šema je organizovana kroz tri MongoDB kolekcije:

- `job_postings`
- `companies`
- `job_metadata`

Cilj ove podele je da se izbegne jedan prevelik dokument koji sadrži sve podatke, jer različiti upiti koriste različite grupe atributa.

## Kolekcija `job_postings`

```js
{
  job_id: Number,
  company_id: Number,

  title: String,
  description: String,

  formatted_work_type: String,
  work_type: String,
  formatted_experience_level: String,

  location: String,
  zip_code: String,
  fips: String,

  remote_allowed: Boolean,
  sponsored: Boolean,

  salary: {
    min_salary: Number,
    med_salary: Number,
    max_salary: Number,
    normalized_salary: Number,
    currency: String,
    pay_period: String,
    compensation_type: String
  },

  metrics: {
    views: Number,
    applies: Number
  },

  dates: {
    listed_time: Date,
    original_listed_time: Date,
    expiry: Date,
    closed_time: Date
  }
}

## Kolekcija `companies`

```js
{
  company_id: Number,
  name: String,

  company_size: String,

  country: String,
  state: String,
  city: String,
  address: String,

  employee_count: Number,
  follower_count: Number,

  specialities: [String]
}

## Kolekcija `job_metadata`
```js
{
  job_id: Number,

  skills: [
    {
      skill_abr: String,
      skill_name: String
    }
  ],

  industries: [
    {
      industry_id: Number,
      industry_name: String
    }
  ],

  benefits: [
    {
      type: String,
      inferred: Boolean
    }
  ]
}

Veze izmedju kolekcija
job_postings.company_id → companies.company_id
job_postings.job_id → job_metadata.job_id