import argparse

if __name__=="__main__":
  parser = argparse.ArgumentParser(
    description="something"
  )

  parser.add_argument("--config", required=True)
  args = parser.parse_args()

  print(args.config)