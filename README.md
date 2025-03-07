# For Unit Testing---


### Run all performance tests:
`pytest tests/performance --benchmark-only`

### To see full performance reports, use:
`pytest tests/performance --benchmark-histogram`

`pytest`


### use this for locust
`locust`

##### Open Locust UI in your browser:
Go to: `http://localhost:8089`

#### To run Locust without the UI, use:
`locust --headless -u 100 -r 10 --run-time 2m`
