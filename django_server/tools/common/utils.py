from typing import Callable, Iterator, Any
from concurrent.futures import ThreadPoolExecutor, as_completed, Future

ThreadPool: int = 50


def start_thread(fn: Callable, *, data: list[Any], args, /, **kwargs) -> Iterator[Future[Any]]:
    """
    开启线程池函数，第一个是需要开启线程池的函数，其它参数按位置传参
    :param args:
    :param fn: 运行的函数
    :param data:需要开启线程池的列表
    :return:
    """
    with ThreadPoolExecutor(max_workers=ThreadPool) as p:
        res: Iterator[Future] = as_completed([p.submit(__fn=fn, *args, *kwargs) for item in data])
        response_data = as_completed([i.result() for i in res])
        return response_data
