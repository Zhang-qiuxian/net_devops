from typing import Callable, Iterator
from concurrent.futures import ThreadPoolExecutor, as_completed, Future

ThreadPool: int = 50


def start_thread(data: list[dict]) -> str:
    """
    开启线程池函数
    :param func:需要多线程的函数
    :param data:传递的参数
    :return:
    """
    with ThreadPoolExecutor(max_workers=ThreadPool) as p:
        res: Iterator[Future] = as_completed([p.submit(item['func'], **item['kwargs']) for item in data])
        response_data = [i.result() for i in res]
        return response_data
