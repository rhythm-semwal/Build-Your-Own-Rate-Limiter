from RateLimitingAlgorithms import TokenBucket, RateLimit


class RateLimitFactory:
    @staticmethod
    def get_instance(algorithm: str = None) -> RateLimit:
        if algorithm == "TokenBucket":
            return TokenBucket()

        # elif algorithm == "FixedCounterWindow":
        #     return FixedCounterWindow()
        #
        # elif algorithm == "SlidingWindow":
        #     return SlidingWindow()
        #
        # else:
        #     return SlidingWindowCounter()
