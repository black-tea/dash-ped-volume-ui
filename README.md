# ped-volume-map
 A Plotly Dash application to view pedestrian volume data and interact with the volume model

## Setup
1. Place mapbox access token in `.mapbox_token` file within root directory. This should contain the public access key, which you can get in your mapbox account settings.

## Deployment
### Switch debug in mode in Dockerfile

```dockerfile
ENV DASH_DEBUG_MODE True # False
```

### Local: Build and run

```sh
docker build -t dash . && docker run --rm -p 8050:8050 dash
```
