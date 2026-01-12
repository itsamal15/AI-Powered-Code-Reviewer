import argparse

def main():
    parser = argparse.ArgumentParser(description="AI Reviewer CLI")
    parser.add_argument("--path", type=str, required=True, help="Folder to scan")
    
    args = parser.parse_args()
    print("Code review completed for:", args.path)

if __name__ == "__main__":
    main()
