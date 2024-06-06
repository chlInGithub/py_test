"""
使用多环境profile配置文件
"""

import yaml
import sys

def load_config(environment:str)->dict:
    """
    从config-xxx.yaml加载配置

    Args:
      environment (str): The environment to load config for ('dev', 'test', 'prod').

    Returns:
      dict: The loaded configuration as a dictionary.
    """

    try:
        with open(f"config-{environment}.yaml", 'r') as file:
            config = yaml.safe_load(file)
            return config

    except FileNotFoundError:
        print("Error: Configuration file not found.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python xxx.py <environment>")
        sys.exit(1)

    env = sys.argv[1]

    if env not in ['dev', 'test', 'prod']:
        print("Invalid environment. Choose from 'dev', 'test', or 'prod'.")
        sys.exit(1)

    config = load_config(env)

    # Example usage of the loaded configuration, checking if config is not None.
    if config:
        print(f"Database host for {env} environment is {config['database']['host']}")
    else:
        print(f"No configuration found for {env} environment.")
