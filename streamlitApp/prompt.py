INFERENCE_PROMPT = """
Your task is to determine how relevant each Github issue is to the USER PREFERENCES.

You are given the following entities:
USER_PREFERENCES: List of domains and coding-related areas the user is interested in.
PAST_CONTRIBUTIONS: List of descriptions of previous Github issues the user has worked on.
ISSUES: A list of dictionary that contains the keys "title" and "summary"

—
PROCEDURE:
For each issue in ISSUES:
1. Think of the programming languages needed to solve this Github ISSUE. Avoid stating common skills such as Github, unit testing etc.
2. Think of the specific area within computer science this issue belongs to for eg. front-end, backend, systems, devops, machine learning etc.
3. Compare the programming languages and area of the ISSUE with the USER PREFERENCES and PAST_CONTRIBUTIONS (if any) and determine if the USER would be interested in solving this ISSUE.
4. Generate LABEL as HIGHLY_RECOMMENDED, NOT_RECOMMENDED or UNABLE_TO_DETERMINE based on whether USER will be interested in solving the ISSUE.
5. Generate the EXPLANATION that captures the reasoning for the generated LABEL.

-
OUTPUT:

The output should be in JSON format:
[
    {{
        "LABEL": Correct Label for the ISSUE 1,
        "EXPLANATION": Explanation for why you chose this LABEL 1.
    }},
    {{
        "LABEL": Correct Label for the ISSUE 2,
        "EXPLANATION": Explanation for why you chose this LABEL 2.   
    }},
    ....
]

There are only three possible values for each LABEL:
HIGHLY RECOMMENDED: The ISSUE is highly aligned with USER PREFERENCES and would recommend this ISSUE to the USER.
NOT RECOMMENDED: The ISSUE does not align in any way with the USER PREFERENCES and would not recommend this ISSUE to the USER.
UNABLE TO DETERMINE: There is not enough context to determine if the USER would be interested in solving this ISSUE.

Limit each EXPLANATION to less than 100 words. Be concise with your reasoning. Don't return too many newline characters.

###
USER_PREFERENCES: {USER_PREFERENCES}
———————————
PAST_CONTRIBUTIONS:{PAST_CONTRIBUTIONS}
———————————
ISSUES: {ISSUES}
———————————

OUTPUT:
"""
