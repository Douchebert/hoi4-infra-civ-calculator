# HOI4 Infra + Civ Factory Calculator
# Learning project

def main():
    print("=== HOI4 Build Order Calculator ===")
    print("Welcome! Let's plan your early game construction.\n")
    
    # Get user inputs
    civs = int(input("How many Civilian Factories do you currently have? "))
    year = input("Starting year (e.g. 1936)? ")
    
    print(f"\nCurrent situation: {civs} Civs in {year}")
    print("We'll expand this step by step!")

if __name__ == "__main__":
    main()