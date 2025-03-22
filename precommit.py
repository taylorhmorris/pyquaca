import subprocess

if __name__ == "__main__":
  # Linting / Style checks
  print("Linting / Style checks")
  subprocess.run(["black", "./src", "./tests"])
  subprocess.run(["pylint", "./src", "./tests"])
  subprocess.run(["isort", "./src", "./tests"])
  subprocess.run(["flake8", "./src", "./tests"])  
  
  # Type checks
  print("Type checks")
  subprocess.run(["mypy", "./src", "./tests"])
  
  # Security checks
  print("Security checks")
  subprocess.run(["bandit", "-r", "./src", "./tests"])
  
  # Package checks
  print("Package checks")
  subprocess.run(["pyroma", "."])

  # Test coverage
  print("Testing and coverage")
  subprocess.run(["coverage", "run", "-m", "pytest", "./tests"])
  subprocess.run(["coverage", "report", "-m"])