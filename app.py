import argparse
from typing import Any
import google.generativeai as genai
import os


# TODO: make it abstract
class Model:
    model: genai.GenerativeModel
    files: dict[str, Any]
    # TODO:maybe save the Q/A
    # TODO: make it async using the REST endpoints and use a context manager

    def __init__(self, model: genai.GenerativeModel, files: list[str]) -> None:
        self.model = model
        self.files = {}
        self.add_files(files)

    def add_files(self, files: list[str]) -> None:
        for file in files:
            if file in self.files:
                continue
            file_id = genai.upload_file(file)
            self.files[file] = file_id
        return None

    def ask_question(self, question: str) -> str:
        # TODO: improve the prompt.
        # Test to add something like: You must response the following answer using the filles at your disposal.
        return self.model.generate_content([question, *self.files.values()]).text


def _get_cli_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Talk to files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "--files",
        type=str,
        nargs="+",
        required=True,
        help="A list of files to talk to",
    )
    return p.parse_args()


def _get_question() -> str:
    return input("Your question:")


def _send_response(response: str) -> None:
    print(response)
    return None


def _questions_loop(model: Model) -> str | None:
    while question := _get_question():
        if question == "stop":
            return "stopped by user"
        response = model.ask_question(question)
        _send_response(response)
    return None


def _set_up_google_model() -> Model:
    print("Setting up model")
    genai.configure(api_key=os.environ["API_KEY"])
    google_model = genai.GenerativeModel("gemini-1.5-flash")
    return Model(model=google_model, files=set())


def main() -> None:
    args = _get_cli_args()
    model = _set_up_google_model()
    model.add_files(args.files)
    _questions_loop(model)
    return None


if __name__ == "__main__":
    main()
