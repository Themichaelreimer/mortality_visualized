# mortality_visualized

# Goal:
This project aims to provide data visualizations and fun/useful stats about diseases and general mortality.

## Technology Stack:
Backend: Python 3.7 <=; Django 3; mysql server
Frontend: Vue.js

# Setup
TODO: Flesh this out more

- Install python3, pip, django

- Install mysql, set up user. Check mortality/settings.py for credentials you should use.

# Project Areas
- `covid` app, which is focused on covid-19 related visualizations and daily case-rates/death rates
- `disease` app, which is focused on disease incidence/prevalence and mortality. Ideally this could expand out into signs/symptoms, treatments, etc, but I doubt the data exists in a nice and free way
- `life_tables` app, which compares various metrics of all-cause mortality across age/sex/location
- Disease Graph, showing common symptoms, treatments, differential diagnosises, etc

# TODO:
- Add deaths in covid time series data
- Make `disease` app if hmd looks general enough; otherwise `hmd` app (`hmd` means "Human Mortality Database")
- Better set up instructions, in case I collab with someone who isn't a soft. engineer

## Data Sources:
Johns Hopkins: Covid time series data

Human Mortality Database: death statistics by ICD code
