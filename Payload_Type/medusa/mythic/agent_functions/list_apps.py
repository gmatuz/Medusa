from mythic_payloadtype_container.MythicCommandBase import *
from mythic_payloadtype_container.MythicRPC import *

class ListAppsArguments(TaskArguments):
    def __init__(self, command_line):
        super().__init__(command_line)
        self.args = {}

    async def parse_arguments(self):
        pass


class ListAppsCommand(CommandBase):
    cmd = "list_apps"
    needs_admin = False
    help_cmd = "list_apps"
    description = "This lists all running applications"
    version = 1
    is_exit = False
    is_file_browse = False
    is_process_list = False
    is_download_file = False
    is_remove_file = False
    is_upload_file = False
    author = "@ajpc500"
    argument_class = ListAppsArguments
    attackmapping = []
    browser_script = [BrowserScript(script_name="list_apps", author="@ajpc500")]
    attributes = CommandAttributes(
        supported_python_versions=["Python 2.7"],
        supported_os=[SupportedOS.MacOS],
    )

    async def create_tasking(self, task: MythicTask) -> MythicTask:
        resp = await MythicRPC().execute("create_artifact", task_id=task.id,
            artifact="NSWorkspace.sharedWorkspace().runningApplications()",
            artifact_type="API Called",
        )
        return task

    async def process_response(self, response: AgentResponse):
        pass
