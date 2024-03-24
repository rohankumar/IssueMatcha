recommendation_prompt =  """
Your task is to determine how relevant each Github issue is to the USER PREFERENCES.


You are given the following entities:
DOMAIN:
USER_PREFERENCES: List of coding-related areas the user is interested in.
PAST_CONTRIBUTIONS_TAGS: List of tags of previous Github issues the user has worked on or shown interest in.
ISSUES: A list of dictionary that contains the keys "ISSUE_TITLE", "ISSUE_SUMMARY" and "ISSUE_ID"


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
UNABLE_TO_DETERMINE: There is not enough context to determine if the USER would be interested in solving this ISSUE.


Limit each EXPLANATION to less than 100 words. Be concise with your reasoning.


###
USER_PREFERENCES: {USER_PREFERENCES}
———————————
PAST_CONTRIBUTIONS_TAGS:{PAST_CONTRIBUTIONS_TAGS}
———————————
ISSUES: {context_str}
———————————


OUTPUT:
"""

# ("""
# Your task is to determine how relevant the given list Github ISSUES are to the USER PREFERENCES.


# You are given the following entities:
# USER_PREFERENCES: List of coding-related areas the user is interested in. It can be empty list if the user is open to all suggestions.
# PAST_CONTRIBUTIONS_TAGS: List of tags of previous Github issues the user has worked on and shown interest in. It can be an empty list if we have no history for the user.
# List of CANDIDATE ISSUES with each ISSUE as follows:
#     ISSUE TITLE: The title of the Github issue.
#     ISSUE SUMMARY: Description of the Github issue


# —
# PROCEDURE:
# 1. Think of the programming languages needed to solve this Github ISSUE. Avoid stating common skills such as Github, unit testing etc.
# 2. Think of the specific area within computer science this issue belongs to for eg. front-end, backend, systems, devops, machine learning etc.
# 3. Compare the programming languages and area of the ISSUE with the USER PREFERENCES and PAST_CONTRIBUTIONS (if any) and determine if the USER would be interested in solving this ISSUE.
# 4. Generate LABEL as HIGHLY_RECOMMENDED, NOT_RECOMMENDED or UNABLE_TO_DETERMINE based on whether USER will be interested in solving the ISSUE.
# 5. Generate the EXPLANATION that captures the reasoning for the generated LABEL.


# -
# OUTPUT:


# The output should be in a list in JSON format with output in same order as given candidate issues:
# [{{
#    "LABEL": Correct Label for the ISSUE.
#    "EXPLANATION": Explanation for why you chose this LABEL.
# }}]


# There are only three possible values for LABEL:
# HIGHLY RECOMMENDED: The ISSUE is highly aligned with USER PREFERENCES and would recommend this ISSUE to the USER.
# NOT RECOMMENDED: The ISSUE does not align in any way with the USER PREFERENCES and would not recommend this ISSUE to the USER.
# UNABLE_TO_DETERMINE: There is not enough context to determine if the USER would be interested in solving this ISSUE.


# Limit the EXPLANATION to less than 100 words. Be concise with your reasoning.


# ###
# USER_PREFERENCES: {USER_PREFERENCES}
# ———————————
# PAST_CONTRIBUTIONS_TAGS:{PAST_CONTRIBUTIONS_TAGS}
# ———————————
# CANDIDATE_ISSUES: {context_str}

# OUTPUT:
# """
# )

# recommendation_prompt = '''You are the maintainer of an open source repository on Github. Your task is to TAG the ISSUE on this repository.
# You are given the following entities in markdown:

# ISSUE TITLE: The title of the issue.
# ISSUE BODY: Description of the issue.
# COMMENTS: Any comments on the issue by other contributors in a list format.
# README: README file of the repository which provides additional information about the repository.

# —
# TASK:
# Your task is to label the ISSUE based on the following parameters:
# 1. Difficulty of the task: How much time and effort would be required to solve this issue.
# 2. Type of Task: Categorize the issue based on the change neeeded to resolve it. For example: bug fix, feature request, enhancement, documentation etc.

# —
# PROCEDURE:
# - Let's think step by step and output a list of labels.
# - Let the output be in JSON format with two attributes: Difficulty, Type, Reasoning (which your step by step analysis)
# Output format template is as follows: 
# \\{"difficulty": "", "type": "", "reasoning":""\\}
# ###
# ———————————
# ISSUE TITLE:{ISSUE_TITLE}
# ———————————
# ISSUE BODY: {ISSUE_BODY}
# ———————————

# '''
