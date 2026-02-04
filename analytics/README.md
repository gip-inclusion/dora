# DORA - Analytics

### Getting started

With [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed:
```bash
make venv
```

Then:
```bash
dbt deps
dbt debug
dbt seed
dbt run
dbt test
```


### Quality

```bash
make fix
make quality
```

### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
