def counter_deco(func):
    counter = {'count': 0}  # mutable 객체로 상태 유지

    def wrapper(*args, **kwargs):
        counter['count'] += 1
        result = func(*args, **kwargs)
        return result
    wrapper.counter = counter

    def reset_count():
        counter['count'] = 0
    wrapper.reset_count = reset_count

    return wrapper