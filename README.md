# AirSource: Air Quality Monitoring and Source Attribution

Built for the Neural Storm Hackathon.

AirSource is a single-page dashboard that shows air quality readings from sensor stations and estimates where the pollution is most likely coming from.

## Features
- Live AQI from PM2.5, plus PM10, NO2, SO2, CO and ozone readings
- Source attribution: vehicles, industry and coal, biomass burning, dust, secondary haze
- Scenario presets (rush hour, crop burning, factory plume, dusty day)
- Live feed simulation and a 24-hour PM2.5 trend chart
- Health advice that changes with the AQI

## How attribution works
Each pollutant is a fingerprint. NO2 and CO at rush hour point to vehicles, SO2 points to coal and industry, a high PM2.5/PM10 ratio with CO points to burning, a low ratio points to dust, and ozone points to secondary pollution. Every source gets a rule-based score, and the scores are converted to percentage shares.

## Run it
Open `index.html` in any browser. No install or build step.

## Roadmap
- Real data from OpenAQ or CPCB APIs
- Wind direction and a map for upwind source tracing
- Machine learning source classifier or PMF receptor model

## Note
Demo data is simulated.
