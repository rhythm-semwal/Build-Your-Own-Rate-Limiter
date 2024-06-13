# Build-Your-Own-Rate-Limiter

A rate limiter restricts the intended or unintended excessive usage of a system by regulating the number of requests made to/from it by discarding the surplus ones.

A rate limiting strategy can make your API more reliable, when:

1. A user is responsible for a spike in traffic, and you need to stay up for everyone else.
2. A user is accidentally sending you a lot of requests.
3. A bad actor is trying to overwhelm your servers.
4. A user is sending you a lot of lower-priority requests, and you want to make sure that it doesn’t affect your high-priority traffic.
5. Your service is degraded, and as a result you can’t handle your regular traffic load and need to drop low-priority requests.


There are 6 common approaches to rate limiting:

1. Token bucket - tokens are added to a ‘bucket’ at a fixed rate. The bucket has a fixed capacity. When a request is made it will only be accepted if there are enough tokens in the bucket. Tokens are removed from the bucket when a request is accepted.
2. Leaky bucket (as a meter) - This is equivalent to the token bucket, but implemented in a different way - a mirror image.
3. Leaky bucket (as a queue) - The bucket behaves like a FIFO queue with a limited capacity, if there is space in the bucket the request is accepted.
4. Fixed window counter - record the number of requests from a sender occurring in the rate limit’s fixed time interval, if it exceeds the limit the request is rejected.
5. Sliding window log - Store a timestamp for each request in a sorted set, when the size of the set trimmed to the window exceeds the limit, requests are rejected.
6. Sliding window counter - similar to the fixed window, but each request is timestamped and the window slides.


Setting Up the Application
Clone the Repository:

Begin by cloning the repository using git. If you don't have git installed, you can download it from https://git-scm.com/. Open your terminal and navigate to your desired directory. Then, run the following command:

git clone https://github.com/rhythm-semwal/Build-Your-Own-Rate-Limiter
Navigate to the project directory using the following command:

```bash
cd Build-Your-Own-Rate-Limiter
```

**Create a Virtual Environment**
```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```
```bash
<directory path>.venv/bin/python3 -m pip install --upgrade pip
```

**Install the required Python libraries using pip:**
```bash
pip3 install fastapi
```

**Running the Application**

Start the Development Server:

Run the following command in your terminal to start the development server:

```bash
uvicorn main:app --reload
```




