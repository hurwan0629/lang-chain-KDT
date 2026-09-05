import sys
text = sys.stdin.read()

print(f"stdout: {text}")
print("stderr message: ", file=sys.stderr)