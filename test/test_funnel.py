import time

from pydantictes.models import TesExecutor, TesState, TesTask


def test_funnel_multi_executors(tes_funnel_client):
    executor = TesExecutor(
        image="alpine",
        command=["sh", "-c", "echo 'foobar' > /pulsar_work/moo"],
    )
    executor2 = TesExecutor(
        image="alpine",
        command=["cat", "/pulsar_work/moo"],
    )
    executor3 = TesExecutor(
        image="alpine",
        command=["cat", "/pulsar_work/moo"],
    )
    task = TesTask(
        name="3 executor test task",
        description="Test a three pod staging scenario (imagine pulsar staging, biocontainer, pulsar staging)",
        executors=[executor, executor2, executor3],
        volumes=["/pulsar_work/"],
    )
    task_response = tes_funnel_client.create_task(task)
    task_basic = tes_funnel_client.get_task(task_response, "BASIC")
    assert task_basic.id == task_response.id


def test_funnel_cancel(tes_funnel_client):
    executor = TesExecutor(
        image="alpine",
        command=["sh", "-c", "sleep 120"],
    )
    task = TesTask(
        name="Cancel test task",
        description="Cancel test.",
        executors=[executor],
        volumes=["/pulsar_work/"],
    )
    task_response = tes_funnel_client.create_task(task)
    tes_funnel_client.cancel_task(task_response)
    time.sleep(3)
    task_full = tes_funnel_client.get_task(task_response, "FULL")
    assert task_full.state == TesState.CANCELED


def test_list_tasks(tes_funnel_client):
    executor = TesExecutor(
        image="alpine",
        command=["sh", "-c", "sleep 120"],
    )
    task = TesTask(
        name="index task test",
        description="Index test.",
        executors=[executor],
        volumes=["/pulsar_work/"],
    )
    task_response = tes_funnel_client.create_task(task)
    list_response = tes_funnel_client.list_tasks()
    found = False
    for task in list_response.tasks:
        if task.id == task_response.id:
            found = True
    assert found


def test_funnel_service_info(tes_funnel_client):
    tes_funnel_client.service_info()
