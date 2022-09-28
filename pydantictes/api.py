from typing import (
    Union,
)

import requests

from .models import (
    TesCancelTaskResponse,
    TesCreateTaskResponse,
    TesListTasksResponse,
    TesServiceInfo,
    TesTask,
)

HasTaskId = Union[TesCreateTaskResponse, TesTask, str]


class TesClient:
    def __init__(self, url: str):
        self._url = url

    def create_task(self, task: TesTask) -> TesCreateTaskResponse:
        url = self._build_url("tasks")
        response = requests.post(url, data=task.json())
        response.raise_for_status()
        return TesCreateTaskResponse(**response.json())

    def get_task(self, has_task_id: HasTaskId, view) -> TesTask:
        task_id = self._get_task_id(has_task_id)
        url = self._build_url(f"tasks/{task_id}")
        response = requests.get(
            url,
            params={"view": view},
        )
        response.raise_for_status()
        response_dict = response.json()
        self._hack_task_response_around_funnel(response_dict)
        return TesTask(**response_dict)

    def cancel_task(self, has_task_id: HasTaskId) -> TesCancelTaskResponse:
        task_id = self._get_task_id(has_task_id)
        url = self._build_url(f"tasks/{task_id}:cancel")
        response = requests.post(url)
        response.raise_for_status()
        return TesCancelTaskResponse(**response.json())

    def service_info(self) -> TesServiceInfo:
        url = self._build_url("/tasks/service-info")
        response = requests.get(url)
        response.raise_for_status()
        response_dict = response.json()
        self._hack_service_info_around_funnel(response_dict)
        return TesServiceInfo(**response_dict)

    def list_tasks(self) -> TesListTasksResponse:
        url = self._build_url("tasks")
        response = requests.get(url)
        response.raise_for_status()
        response_dict = response.json()
        self._hack_list_response_around_funnel(response_dict)
        return TesListTasksResponse(**response_dict)

    def _get_task_id(self, has_task_id: HasTaskId) -> str:
        if not isinstance(has_task_id, str):
            task_id = has_task_id.id
        else:
            task_id = has_task_id
        assert task_id
        return task_id

    def _hack_list_response_around_funnel(self, response_dict):
        for task in response_dict["tasks"]:
            if "executors" not in task:
                task["executors"] = []

    def _hack_service_info_around_funnel(self, response_dict):
        if "id" not in response_dict:
            response_dict["id"] = "unknown id"
        if "organization" not in response_dict:
            response_dict["organization"] = {
                "name": "unknown organization",
                "url": "http://unkonwnservice.com/",
            }
        if "version" not in response_dict:
            response_dict["version"] = "0.0.1"
        if "type" not in response_dict:
            response_dict["type"] = {
                "artifact": "tes",
                "group": "org.ga4gh",
                "version": "1.0.0",
            }

    def _hack_task_response_around_funnel(self, response_dict):
        if "logs" in response_dict:
            logs = response_dict["logs"]
            if len(logs) == 1 and logs[0] == {}:
                response_dict["logs"] = []
            for log in logs:
                if "outputs" not in log:
                    log["outputs"] = []
                if "logs" in log:
                    for inner_log in log["logs"]:
                        if "exit_code" not in inner_log:
                            inner_log["exit_code"] = -255

    def _build_url(self, path: str) -> str:
        return f"{self._url}/v1/{path}"
