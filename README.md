# BIOGRID Database Uploading Project

This was a one week internship project where the goal was to upload a BIOGRID database into neo4j. 

The database used was [Ubiquitin-Proteasome System](https://thebiogrid.org/project/1/ubiquitin-proteasome-system.html). I only uploaded the genes and their interactions. 

## setup

I use miniconda as my package manager, you can install everything using

```bash
conda env create -f environment.yml
conda activate ups-visual
source setup.sh
```

In order to acheive full functionality, create a .env file and add

```yaml
USERNAME=YOUR_NEO_USERNAME_HERE
INSTANCE_PASSWORD=YOUR_NEO_PASSWORD_HERE
```

To run

```shell
python main.py
```