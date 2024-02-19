from benchmark.constraints.fibonacci_word_count_constraint import FibonacciSequenceConstraint
from benchmark.question import Question
from utils.element_type import ElementType


# Create a Fibonacci word count constraint
fib_word_constraint = FibonacciSequenceConstraint(ElementType.WORDS)

# Create a question with this constraint
question = Question(constraints=[fib_word_constraint])

# Generate a prompt for the question
question.generate_prompt()
print(question.prompt)  # Output will include the constraint description

# Evaluate a sample response
response = "This is a test response with nine words total."
evaluation_result = question.evaluate_response(response)

# Provide feedback based on the evaluation
feedback = question.provide_feedback(evaluation_result)
print(feedback)
