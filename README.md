# CF Pipeline

A command-line interface tool for automating Codeforces competitive programming workflows.

![Version](https://img.shields.io/badge/version-0.0.5-blue)
![Status](https://img.shields.io/badge/status-alpha-orange)

## Overview

CF Pipeline is a CLI application that streamlines interaction with the Codeforces competitive programming platform. Built with a "plumbing and porcelain" architecture (inspired by Git), it provides a set of composable commands for automating common Codeforces tasks.

## Features

- **Problem retrieval**: Download contest problems directly to your local environment
- **Solution testing**: Test your solutions against sample test cases before submission
- **Workflow automation**: Combine commands to create custom workflows
- **Framework extensibility**: Build your own commands on top of the core framework

## Installation

```bash
pip install -r requirements.txt
python setup.py install
```

## Usage

Basic commands:

```bash
# Get a specific problem
cfp get-problem <contest-id> <problem-index>

# Test your solution against problem test cases
cfp test-solution <solution-file> <contest-id> <problem-index>
```

## Architecture

CF Pipeline follows a modular approach:

- **Core modules**: Problem representation, contest data, and configuration management
- **Commands**: Single-purpose tools that can be combined into workflows
- **API utilities**: Tools for interacting with the Codeforces API

## Why Use CF Pipeline?

- **Save time**: Automate repetitive tasks in the competitive programming workflow
- **Focus on coding**: Reduce time spent on administrative tasks
- **Integration**: Use from your terminal without switching to the browser
- **Customization**: Build and extend with your own commands and workflows

## Development Status

This project is in early alpha development (version 0.0.5 "AlmostAlpha"). Many planned features are still in progress.

## Contributing

Contributions are welcome! See our contribution guidelines for details.

## License

See the [LICENSE](RESOURCES/LICENSE) file for details.