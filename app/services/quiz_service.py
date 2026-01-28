def evaluate_quiz(quiz, answers):

    score = 0
    feedback = []

    for q, a in zip(quiz, answers):
        # Handle both 'answer' and 'correct_answer' keys
        correct_answer = q.get("answer") or q.get("correct_answer", 0)
        
        if a == correct_answer:
            score += 1
        else:
            feedback.append(f"Review this question: {q.get('question', 'Unknown question')}")

    if len(quiz) > 0:
        percent = int(score / len(quiz) * 100)
    else:
        percent = 0

    return percent, feedback
