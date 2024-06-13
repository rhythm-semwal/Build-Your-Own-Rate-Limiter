from fastapi import FastAPI, Request, HTTPException
from RateLimitFactory import RateLimitFactory
from RateLimitingAlgorithms import RateLimitExceeded


app = FastAPI()

ip_address_to_algorithm_mapping = {}
PERMITTED_ALGORITHM = ['TokenBucket', 'FixedCounterWindow', 'SlidingWindow', 'SlidingWindowCounter']


@app.get("/limited")
def limited(request: Request):
    client = request.client.host
    algorithm = request.query_params.get("algorithm")

    if algorithm not in PERMITTED_ALGORITHM:
        raise HTTPException(
            status_code=400,
            detail="Bad Request. Please try again later."
        )

    try:
        if client not in ip_address_to_algorithm_mapping:
            ip_address_to_algorithm_mapping[client] = RateLimitFactory.get_instance(algorithm)
        if ip_address_to_algorithm_mapping[client].allow_request():
            return "This is a limited use API"
    except RateLimitExceeded as e:
        raise e


@app.get("/unlimited")
def unlimited():
    return "Unlimited! Let's Go!"

