# HCMUS Socket Programming Project

This repository contains the source code and related materials for the Socket Programming project developed at Ho Chi Minh City University of Science (HCMUS). The project focuses on implementing a client-server application using socket programming techniques.

## Project Overview

The main objective of this project is to create a console-based FTP Client application that facilitates file upload and download between a client and server through socket communication. The project is implemented in Python and demonstrates fundamental concepts of network programming, including:

- Establishing connections between client and server using sockets
- Handling multiple client requests
- Implementing file transfer protocols
- Managing user authentication and session control

## Repository Structure

The repository includes the following files:

- `main.py`: The main entry point of the application.
- `LoginPage.py`: Manages user authentication.
- `Menu.py`: Provides the main menu interface for users.
- `MailSender.py`: Handles the sending of files from client to server.
- `MailReceiver.py`: Manages the receiving of files from the server.
- `InterfaceLib.py`: Contains common interface components used across the application.
- `MailLib.py`: Provides utilities for handling mail operations.
- `manageInfo.py`: Manages user information and session data.
- `SendPage.py`: Interface for sending files.
- `ReceivePage.py`: Interface for receiving files.
- `Report.pdf`: Detailed documentation and report of the project.
- `filter.json`: Configuration file for filtering specific data.
- `__pycache__/`: Directory containing compiled Python files.

## Getting Started

To run the application, ensure you have Python installed on your system. Clone the repository and execute the following command:

```bash
python main.py
```

Follow the on-screen instructions to navigate through the application.

## Documentation
For a comprehensive understanding of the project, including design decisions, implementation details, and future enhancements, please refer to the Report.pdf file included in this repository.

## Contributors
- Nguyen Cong Tuan (K22-HCMUS)
- Dinh Nguyen Gia Bao (K22-HCMUS)

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
