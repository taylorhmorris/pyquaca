import subprocess

if __name__ == "__main__":
  # Linting / Style checks
  subprocess.run(["pylint", "./src", "./tests"])
  subprocess.run(["black", "./src", "./tests"])
  subprocess.run(["isort", "./src", "./tests"])
  subprocess.run(["flake8", "./src", "./tests"])
  
  # Type checks
  subprocess.run(["mypy", "./src", "./tests"])
  
  # Security checks
  subprocess.run(["bandit", "-r", "./src", "./tests"])
  
  # Package checks
  subprocess.run(["pyroma", "."])

  # Test coverage
  subprocess.run(["coverage", "run", "-m", "pytest", "./tests"])
  subprocess.run(["coverage", "report", "-m"])