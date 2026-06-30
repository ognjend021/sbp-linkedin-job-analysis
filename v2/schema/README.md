# V2 logička šema baze podataka

Druga verzija šeme baze podataka nastala je restrukturiranjem inicijalne šeme sa ciljem optimizacije analitičkih upita. Tokom analize V1 uočeno je da najveći broj sporih upita koristi operacije `$lookup` nad kolekcijama `companies` i `job_metadata`, što je značajno povećavalo vreme izvršavanja.

Zbog toga je u V2 primenjen **šablon proširene reference (Extended Reference Pattern)**, pri čemu su podaci koji se često koriste zajedno objedinjeni u jednu kolekciju. Takođe su primenjeni elementi **šablona aproksimacije (Approximation Pattern)** kroz unapred izračunata polja koja se često koriste u analitičkim upitima.

V2 šema sastoji se iz dve kolekcije:

- `job_postings_v2`
- `industry_skill_stats_v2`

---

# Kolekcija `job_postings_v2`

Kolekcija `job_postings_v2` predstavlja denormalizovanu verziju kolekcije `job_postings`. Podaci iz kolekcija `companies` i `job_metadata` ugrađeni su direktno u dokument kako bi se eliminisala potreba za čestim `$lookup` operacijama.

Pored toga, unapred je izračunata stopa konverzije prijava u odnosu na broj pregleda (`conversion_rate`) i broj veština (`skill_count`), čime se dodatno ubrzavaju analitički upiti.

```js
{
  job_id: Number,
  company_id: Number,

  title: String,

  work_type: String,
  formatted_work_type: String,
  formatted_experience_level: String,

  location: String,

  company: {
    company_size: Number,
    employee_count: Number
  },

  salary: {
    normalized_salary: Number,
    currency: String,
    pay_period: String,
    compensation_type: String
  },

  metrics: {
    views: Number,
    applies: Number,
    conversion_rate: Number
  },

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
  ],

  skill_count: Number,

  dates: {
    listed_time: Date
  }
}
```

## Izvor podataka

Kolekcija je formirana objedinjavanjem podataka iz:

- `job_postings`
- `companies`
- `job_metadata`

pri čemu su korišćene agregacione operacije `$lookup`, `$project` i `$out`.

---

# Kolekcija `industry_skill_stats_v2`

Kolekcija `industry_skill_stats_v2` predstavlja unapred agregirane statistike po industrijama i namenjena je analitičkim upitima koji ispituju zastupljenost veština u različitim industrijama.

Za svaku industriju čuvaju se:

- ukupan broj oglasa,
- broj različitih veština,
- prosečan broj veština po oglasu,
- tri najzastupljenije veštine.

```js
{
  industry: String,

  total_jobs: Number,

  distinct_skill_count: Number,

  avg_skills_per_job: Number,

  top_skills: [
    {
      rank: Number,
      skill: String,
      skill_count: Number
    }
  ]
}
```

## Izvor podataka

Kolekcija je formirana agregacijom podataka iz kolekcije `job_metadata` korišćenjem operatora:

- `$group`
- `$facet`
- `$setWindowFields`
- `$project`
- `$out`

---

# Razlike u odnosu na V1

U odnosu na inicijalnu šemu izvršene su sledeće izmene:

- denormalizovani su podaci o kompaniji (`company_size`, `employee_count`);
- denormalizovane su informacije o veštinama, industrijama i pogodnostima oglasa;
- unapred je izračunata stopa konverzije (`conversion_rate`);
- dodat je atribut `skill_count`;
- kreirana je posebna kolekcija sa unapred agregiranim statistikama po industrijama (`industry_skill_stats_v2`);
- eliminisana je potreba za većinom `$lookup` operacija tokom izvršavanja analitičkih upita.

Ovakva organizacija omogućava znatno brže izvršavanje kompleksnih analitičkih upita u odnosu na V1 šemu.