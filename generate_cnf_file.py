import os

# Function to generate a CNF string based on variables and clauses
def generate_cnf(variables, clauses):
   
    cnf = f"p cnf {variables} {len(clauses)}\n"
    
    for clause in clauses:
        cnf += " ".join(map(str, clause)) + " 0\n"
    
    return cnf

# Function to generate simple test cases with random clauses
def generate_test_cases():
    # Create the 'example' folder if it doesn't exist
    if not os.path.exists("example"):
        os.makedirs("example")

    test_cases = []

    # Test case 1: Simple 3-variable, 2-clause CNF
    test_cases.append({
        "filename": "example/cnf_example1.txt",
        "variables": 3,
        "clauses": [
            [1, -2],
            [-1, 2, 3]
        ]
    })

    # Test case 2: 3-variable, 3-clause CNF
    test_cases.append({
        "filename": "example/cnf_example2.txt",
        "variables": 3,
        "clauses": [
            [1, 2, -3],
            [-1, -2, 3],
            [1, -2, 3]
        ]
    })

    # Test case 3: 4-variable, 2-clause CNF
    test_cases.append({
        "filename": "example/cnf_example3.txt",
        "variables": 4,
        "clauses": [
            [1, -4],
            [-2, 3]
        ]
    })

    # Test case 4: 5-variable, 4-clause CNF
    test_cases.append({
        "filename": "example/cnf_example4.txt",
        "variables": 5,
        "clauses": [
            [1, -2, 3],
            [-1, 2],
            [3, -4, 5],
            [-5, 4]
        ]
    })

    # Test case 5: 1-variable, 1-clause CNF
    test_cases.append({
        "filename": "example/cnf_example5.txt",
        "variables": 1,
        "clauses": [
            [1]
        ]
    })

    # Test case 6: All unit clauses (3 variables, 3 unit clauses)
    test_cases.append({
        "filename": "example/cnf_example6.txt",
        "variables": 3,
        "clauses": [
            [1],
            [-2],
            [3]
        ]
    })

    # Test case 7: Random CNF (10 variables, 5 clauses)
    test_cases.append({
        "filename": "example/cnf_example7.txt",
        "variables": 10,
        "clauses": [
            [1, -2, 3],
            [-1, 2, 4, 5],
            [-3, 6, 7],
            [2, -5, 8],
            [-9, 10]
        ]
    })

    # Generate CNF files
    for test_case in test_cases:
        cnf = generate_cnf(test_case["variables"], test_case["clauses"])
        with open(test_case["filename"], "w") as f:
            f.write(cnf)
            print(f"Generated {test_case['filename']}")

# Run the function to generate test cases
generate_test_cases()
