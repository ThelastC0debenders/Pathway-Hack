
import sys
import os

# Ensure backend is in path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from change_intelligence import analyze_code_changes

def main():
    print("🧪 Testing Change Intelligence Module")
    print("====================================")

    # 1. Define Old Code
    old_code = """
def process_data(data, format="json"):
    \"\"\"Process data in specified format.\"\"\"
    if format == "json":
        return {"processed": True, "data": data}
    return data
    """

    # 2. Define New Code (Breaking Change: renamed arg 'format' to 'output_format')
    new_code = """
def process_data(data, output_format="json"):
    \"\"\"Process data in specified output format.\"\"\"
    if output_format == "json":
        return {"processed": True, "data": data}
    return data
    """

    print("\n📝 Analyzing changes...")
    print(f"Old signature: def process_data(data, format='json')")
    print(f"New signature: def process_data(data, output_format='json')")

    # 3. Analyze
    result = analyze_code_changes(
        old_content=old_code,
        new_content=new_code,
        file_path="utils/processor.py"
    )

    # 4. Print Results
    print("\n📊 Analysis Result:")
    print(f"Changed: {result['changed']}")
    print(f"Breaking Change: {result['breaking_change']}")
    
    if result['breaking_change']:
        print(f"Severity: {result['severity']}")
        print(f"Details: {result['breaking_details']}")
    
    print("\nImpact Analysis:")
    for impact in result['impact']:
        print(f"- {impact}")

    print("\nRecommendations:")
    for rec in result['recommendations']:
        print(f"- {rec}")

if __name__ == "__main__":
    main()
