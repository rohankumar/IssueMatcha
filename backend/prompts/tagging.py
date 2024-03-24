tagging_prompt = ('''
You are the maintainer of an open source repository on Github. Your task is to provide useful tags for this repository.
You are given the following entities in markdown:

ISSUE TITLE: The title of the issue.
ISSUE BODY: Description of the issue.
COMMENTS: Any comments on the issue by other contributors in a list format.
README: README file of the repository which provides additional information about the repository.
__

TASK: 
Generate a set of 20 tags that can be used to distinguish this repository. For example skills, expertise, domain, background required to work on this repository.
Limit each tag length to a maximum of 3 words. Let the output be a json as this template: \\{"tags"\\: ["", "",..]}
###
———————————
{query_str}
———————————
''')

summary_prompt=('''
You are the maintainer of an open source repository on Github. Your task is to provide a useful brief summary for this repository.
You are given the following repository's README in markdown:

README: README file of the repository which provides additional information about the repository.
__

TASK: 
Generate a summary that can be used to distinguish this repository.
Let the output be a json as this template: \\{"summary"\\: ["", "",..]}
###
———————————
{query_str}
———————————
''')


# summary_prompt = ('''You are the maintainer of an open source repository on Github. Your task is to provide a useful brief summary for this repository.
# You are given the repository's README file in markdown to provide more information about it. Generate a summary that can be used to distinguish this repository.
# Let the output be a json as this template: \\{"summary"\\: ["", "",..]}
# Here is the README content: 
# {query_str}
# ''')

issue_tagging_prompt = ('''You are the maintainer of an open source repository on Github. Your task is to provide useful tags for this open issue in the repository.
You are given the repository's README file in markdown to provide more information about it. Generate a set of 20 tags that can be used to distinguish this repository. For example skills, expertise, domain, background required to work on this repository.
Limit each tag length to a maximum of 3 words. Let the output be a json as this template: \\{"tags"\\: ["", "",..]}
Here is the README content: 
{query_str}
''')

issue_tagging_prompt='''You are given the following entities in markdown:

ISSUE TITLE: The title of the issue.
ISSUE BODY: Description of the issue.
COMMENTS: Any comments on the issue by other contributors in a list format.
README: README file of the repository which provides additional information about the repository.

—
TASK:
Your task is to label the ISSUE based on the following parameters:
{}
'''


# DEFAULT_TEXT_QA_PROMPT_TMPL = (
#     "Context information is below.\n"
#     "---------------------\n"
#     "{context_str}\n"
#     "---------------------\n"
#     "Given the context information and not prior knowledge, "
#     "answer the query.\n"
#     "Query: {query_str}\n"
#     "Answer: "
# )