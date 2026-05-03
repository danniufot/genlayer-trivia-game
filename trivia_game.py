# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json

class TriviaGame(gl.Contract):
    total_questions: u256
    correct_answers: u256
    last_question: str
    last_answer: str
    last_result: str

    def __init__(self):
        self.total_questions = u256(0)
        self.correct_answers = u256(0)
        self.last_question = ""
        self.last_answer = ""
        self.last_result = ""

    @gl.public.write
    def ask_question(self, topic: str) -> str:
        def generate_question() -> str:
            prompt = (
                f"Generate a single trivia question about {topic}. "
                f"Return ONLY the question, nothing else. No answer."
            )
            return gl.nondet.exec_prompt(prompt)
        question = gl.eq_principle.prompt_comparative(
            generate_question,
            principle="Both questions must be about the same topic and be valid trivia questions"
        )
        self.last_question = question
        self.total_questions = self.total_questions + u256(1)
        return question

    @gl.public.write
    def submit_answer(self, question: str, answer: str) -> str:
        self.last_answer = answer
        def check_answer() -> str:
            prompt = (
                f"Question: {question} "
                f"Player answer: {answer} "
                f"Is this answer correct? Reply with only CORRECT or INCORRECT."
            )
            return gl.nondet.exec_prompt(prompt)
        result = gl.eq_principle.prompt_comparative(
            check_answer,
            principle="Both must agree on whether the answer is correct or incorrect"
        )
        self.last_result = result
        if "CORRECT" in result.upper():
            self.correct_answers = self.correct_answers + u256(1)
        return result

    @gl.public.view
    def get_score(self) -> u256:
        return self.correct_answers

    @gl.public.view
    def get_total_questions(self) -> u256:
        return self.total_questions

    @gl.public.view
    def get_last_question(self) -> str:
        return self.last_question

    @gl.public.view
    def get_last_answer(self) -> str:
        return self.last_answer

    @gl.public.view
    def get_last_result(self) -> str:
        return self.last_result
