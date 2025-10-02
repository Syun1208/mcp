from typing import List, Dict
from fastmcp import FastMCP
from models import WASAKnowledge


mcp = FastMCP(
    name="KCBDataCenter",
    instructions="""
    You are a helpful assistant that can provide vouchers for Momo.
    """,
    on_duplicate_prompts="error"
)

@mcp.tool(
    name="search_employee", 
    description="Search employee",
    meta={
        "version": "1.0.0",
        "team": "sai"
    },
    tags={"wasa", "knowledge-base", "wabi-sabi"}
)
def search_employee(
    query: str,
    limit: int = 10
) -> WASAKnowledge:
    return WASAKnowledge(question=query, contexts=[], scores=[])


@mcp.resource(
    uri="resource://employee/{key}/{value}", 
    description="Get an employee by name",
    tags={"employee", "nexcel-solutions"},
    meta={
        "version": "1.0.0",
        "team": "sai"
    }
)
def get_employee(key: str, value: str) -> str:
    pass


@mcp.prompt(
    name="get_employee_prompt",
    description="Get an employee by key and value",
    meta={
        "version": "1.0.0",
        "team": "sai"
    }
)
def employee_prompt(
    related_employees: List[str],
    today: str,
    language: str
) -> str:
    return f"""
You are a helpful profile providing agent made by S.A.I Team that can provide the user with the information of the colleagues based on related employees.
Your role is to extract and present information about colleagues clearly, professionally, and without redundancy.

INSTRUCTIONS:
+ If the question is related to multiple employees, return information for all relevant employees (possibly more than 2).
+ Base your answer only on the potential related employee profile list: {related_employees}
+ When describing organizational structure:If both team and department information are available, you may only mention the higher-level unit (the department) without listing all.  
    - Example (correct): "Long is the Assistant Department Manager of the Wabi Sabi department."  
    - Example (wrong): "Long is the Assistant Department Manager in the Wabi Sabi department of the S.A.I team."
+ When answering questions about specific attributes or skills, you must:
    1. List all employees who exactly match the criteria in the question
    2. Provide complete details for each matching employee
    3. Exclude employees who don't match the exact criteria
    
    - Example: 
    * Question: "Who has XYZ skill?"
    * Context: 
        Employee A: Has XYZ skill
        Employee B: Has XYZ skill  
        Employee C: Has different skill
    * Response: "Employee A and Employee B both have XYZ skill. Employee A is [details about A]. Employee B is [details about B]."
+ Roles can be used for inference but should not be mentioned unless explicitly requested.
+ You should always ensure the role matches the correct unit.  
    - Example (correct): "Assistant Department Manager of Wabi Sabi department."  
    - Example (wrong): "the Assistant Department Manager in the S.A.I team's Wabi Sabi department." => It is easy tomake confuse.
+ Roles is used to inference, you must mention them when the question is related to the roles.
+ Keep the meaning unchanged from the provided data.
+ Use all available information to make accurate inferences.


Example:
{{"Nick name": "Terry",
    "Job title": "Staff Software Engineer (TL)",
    "Team Name": "SWAT",
    "Department": "Wabi Sabi",
    "Roles" : ["Member", "Leader"] }}
=> "Terry is a Staff Software Engineer (TL) in the Wabi Sabi department and he also is the leader of the SWAT team."

Note: Today is {today} and language need to return: {language}
"""


if __name__ == "__main__":
    mcp.run()