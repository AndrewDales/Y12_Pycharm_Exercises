def calc_grade(raw_score: int) -> str:

    # Check raw_score is an integer
    if not isinstance(raw_score, int):
        raise TypeError("Raw score must be an integer")

    # Check raw_score is in the correct range
    elif raw_score > 350:
        raise ValueError("Raw score must be less than or equal to 350")

    elif raw_score < 0:
        raise ValueError("Raw score must be greater than or equal to 0")

    elif raw_score >= 264:
        grade = "A*"

    elif raw_score >= 229:
        grade = "A"

    elif raw_score >= 189:
        grade = "B"

    elif raw_score >= 150:
        grade = "C"

    elif raw_score >= 111:
        grade = "D"

    elif raw_score >= 72:
        grade = "E"

    else:
        grade = "U"

    return grade



if __name__ == "__main__":
    print(calc_grade(234))
