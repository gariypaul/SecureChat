# Secure Instant Point-to-Point Messaging System

## Project Overview

Design a secure instant messaging tool that enables communication between two parties, Alice and Bob, similar to platforms like gtalk, Skype, or ICQ chat. The tool should ensure privacy and security through encryption.

## Functional Requirements

- **Message Exchange**: Alice and Bob can use the tool to send and receive encrypted messages.
- **Password-Based Setup**: Both users share a common password which is used to set up the encryption and decryption of messages.

## Technical Requirements

### Encryption

- **Minimum Key Length**: Each message must be encrypted with a key of at least 56 bits.
- **Cipher Selection**: Recommend which cipher should be used that supports the key length requirement.
- **Key Derivation**: Describe the method to generate a secure key from the shared password without using the password directly as the key.

### GUI Requirements

- **Interface Design**: A graphical user interface where sent and received messages are displayed both in ciphertext and decrypted form.

### Network Communication

- **Connection Setup**: How Alice and Bob initially establish a secure connection.
- **Connection Maintenance**: Strategy to maintain the connection over the Internet, possibly using socket programming.

### Security Enhancements

- **Variable Ciphertext for Repeated Messages**: Implement a method to ensure that sending the same message multiple times results in different ciphertexts.
- **Key Management**: Design a key management system to periodically update the encryption key and enhance security.

## Implementation Suggestions

- **Languages and Tools**: The system can be implemented using programming languages like Java, C++, or Python. Open-source tools and libraries for encryption and network communication are encouraged.

## Design Justification

- **Security Measures**: Explain the choice of encryption algorithm, key derivation process, and any additional security protocols implemented.
- **GUI Functionality**: Detail the functionality of the user interface and how it contributes to user experience and security.
- **Network Strategy**: Justify the methods used for setting up and maintaining network connections.

## Documentation and Reporting

- **Design Overview**: Provide a detailed description and justification of the design choices made.
- **Screenshots**: Include screenshots of the GUI and examples of the system in operation.
- **Function Explanations**: Describe major functions and how they contribute to the project's requirements.

## Appendix

- **References**: List any references or resources used during the development of the project.
