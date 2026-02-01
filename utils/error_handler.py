"""
Error handling and retry logic for Claude API calls.
"""

import time
import functools
from typing import Callable, Any
from anthropic import APIError, RateLimitError, APIConnectionError


def handle_api_errors(func: Callable) -> Callable:
    """
    Decorator to handle common API errors gracefully.
    
    Usage:
        @handle_api_errors
        def my_api_call():
            ...
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RateLimitError as e:
            print(f"⚠️  Rate limit exceeded: {e}")
            print("Try again in a few moments.")
            raise
        except APIConnectionError as e:
            print(f"⚠️  Connection error: {e}")
            print("Check your internet connection and try again.")
            raise
        except APIError as e:
            print(f"⚠️  API error: {e}")
            raise
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            raise
    
    return wrapper


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0
) -> Callable:
    """
    Decorator to retry a function with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for each retry delay
        
    Usage:
        @retry_with_backoff(max_retries=3, initial_delay=1.0)
        def my_api_call():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (RateLimitError, APIConnectionError) as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        print(f"❌ Failed after {max_retries} retries")
                        raise
                    
                    print(f"⚠️  Attempt {attempt + 1} failed: {e}")
                    print(f"Retrying in {delay:.1f}s...")
                    time.sleep(delay)
                    delay *= backoff_factor
                except Exception as e:
                    # Don't retry on other errors
                    raise
            
            # Should never reach here, but just in case
            if last_exception:
                raise last_exception
                
        return wrapper
    return decorator
