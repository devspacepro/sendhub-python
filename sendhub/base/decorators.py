from log import log
import time
import constants         
    
def retry_wrapper(max_retries):
    '''
    Wrap the function with a retry mechanism.  Try up to max_retries
    and if we cannot succeed, re-raise the exception on max_retries 
    iteration.  For example, if we specify 10 retries, then on the 
    10th retry, we will re-raise the exception.  Otherwise, we will
    silently (except for logging) keep trying.
    '''
    
    def decorate(f):
        
        def new_f(*args, **kwargs):
            
            # allow configuration of retry
            if constants.DISABLE_API_RETRIES:
                retry_count = max_retries
            else:
                retry_count=0
                
            while retry_count <= max_retries:
                
                try:
                    
                    # try to run the function as normal
                    result = f(*args, **kwargs)
                    
                    # exit the loop to return the result
                    break
                    
                except:
                    
                    # we've reached max_retries allowed, re-raise
                    if retry_count == max_retries:
                        raise
                    
                    else:
                        
                        # increment retry count
                        retry_count += 1
                        
                        # log our retry attempt
                        log.warn("Repeatable function %s failed, waiting %i seconds before retrying up to %s more times" % (f.func_name, 1.5**retry_count, max_retries-retry_count))
                        
                        # sleep for a bit, in the event there is a network hiccup and continue to back off the api as we continue to fail
                        time.sleep(1.5**retry_count)
                        
                        # continue to the next iteration
                        continue
                    
            return result
        new_f.func_name = f.func_name
        return new_f
    return decorate