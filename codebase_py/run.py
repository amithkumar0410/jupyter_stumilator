import io, traceback
from contextlib import redirect_stdout, redirect_stderr

user_sessions = {}

class InputRequired(Exception):
    def __init__(self, prompt=""):
        self.prompt = prompt


class RunCell:
    def __init__(self, username):
        self.username = username
        if username not in user_sessions:
            user_sessions[username] = {
                "env": {},
                "input_queue": []
            }

        self.env = user_sessions[username]["env"]
        self.input_queue = user_sessions[username]["input_queue"]

    def run_code_persistent(self, code, new_input=None):
        if new_input is not None:
            self.input_queue.append(new_input)

        def notebook_input(prompt=""):
            if self.input_queue:
                return self.input_queue.pop(0)
            raise InputRequired(prompt)

        buf_out, buf_err = io.StringIO(), io.StringIO()

        try:
            with redirect_stdout(buf_out), redirect_stderr(buf_err):
                exec(code, {**self.env, "input": notebook_input}, self.env)

            return {
                "status": "done",
                "output": buf_out.getvalue() + buf_err.getvalue()
            }

        except InputRequired as e:
            return {
                "status": "input",
                "prompt": e.prompt,
                "output": buf_out.getvalue()
            }

        except Exception:
            return {
                "status": "error",
                "output": traceback.format_exc()
            }
