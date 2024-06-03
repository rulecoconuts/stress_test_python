import concurrent.futures
from typing import Callable, Iterable

def perform(action : Callable, args:Iterable[Iterable], executor: concurrent.futures.ThreadPoolExecutor) -> Iterable:
    """Perform an action multiple times on different arguments. 

    Args:
        action (Callable): A function to perform
        args (Iterable[Iterable]): An iterable whose elements are the inorder arguments of the action
        executor (concurrent.futures.ThreadPoolExecutor): A thread pool executor to manage/handle the calls to the action

    Returns:
        Iterable: The returned results of performing the action. Not necessarily in the order that they were passed to the function.
        So it is advisable to pass an id as an argument to the action, and return it along with the action's result

    Yields:
        Iterator[Iterable]: _description_
    """
    futures = []
    for arg in args:
        futures.append(executor.submit(action, *arg))

    for completed in concurrent.futures.as_completed(futures):
        yield completed.result()

def initializeExecutorAndPerform(action : Callable, args:Iterable[Iterable], max_workers: int=800)->Iterable:
    """Perform an action multiple times on different arguments using a ThreadPoolExecutor.

    Args:
        action (Callable): A function to perform
        args (Iterable[Iterable]): An iterable whose elements are the inorder arguments of the action
        max_workers (int, optional): The maximum number of workers needed to perform the action for all arguments. Defaults to 800.
    Returns:
        Iterable: The returned results of performing the action. Not necessarily in the order that they were passed to the function.
        So it is advisable to pass an id as an argument to the action, and return it along with the action's result

    Yields:
        Iterator[Iterable]: _description_
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        yield from perform(action, args, executor)