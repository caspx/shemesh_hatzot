
def safe_run(func):
    def wrap(*func_args, **func_kwargs):
        try:
            return func(*func_args, **func_kwargs)
        except Exception as ex:
            print(ex)
    return wrap
